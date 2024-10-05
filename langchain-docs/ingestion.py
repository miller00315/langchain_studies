import os
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv(dotenv_path=find_dotenv())

os.environ["INDEX_NAME"] = "langchain-doc-index"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def scrap_data():
    import requests
    from bs4 import BeautifulSoup
    import os
    import urllib

    # The URL to scrape
    url = "https://api.python.langchain.com/en/latest/langchain_api_reference.html"

    # The directory to store files in
    output_dir = f"{os.getcwd()}/langchain-docs/"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Fetch the page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links to .html files
    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]

        # If it's a .html file
        if href.endswith(".html"):
            # Make a full URL if necessary
            if not href.startswith("http"):
                href = urllib.parse.urljoin(url, href)

            # Fetch the .html file
            file_response = requests.get(href)

            # Write it to a file
            file_name = os.path.join(output_dir, os.path.basename(href))
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(file_response.text)


def ingest_docs():
    loader = ReadTheDocsLoader(f"{os.getcwd()}/langchain-docs/")

    raw_documents = loader.load()

    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)

    documents = text_splitter.split_documents(raw_documents)

    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace(f"{os.getcwd()}/langchain-docs/", "")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")

    PineconeVectorStore.from_documents(
        documents, embeddings, index_name="langchain-doc-index"
    )

    print("****Loading to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()
