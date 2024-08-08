from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import time  # Добавлен импорт для времени
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
import yaml
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

client = QdrantClient(url="http://localhost:6333")


chunk_size = 600
chunk_overlap = 60

start_time1 = time.time()
# Загрузить документы
loader = DirectoryLoader('documents', glob="**/*.pdf", loader_cls=PyPDFLoader)
docs = loader.load_and_split()
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-large', show_progress=True,
                                    model_kwargs={'device': 'cuda'})

end_time1 = time.time()  # Завершить отсчет времени
print("==== Документы загружены ====")
print(f"\033[92mВремя исполнения: {end_time1 - start_time1:.2f} секунд\033[0m")

start_time2 = time.time()  # Начать отсчет времени
# Разделить документы на фрагменты
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
all_splits = text_splitter.split_documents(docs)






from langchain_qdrant import RetrievalMode

qdrant = QdrantVectorStore.from_documents(
    all_splits,
    embedding=embeddings,
    location="http://localhost:6333",
    collection_name="my_documents",
    retrieval_mode=RetrievalMode.DENSE,
)





def search():
    results = qdrant.similarity_search_with_score(
    "Кто такой дагон", k=3
    )

    for i in results:
        print(i[0].page_content)
        # aa = i[0].metadata.get("page")
        # print(f"{aa}")
        print(i[0].metadata)

if __name__ == "__main__":
    search()