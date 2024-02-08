import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import MarkdownTextSplitter

chunk_size = int(700)
chunk_overlap = int(100)

embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

print(embeddings)

loader = DirectoryLoader('Doc/', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
documents = loader.load()
text_splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
texts = text_splitter.split_documents(documents)

vector_store = Chroma.from_documents(texts, embeddings, collection_metadata={"hnsw:space": "cosine"}, persist_directory="stores/db")

print("Векторная база создана!")


