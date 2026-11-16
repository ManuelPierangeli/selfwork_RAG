import os
import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions


def load_documents(documents_dir):
    documents = []
    metadatas = []
    ids = []
    id = 0

    for filename in os.listdir(documents_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(documents_dir, filename), "r", encoding="utf-8") as file:
                chuncks = file.read().replace("\n", ".").split("### ")

                for chunk in chuncks:
                    if not chunk.isspace() and not chunk == "":
                        documents.append(chunk)
                        metadatas.append({"source": filename})
                        ids.append(str(id))
                        id += 1

    return documents, metadatas, ids


def get_collection():
    load_dotenv(".env")
    openai_key = os.environ["OPENAI_API_KEY"]

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-3-small"
    )

    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    return chroma_client.get_or_create_collection(
        name="CVs",
        embedding_function=openai_ef
    )


def run_ingest():
    documents_dir = os.path.join("data", "cvs")
    documents, metadatas, ids = load_documents(documents_dir)
    collection = get_collection()

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )


if __name__ == "__main__":
    run_ingest()