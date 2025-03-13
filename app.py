import streamlit as st
import plotly.graph_objects as go
from webcolors import name_to_rgb

import datalayer as dl

st.set_page_config(
    page_title="Covid-19 Among Older People and Nursing Home Residents in Denmark", 
    page_icon=":older_woman:", 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items={"Get Help": None, 
                "Report a bug": "https://github.com/steenhulthin/covid-19_in_Denmark/issues", 
                "About": "Written by Steen Hulthin Rasmussen. Data source: Statens Serum Institut"})

df = dl.get_confirmed_admitted_deceased_per_day_per_sex()
nursinghome_df = dl.get_plejehjemsdata()



# Title
st.title('Covid-19 in Denmark')
st.header('Focused on Older People and Nursing Home Residents')

# Sidebar
st.sidebar.header('Region')
selected_option = st.sidebar.selectbox('Select an option', df['Region'].unique())



query_text = f"Region == '{selected_option}'"
year_week_column_name = 'year_week'
nursinghome_df[year_week_column_name] = nursinghome_df['År'].astype(str) + '-w' + nursinghome_df['Uge'].astype(str)
nursinghome_df = nursinghome_df[nursinghome_df["År"] != "I alt"] # ugly hack to remove the total row for the rest of the  script

fig = go.Figure()

fig.add_trace(go.Scatter(x=nursinghome_df[year_week_column_name], 
                         y=nursinghome_df[dl.get_testede_column_name()], 
                         mode='lines', 
                         name="🧪 " + dl.get_testede_column_name(), 
                         line=dict(color=dl.color_tested)))
fig.add_trace(go.Scatter(x=nursinghome_df[year_week_column_name], 
                         y=nursinghome_df[dl.get_positive_column_name()], 
                         mode='lines', 
                         name= "🦠 " + dl.get_positive_column_name(), 
                         yaxis='y2', 
                         line=dict(color=dl.color_positive)))
fig.add_trace(go.Scatter(x=nursinghome_df[year_week_column_name], 
                         y=nursinghome_df[dl.get_dead_column_name()], 
                         mode='lines', 
                         name="💀 " + dl.get_dead_column_name(), 
                         yaxis='y2', 
                         line=dict(color=dl.color_dead)))

fig.update_layout( 
    yaxis=dict(
        title='Antal tests 🧪', 
        tickfont=dict(color=dl.color_tested)
    ),
    yaxis2=dict(
        title='Antal positive/døde 🦠/💀',
        tickfont=dict(color=dl.color_dead),
        overlaying='y',
        side='right'
    ),
    title='Status for covid-19 på plejehjem over tid'
)

st.plotly_chart(fig)


dead_pos_rate_column_name = 'dead_positive_rate'
pos_tested_rate_column_name = 'positive_tested_rate'

nursinghome_df[dead_pos_rate_column_name] = nursinghome_df[dl.get_dead_column_name()] / (nursinghome_df[dl.get_positive_column_name()] + 1) # the + 1 is to avoid division by zero
nursinghome_df[pos_tested_rate_column_name] = nursinghome_df[dl.get_positive_column_name()] / (nursinghome_df[dl.get_testede_column_name()] + 1) # the + 1 is to avoid division by zero

st.line_chart(nursinghome_df[nursinghome_df["År"] != "I alt"], 
              y=[ dead_pos_rate_column_name, pos_tested_rate_column_name ], 
              x=year_week_column_name)

st.write("Age groups")

df_groups = dl.get_age_group_data()
st.bar_chart(df_groups[df_groups["Region_x"] == selected_option], 
             y=["Bekræftede tilfælde i alt", "Indlæggelser", "Døde"], 
             x="Aldersgruppe", 
             color=[name_to_rgb(dl.color_positive), name_to_rgb(dl.color_admitted), name_to_rgb(dl.color_dead)])
