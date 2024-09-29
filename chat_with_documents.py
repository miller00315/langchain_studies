from datetime import datetime
import os
from readline import clear_history
import streamlit as st
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

connection = "postgresql+psycopg2://myuser:mypassword@0.0.0.0:5433/mydb"  # Uses psycopg3!
collection_name = "my_docs"

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# loading PDF, DOCX and TXT files as LangChain Documents
def load_document(file):
    import os
    _, extension = os.path.splitext(file)

    match extension:
        case '.pdf':
            from langchain_community.document_loaders import PyPDFLoader
            print(f'Loading {file}')
            loader = PyPDFLoader(file)
        case '.docx':
            from langchain_community.document_loaders import Docx2txtLoader
            print(f'Loading {file}')
            loader = Docx2txtLoader(file)
        case '.txt':
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(file)
        case _:
            print('Document format is not supported!')
            return None

    data = loader.load()
    return data

def chunk_data(data, chunk_size: int = 256, chunk_overlap: int = 20) -> list[Document]:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks

def create_embedings(chuncks: list[Document]):
    embeddings = OpenAIEmbeddings()

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )

    vector_store.add_documents(chuncks)

    return vector_store

def ask_and_get_answer(vector_store: PGVector, q: str, k: int = 3):
    from langchain.chains.retrieval_qa.base import RetrievalQA
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)

    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': k})

    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    
    answer = chain.invoke(q)
    
    return answer['result']

def calculate_embedding_cost(texts: list[Document]):
    import tiktoken

    enc = tiktoken.encoding_for_model('text-embedding-3-small')

    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    
    return total_tokens, total_tokens / 1000 * 0.0004

def clear_history():
    if 'history' in st.session_state:
        st.session_state['history'] = []

if __name__ == '__main__':
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(), override=True)

    st.subheader('LLM Question-Answer Application')

    if 'history' not in st.session_state:
        st.session_state.history = []
    
    with st.sidebar:
        api_key = st.text_input('OpenAi API Key', type='password')

        if api_key:
            os.environ['OPEN_AI_KEY'] = api_key

        uploaded_file = st.file_uploader('Upload a file:', type=['pdf', 'docx', 'txt'])

        chunk_size = st.number_input('Chunk size:', min_value=100, max_value=2048, value=512, on_change=clear_history)

        k = st.number_input('k  neighbors:', min_value=1, max_value=20, value=3, on_change=clear_history)

        add_data = st.button('Add Data', on_click=clear_history)

        if uploaded_file and add_data:
            with st.spinner('Reading, chunking and embedding file'):
                bytes_data = uploaded_file.read()

                file_name = os.path.join('./', uploaded_file.name)

                with open(file_name, 'wb') as file:
                    file.write(bytes_data)

                data = load_document(file_name)

                chunks = chunk_data(data, chunk_size=chunk_size)

                st.write(f'Chunck size: {chunk_size}, Chunks: {len(chunks)}')

                tokens, embedding_cost = calculate_embedding_cost(chunks)

                st.write(f'Embedding cost: ${embedding_cost:.4f}')

                vector_store = create_embedings(chuncks=chunks)

                st.session_state.vector_store = vector_store

                st.success('File uploaded, chunked ans embedded successfully!')
    
    user_question = st.text_input('Ask a question about the content of your file')

    if user_question:
        if 'vector_store' in st.session_state:
            vector_store = st.session_state.vector_store

            answer = ask_and_get_answer(
                    vector_store=vector_store, 
                    q=user_question, 
                    k=k
                )
            
            st.text_area('LLM Answer: ', value=answer)

            if 'history' in st.session_state:
                value = {
                    'question': user_question,
                    'answer': answer,
                    'date': datetime.now()
                }

                update_history = st.session_state.history

                update_history.append(value)

                st.session_state.history = update_history

    st.divider()

    st.subheader('History')

    if 'history' in st.session_state:
        for item in st.session_state.history:
            st.text_area(
                item['question'], 
                value=item['answer'],
            )

            if 'date' in item:
                st.write(item['date'])

    

    