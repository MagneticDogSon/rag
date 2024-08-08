from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_ollama import ChatOllama
import streamlit as st
import pandas as pd
import time
import torch
from langchain_core.prompts import ChatPromptTemplate

import streamlit_shadcn_ui as ui






start_time = time.time()


st.set_page_config(page_title="АтомБот", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

loader = DirectoryLoader('documents', glob="**/*.pdf", loader_cls=PyPDFLoader)

dataset = {}


st.title("⚛️ Vega v0.1")
st.write("")

docs = loader.load()
device = 'cuda' if torch.cuda.is_available() else 'cpu'
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-large', model_kwargs={'device': device})


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
db = Chroma(persist_directory="./.chroma", embedding_function=embeddings, collection_name="rag-chroma")



# Retrieve and generate using the relevant snippets of the blog.
retriever = db.as_retriever(search_kwargs={"k": 4}, model_kwargs={'device': device})



template = """
human:

You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:

"""

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOllama(model="llama3.1", temperature=0)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# a = rag_chain.invoke("кто такой дагон?")
#
# print(a)
user_query = ("Кто такой ктулху?")
#user_query = st.chat_input("Напишите запрос...")
if user_query:

    with st.chat_message("Human"):
        st.write(user_query)


    with st.chat_message("AI"):
        with st.spinner(""):
            response = rag_chain.invoke(user_query)
            st.write(response)

            content = retriever.invoke(user_query)

            end_time = time.time()  # Завершить отсчет времени
            st.write(f"Время исполнения: {end_time - start_time:.2f} секунд")

        expander = st.expander("Форагменты:")
        for i in content:
            expander.write(content[0].page_content)
            meta = content[0].metadata["page"]
            source = content[0].metadata["source"]

            expander.markdown(f":green-background[Страница:{meta}]")
            expander.markdown(f":blue-background[Документ:{source}]")
            expander.write("-----------------------")
# датафрейм

dataset["question"] = [f'{user_query}']
dataset["answer"] = [f'{response}']
df = pd.DataFrame.from_dict(dataset)
df.to_csv('dataset/dataset.csv', mode='a', index=False, header=True)


