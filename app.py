import streamlit as st
import pandas as pd
import numpy as np

import datalayer as dl

df = dl.get_confirmed_admitted_deceased_per_day_per_sex()
plejehjem = dl.get_plejehjemsdata()

# Title
st.title('Covid-19 Dashboard for Denmark')

# Sidebar
st.sidebar.header('Region')
selected_option = st.sidebar.selectbox('Select an option', df['Region'].unique())

# Main Content
st.write('You selected:', selected_option)

query_text = f"Region == '{selected_option}'"

st.write(df.query(query_text))

st.line_chart(df[df["Region"] == selected_option], y=["Indlæggelser", "Døde"], x="Prøvetagningsdato")
st.line_chart(df[df["Region"] == selected_option], y=["Bekræftede tilfælde i alt"], x="Prøvetagningsdato")

st.write('---')

plejehjem['year_week'] = plejehjem['År'].astype(str) + '-w' + plejehjem['Uge'].astype(str)

st.line_chart(plejehjem[plejehjem["År"] != "I alt"], y=["Antal tests blandt beboere", "Bekræftede tilfælde beboere", "Dødsfald blandt bekræftede beboere"], x="year_week")