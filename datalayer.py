import pandas as pd

def get_confirmed_admitted_deceased_per_day_per_sex():
    return pd.read_csv(r'./data/03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv', delimiter=';')