import streamlit as st
import pandas as pd


st.set_page_config(page_title='AI', page_icon=None, layout="wide", initial_sidebar_state="collapsed")




#with st.sidebar:
    #st.sidebar.page_link("app2.py", label="Chat")
    #st.sidebar.page_link("app2.py", label="About")


st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
         

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: left;
        } 
    </style>
    """,unsafe_allow_html=True
)

# Первая колонка (ПОИСК)
col3, col4, col5 = st.columns([1,3,1])

with col3:
    with st.container(border=False):
        st.write('')
        st.write('')
        st.write('AI Generator')

with col4:
    with st.container(border=False):
        st.text_input("", placeholder='Поиск')

with col5:
    with st.container(border=False):
        st.write('')


# Вторая колонка (САМАРИ, ИСТОЧНИКИ, РЕЗУЛЬТАТЫ, ЧАТ)
col1, col2 = st.columns([3,1])

# САМАРИ
with col1:
    with st.container(border=True, height=600):
        st.markdown(":blue[AI Summary]")
        st.write(st.session_state["Text"])



        st.divider()
        st.markdown(":blue[Источники:]")
        col6, col7, col8, col9, col10 = st.columns([1, 1, 1, 1, 1])
        with col6:
            st.info("[НП-001-15.pdf](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")

        with col7:
            st.info("[НП-001-15.pdf](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")

        with col8:
            st.info("[НП-001-15.pdf](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")

        with col9:
            st.info("[НП-001-15.pdf](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")

        with col10:
            st.info("[НП-001-15.pdf](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")



        st.divider()
        st.markdown(":blue[Результаты:]")
        col4, col5 = st.columns([1, 1])
        with col4:
            st.write ("Документ")
            st.write("НП-001-15.pdf")
            st.write("НП-001-15.pdf")
            st.write("НП-001-15.pdf")
            st.write("НП-001-15.pdf")
        with col5:
            st.write("Процент совпадения, %")
            st.write("90%")

st.chat_input()

# ЧАТ
with col2:
    with st.container(border=True,height=600):
        st.header("")


        with st.container(border=False, height=100):
            if "messages" not in st.session_state:
                st.session_state["messages"] = [{"role": "assistant", "content": "Чем я могу помочь?"}]
                st.session_state["messages"] = [{"role": "user", "content": "К какому классу безопасности по НП-001 относится вентсистема В-31 зд. 401"}]




            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])



st.write(
    """
       
       <style>
   
   
           section[data-testid="stSidebar"] {
               width: 10px !important; # Set the width to your desired value
           }
       </style>
       """,
    unsafe_allow_html=True,
)