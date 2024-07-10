import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

import yaml


#----------------------

chunks_rag = ""

#----------------------

with open('config.yaml', "r") as f:
    conf = yaml.safe_load(f)
    f.close()

temp = float(conf["temp"])
top_k = int(conf["top_k"])
top_p = float(conf["top_p"])

# app config
st.set_page_config(page_title="АтомБот", page_icon="🤖")
st.title("АтомБот")


def get_response(user_query, chat_history, chunks_rag):

    template = """
    
    {chunks_rag}
    
    "You are an assistant for question-answering tasks. Use "
    "the following pieces of retrieved context to answer the "
    "question. If you don't know the answer, just say that you "
    "don't know. Use three sentences maximum and keep the answer "
    "concise."
    "\n\n"

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm =ChatOllama(model="llama3", temp=temp, top_p=top_p, top_k=top_k)

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
        "chunks_rag": chunks_rag,
    })


# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Чем могу помочь?"),
    ]

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Напишите запрос...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history, chunks_rag))

    st.session_state.chat_history.append(AIMessage(content=response))