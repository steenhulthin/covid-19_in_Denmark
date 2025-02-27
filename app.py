import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import datalayer as dl

st.set_page_config(page_title="Covid-19 Among Older People and Nursing Home Residents in Denmark", page_icon=":older_woman:", layout="wide", initial_sidebar_state="auto", menu_items={"Get Help": None, "Report a bug": "https://github.com/steenhulthin/covid-19_in_Denmark/issues", "About": "Written by Steen Hulthin Rasmussen. Data source: Statens Serum Institut"})

df = dl.get_confirmed_admitted_deceased_per_day_per_sex()
nursinghome_df = dl.get_plejehjemsdata()



# Title
st.title('Covid-19 in Denmark')
st.header('Focused on Older People and Nursing Home Residents')

# Sidebar
st.sidebar.header('Region')
selected_option = st.sidebar.selectbox('Select an option', df['Region'].unique())



query_text = f"Region == '{selected_option}'"
nursinghome_df['year_week'] = nursinghome_df['År'].astype(str) + '-w' + nursinghome_df['Uge'].astype(str)
nursinghome_df = nursinghome_df[nursinghome_df["År"] != "I alt"] # ugly hack to remove the total row for the rest of the  script

fig = go.Figure()

fig.add_trace(go.Scatter(x=nursinghome_df['year_week'], y=nursinghome_df[dl.get_testede_column_name()], mode='lines', name="🧪 " + dl.get_testede_column_name(), line=dict(color=dl.color_tested)))
fig.add_trace(go.Scatter(x=nursinghome_df['year_week'], y=nursinghome_df[dl.get_positive_column_name()], mode='lines', name= "🦠 " + dl.get_positive_column_name(), yaxis='y2', line=dict(color=dl.color_positive)))
fig.add_trace(go.Scatter(x=nursinghome_df['year_week'], y=nursinghome_df[dl.get_dead_column_name()], mode='lines', name="💀 " + dl.get_dead_column_name(), yaxis='y2', line=dict(color=dl.color_dead)))

fig.update_layout( 
    yaxis=dict(
        title='Antal tests 🧪', 
        tickfont=dict(color=dl.color_tested)
    ),
    yaxis2=dict(
        title='Antal positive/døde 🦠/💀',
        overlaying='y',
        side='right'
    ),
    title='Status for covid-19 på plejehjem over tid'
)

st.plotly_chart(fig)

# todo: handle division by zero
nursinghome_df['dead_positive_rate'] = nursinghome_df[dl.get_dead_column_name()] / nursinghome_df[dl.get_positive_column_name()]

st.line_chart(nursinghome_df[nursinghome_df["År"] != "I alt"], y=[ 'dead_positive_rate' ], x='year_week')

st.write('You selected:', selected_option)


st.line_chart(nursinghome_df[nursinghome_df["År"] != "I alt"], y=[dl.get_testede_column_name, dl.get_positive_column_name(), dl.get_dead_column_name()], x='year_week')

st.write(df.query(query_text))

st.line_chart(df[df["Region"] == selected_option], y=["Indlæggelser", "Døde"], x="Prøvetagningsdato")
st.line_chart(df[df["Region"] == selected_option], y=["Bekræftede tilfælde i alt"], x="Prøvetagningsdato")
