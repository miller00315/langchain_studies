import os
from typing import Dict, List
from click import prompt
from dotenv import load_dotenv, find_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

load_dotenv(dotenv_path=find_dotenv())

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

os.environ["INDEX_NAME"] = "langchain-doc-index"


def run_llm(query: str, chat_history: List[Dict[str, any]]) -> Dict:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    doc_search = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], embedding=embeddings
    )

    llm = ChatOpenAI(verbose=True, temperature=0)

    rephrase_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=doc_search.as_retriever(),
        prompt=rephrase_prompt
    )

    stuff_documents_chain = create_stuff_documents_chain(
        llm=llm, prompt=rephrase_prompt
    )

    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, 'context': chat_history})

    return {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }


if __name__ == "__main__":
    res = run_llm(query="What is a Langchina chain")

    print(res)
