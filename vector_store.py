import streamlit as st
import yaml
from ingestion import create_vector_store
import ollama

st.set_page_config(page_title='Настройки', page_icon=None, layout="wide", initial_sidebar_state="collapsed")

# Извлечение парметров из конфига
with open('./config.yaml', "r") as f:
    conf = yaml.safe_load(f)
    f.close()

collection_name = str(conf["collection_name"])
path_files = str(conf["path_files"])
chunk_overlap = int(conf["chunk_overlap"])
chunk_size = int(conf["chunk_size"])
sep = str(conf["sep"])
embeding = str(conf["embeding"])

temp = float(conf["temp"])
top_k = int(conf["top_k"])
top_p = float(conf["top_p"])
model = str(conf["model"])

search = str(conf["search"])
k = int(conf["k"])
score_threshold = float(conf["score_threshold"])
fetch_k = int(conf["fetch_k"])
lambda_mult = float(conf["lambda_mult"])

###############НАСТРОЙКИ##########################

st.title('Настройки')
st.divider()

col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    with st.container(border=False):
        st.title('Векторная база')

        path_files_new = st.text_input("Папка с файлами:")

        collection_name_new = st.text_input("Имя коллекции:")

        chunk_size_new = st.slider('Размер фрагментов:', 0, 1000, chunk_size, step=100,
                                   help="Кол-во токенов для одного фрагмента")
        chunk_overlap_new = st.slider('Пересечение фрагментов:', 0, 500, chunk_overlap, step=50,
                                      help="Кол-во токенов для перекрытия фрагмента")

        separator_new = st.selectbox("Метод разбитиия фрагментов:",
                                     ("RecursiveCharacterTextSplitter",
                                      "CharacterTextSplitter",
                                      "SentenceTransformersTokenTextSplitter",
                                      "TokenTextSplitter"))

        embeding_new = st.selectbox("Модель встраивания:", ("BAAI/bge-m3", "Embeding_2"))

        if st.button("Создать векторную базу", type="primary"):
            with st.spinner(""):
                st.toast("Создание векторной базы данных....", icon="❌")
                create_vector_store()
                st.toast("Создание векторной базы данных завершено", icon="🔥")

with col2:
    with st.container(border=False):
        st.write("")

with col3:
    with st.container(border=False):
        st.title('Поиск по векторной базе')

        search_new = st.selectbox("Алгоритм поиска", ("similarity", "mmr", "similarity_score_threshold", ""))

        if search_new == "similarity":
            fetch_k_new_disable = True
            score_threshold_disable = True
            lambda_mult_new_disabled = True

        if search_new == "mmr":
            fetch_k_new_disable = True
            score_threshold_disable = False
            lambda_mult_new_disabled = True

        if search_new == "similarity_score_threshold":
            fetch_k_new_disable = False
            score_threshold_disable = True
            lambda_mult_new_disabled = False

        k_new = st.slider('Кол-во фрагментов для контекстного окна:', 0, 10, k, step=1,
                          help="Кол-во фрагментов для контекстного окна LLM")

        score_threshold = st.slider('Минимальный порог сходства:', 0.0, 1.0, score_threshold, step=0.1,
                                    help=" Минимальный порог сходства фрагментов с запросом",
                                    disabled=score_threshold_disable)

        fetch_k_new = st.slider('fetch_k:', 0, 20, fetch_k, step=1,
                                help="",
                                disabled=fetch_k_new_disable, )

        lambda_mult_new = st.slider('lambda_mult:', 0.0, 1.0, lambda_mult, step=0.1,
                                    help="",
                                    disabled=lambda_mult_new_disabled)

col4, col5, col6 = st.columns([2, 1, 2])
with col4:
    with st.container(border=False):
        st.divider()
        st.title('Модель')

        # model_new = st.selectbox("Модель", ("llama3.1", "gemma2:2b", "mistral-nemo"))

        models = [m['name'] for m in ollama.list()["models"]]

        index = models.index("llama3.1:latest")

        model_new = st.selectbox("Модель", options=models, index=index)

        top_p_new = st.slider('Top-p:', 0.0, 1.0, top_p, step=0.1,
                              help="Контролирует разнообразие сгенерированного текста, рассматривая только токены с наибольшей массой вероятности")
        top_k_new = st.slider('Top-k:', 0, 10, top_k, step=1,
                              help="Выбирает токены с наибольшей вероятностью до тех пор, пока не будет достигнуто указанное количество токенов")
        temp_new = st.slider('Temp:', 0.0, 1.0, temp, step=0.1,
                             help="Чем ниже значение температуры , тем более детерминированными будут результаты в смысле того, что будет выбран самый вероятный следующий токен")

        st.button("Перезагрузить модель", type="primary", on_click=None)

with col5:
    with st.container(border=False):
        st.write("")

with col6:
    with st.container(border=False):
        st.write("")

# запись в конфиг
to_yaml = {}
to_yaml['path_files'] = path_files
to_yaml['collection_name'] = collection_name
to_yaml['chunk_size'] = chunk_size_new
to_yaml['chunk_overlap'] = chunk_overlap_new
to_yaml['sep'] = separator_new
to_yaml['embeding'] = embeding_new

to_yaml['top_p'] = top_p_new
to_yaml['top_k'] = top_k_new
to_yaml['temp'] = temp_new
to_yaml['model'] = model_new

to_yaml['search'] = search_new
to_yaml["k"] = k_new
to_yaml["score_threshold"] = score_threshold
to_yaml["fetch_k"] = fetch_k
to_yaml["lambda_mult"] = lambda_mult

with open('config.yaml', 'w') as f:
    yaml.dump(to_yaml, f)
    f.close()
