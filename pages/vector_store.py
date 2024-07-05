import streamlit as st
import yaml




st.set_page_config(page_title='Настройки', page_icon=None, layout="wide", initial_sidebar_state="collapsed")



# Извлечение парметров из конфига
with open('config.yaml', "r") as f:
    conf = yaml.safe_load(f)
    f.close()

chunk_overlap = int(conf["chunk_overlap"])
chunk_size = int(conf["chunk_size"])
fragments_size = int(conf["fragments_size"])
temp = float(conf["temp"])
top_k = int(conf["top_k"])
top_p = float(conf["top_p"])

###############НАСТРОЙКИ##########################

st.title('Настройки')
st.divider()


col1, col2, col3 = st.columns([3,1,3])
with col1:
    with st.container(border=False):
        st.title('Векторная база')
        chunk_size_new = st.slider('Размер фрагментов', 0, 1000, chunk_size, step=100, help="Кол-во токенов для одного фрагмента")
        chunk_overlap_new = st.slider('Пересечение', 0, 500, chunk_overlap, step=50, help="Кол-во токенов для перекрытия фрагмента")
        fragments_size_new = st.slider('Кол-во фрагментов для контекста', 0, 10, fragments_size, help="Кол-во фрагментов для контекстного окна LLM")
        st.divider()

        st.button("Создать векторную базу", type="primary", on_click=None)
with col2:
    with st.container(border=False):
        st.write('')

with col3:
    with st.container(border=False):
        st.title('Модель')
        top_p_new = st.slider('Top-p', 0.0, 1.0, top_p, step=0.1, help="Контролирует разнообразие сгенерированного текста, рассматривая только токены с наибольшей массой вероятности")
        top_k_new = st.slider('Top-k', 0, 10, top_k, step=1, help="Выбирает токены с наибольшей вероятностью до тех пор, пока не будет достигнуто указанное количество токенов")
        temp_new = st.slider('Temp', 0.0, 1.0, temp, step=0.1, help="Чем ниже значение температуры , тем более детерминированными будут результаты в смысле того, что будет выбран самый вероятный следующий токен")
        st.divider()

        st.button("Перезагрузить модель", type="primary", on_click=None)



#запись в конфиг
to_yaml = {}
to_yaml['chunk_size'] = chunk_size_new
to_yaml['chunk_overlap'] = chunk_overlap_new
to_yaml['fragments_size'] = fragments_size_new
to_yaml['top_p'] = top_p_new
to_yaml['top_k'] = top_k_new
to_yaml['temp'] = temp_new


with open('config.yaml', 'w') as f:
    yaml.dump(to_yaml, f)
    f.close()


