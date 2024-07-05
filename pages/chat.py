import streamlit as st
import yaml




with st.sidebar:

    st.title('Загрузка документа')
    st.file_uploader('', type = 'pdf')

    #with st.spinner ('Подождите...'):
    #    time.sleep (100)
    #st.success('Загружено!')

    st.divider()
    st.title('Настройки')

    st.title('Векторная база')
    chunk_size = st.slider('Размер фрагментов',0,1000,500)
    chunk_overlap = st.slider('Пересечение', 0, 500, 50)
    fragments_size = st.slider('Кол-во фрагментов для контекста', 0, 10, 3)
    st.divider()
    st.title('Модель')
    top_p = st.slider('Top-p, %', 0.0, 1.0, 0.15)
    top_k = st.slider('Top-k', 0, 10, 3)
    temp = st.slider('Temp', 0.0, 1.0, 0.1)
    st.divider()


    #запись в конфиг
    to_yaml = {}
    to_yaml['chunk_size'] = chunk_size
    to_yaml['chunk_overlap'] = chunk_overlap
    to_yaml['fragments_size'] = fragments_size
    to_yaml['top_p'] = top_p
    to_yaml['top_k'] = top_k
    to_yaml['temp'] = temp


    with open('conf.yaml', 'w') as f:
        yaml.dump(to_yaml, f)
        f.close()



st.title("АтомБот")
st.caption("Задай вопрос и я отвечу")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    prompt = st.chat_input("Задайте вопрос")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")

