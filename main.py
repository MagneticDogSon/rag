import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.session_state()

st.set_page_config(page_title='AI', page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)


col1, col2, col3 = st.columns([1,1,1])
with col1:
    with st.container(border=False):
        st.write("")

with col2:
    with st.container(border=False):
        st.image('img/ra.png')
with col3:
    with st.container(border=False):
        st.write("")


#st.markdown("<h1 style='text-align: center; color: white;'>AI</h1>", unsafe_allow_html=True)

input = st.text_input("", key="text", placeholder="Поиск")

col4, col5, col6 = st.columns([1,1,1])


# примеры
a = "К какому классу безопасности по НП-001 относится вентсистема В-31 зд. 401"
b = "К какому классу безопасности по НП-001 относится вентсистема В-31 зд. 401"
c = "К какому классу безопасности по НП-001 относится вентсистема В-31 зд. 401"


with col4:
    with st.container(border=False):
        st.button(label=a, key="primer1")
with col5:
    with st.container(border=False):
        st.button(label=b, key="primer2")
with col6:
    with st.container(border=False):
        st.button(label=c, key="primer3")



st.session_state['Text'] = "text"
if st.session_state["primer1"] == True:
    st.session_state['Text'] = a
    switch_page("app2")

if st.session_state["primer2"] == True:
    st.session_state['Text'] = b
    switch_page("app2")

if st.session_state["primer3"] == True:
    st.session_state['Text'] = c
    switch_page("app2")


#st.write(st.session_state)


if input:
    st.session_state['Text'] = st.session_state['text']
    switch_page ("app2")


