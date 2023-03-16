import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt


def upload_csv():        
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        data = uploaded_file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(data))
        return st.dataframe(df)

df = st.button("업로드", on_click=upload_csv)

