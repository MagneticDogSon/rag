from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import yaml


# Извлечение парметров из конфига
with open('config.yaml', "r") as f:
    conf = yaml.safe_load(f)
    f.close()

chunk_size = int(conf["chunk_size"])
chunk_overlap = int(conf["chunk_overlap"])

# Документы
docs = []

def create_vector_store():
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    all_splits = text_splitter.split_documents(docs)



# Эмбединг
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")


#Векторная база данных
    vectorstore = Chroma.from_documents(
            documents=all_splits,
            collection_name="rag-chroma",
            embedding=embeddings(),
            persist_directory="./.chroma",
        )


# Извлекатель
    retriever = Chroma(
        collection_name="rag-chroma",
        persist_directory="./.chroma",
        embedding_function=embeddings(),
    ).as_retriever()


create_vector_store()