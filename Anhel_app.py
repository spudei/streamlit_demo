# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from datetime import datetime

st.title('Аналіз даних покупок в супермаркеті')

name = st.text_input(
    "Як вас звати?",
)
if name:
    st.write("Привіт, ", name, "!")


DATA_URL = ('https://docs.google.com/spreadsheets/d/e/2PACX-1vQf1s4z3C0iRAKOu6ClRTZbqN4ocTWoJX5KLynr7iB_ieK2bP5eZXmX7zyHBr9lmLud1ec4Ve71544L/pub?gid=335944704&single=true&output=csv')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data['Date'] = pd.to_datetime(data['Date'])
    return data

if st.checkbox('Завантажити дані'):
    data_load_state = st.text('Дані завантажуються...')
    data = load_data(10000)
    data_load_state.text("Готово! Дані вже завантажено!")

if st.checkbox('Показати чорнові дані'):
    st.subheader('Чорнові дані')
    min_row, max_row = st.slider("Оберіть, з якого по який рядочки даних ви хочете переглянути", 0, len(data) - 1,
                                 (0, len(data) - 1), key='key1')
    filtered_data = data.iloc[min_row:max_row + 1]
    st.write(filtered_data)

show_histograms = st.sidebar.checkbox('Показати гістограми', key='check1')

if show_histograms:
    column_names = ['Age', 'DISC', 'Amount', 'Net Bill Amount']
    selected_indicators = st.sidebar.multiselect(
        "Оберіть колонку для побудови гістограми", column_names, key='widget1'
        )
    if selected_indicators:
        for indicator in selected_indicators:
            fig = px.histogram(data, x = indicator)
            fig.update_traces(opacity=.4)  # аби встановити прозорість
            st.plotly_chart(fig)  # аби відобразити в стрімліті

average_data_checkbox = st.sidebar.checkbox('Показати cередні показники в динаміці за датою', key='check2')


if average_data_checkbox:
    min_date = data.Date.min().to_pydatetime()
    max_date = data.Date.max().to_pydatetime()
    default_date_range = (datetime(2016, 1, 1, 0, 0), max_date)
    date_slider = st.slider(
        "Оберіть часовий період, щоб переглянути дані?",
        min_value=min_date,
        max_value=max_date,
        value=default_date_range,
        key='key2')
    start_date, end_date = date_slider
    filtered_data2 = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    column_names2 = ['Age', 'DISC', 'Amount', 'Net Bill Amount']
    selected_indicators2 = st.sidebar.multiselect(
        "Оберіть колонку для побудови гістограми", column_names2, key='widget2'
    )
    if selected_indicators2:
        for indicator2 in selected_indicators2:
            average_data = filtered_data2.groupby('Date')[indicator2].mean()
            st.line_chart(average_data)
