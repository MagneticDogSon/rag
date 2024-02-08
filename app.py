import os
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
import streamlit as st 

from langchain_community.llms import LlamaCpp
from huggingface_hub.file_download import http_get
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import MarkdownTextSplitter
from langchain import HuggingFacePipeline
import ingest as vb

from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import MarkdownTextSplitter

#######################################################

top_p = ()
top_k = ()
temp = ()
chunk_size = ()
chunk_overlap = ()

######################################################

def llm():
    prompt_template = """Ты — русскоязычный автоматический ассистент. 
    Ты разговариваешь с людьми и помогаешь им. 


    Context: {context}
    Question: {question}

    Отвечаешь точно и только то что есть в документе.

    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["question", "context"])

    embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

    load_vector_store = Chroma(persist_directory="stores/db", embedding_function=embeddings)

    retriever = load_vector_store.as_retriever(search_kwargs={"k":2})


    llm = LlamaCpp(model_path=".model/model-q4_K.gguf",
        temperature = temp,
        top_p=top_p,
        top_k=top_k,

        streaming =True,
        n_gpu_layers=100,
        n_batch=8,
        n_ctx=2000,
        n_parts=1,
        verbose=True
                    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
        verbose=True
        )
    return qa


