import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import datalayer as dl

df = dl.get_confirmed_admitted_deceased_per_day_per_sex()
plejehjem = dl.get_plejehjemsdata()

def get_testede_column_name():
    return "Antal tests blandt beboere"

def get_positive_column_name():
    return "Bekræftede tilfælde beboere"

def get_dead_column_name():
    return "Dødsfald blandt bekræftede beboere"

# Title
st.title('Covid-19 Dashboard for Denmark')

# Sidebar
st.sidebar.header('Region')
selected_option = st.sidebar.selectbox('Select an option', df['Region'].unique())

query_text = f"Region == '{selected_option}'"
plejehjem['year_week'] = plejehjem['År'].astype(str) + '-w' + plejehjem['Uge'].astype(str)
plejehjem = plejehjem[plejehjem["År"] != "I alt"] # ugly hack to remove the total row for the rest of the  script


fig = go.Figure()

# Add first trace (y-axis on the left)
fig.add_trace(go.Scatter(x=plejehjem['year_week'], y=plejehjem[get_testede_column_name()], mode='lines', name=get_testede_column_name()))

# Add second trace (y-axis on the right)
fig.add_trace(go.Scatter(x=plejehjem['year_week'], y=plejehjem[get_positive_column_name()], mode='lines', name=get_positive_column_name(), yaxis='y2'))
fig.add_trace(go.Scatter(x=plejehjem['year_week'], y=plejehjem[get_dead_column_name()], mode='lines', name="💀 " + get_dead_column_name(), yaxis='y2'))

# Create second y-axis on the right
fig.update_layout(
    yaxis2=dict(
        title='positive/døde',
        overlaying='y',
        side='right'
    ),
    title='Status for covid-19 på plejehjem over tid'
)

st.plotly_chart(fig)

st.write('You selected:', selected_option)


st.line_chart(plejehjem[plejehjem["År"] != "I alt"], y=[get_testede_column_name(), get_positive_column_name(), get_dead_column_name()], x="year_week")

st.write(df.query(query_text))

st.line_chart(df[df["Region"] == selected_option], y=["Indlæggelser", "Døde"], x="Prøvetagningsdato")
st.line_chart(df[df["Region"] == selected_option], y=["Bekræftede tilfælde i alt"], x="Prøvetagningsdato")
