import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title('My Streamlit Dashboard')

# Sidebar
st.sidebar.header('User Input')
selected_option = st.sidebar.selectbox('Select an option', ['Option 1', 'Option 2'])

# Main Content
st.write('You selected:', selected_option)

         
# Slider
number = st.slider('Pick a number', 1, 10)
st.write('Selected number:', number)

# Chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)