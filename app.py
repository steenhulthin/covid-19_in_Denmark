import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datalayer as dl

df = dl.get_confirmed_admitted_deceased_per_day_per_sex()

# Title
st.title('Covid-19 Dashboard')

# Sidebar
st.sidebar.header('User Input')
selected_option = st.sidebar.selectbox('Select an option', ['Option 1', 'Option 2'])

# Main Content
st.write('You selected:', selected_option)

st.write(df)

# Slider
number = st.slider('Pick a number', 1, 10)
st.write('Selected number:', number)

# Chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)