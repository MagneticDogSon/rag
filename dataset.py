import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui


st.title("Датасет")

df = pd.read_csv('dataset.csv')
ui.table(data=df, maxHeight=300)
st.table(df)