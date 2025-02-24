import pandas as pd
import requests
from io import StringIO

def get_confirmed_admitted_deceased_per_day_per_sex():
    url = "https://steenhulthin.github.io/infectious-diseases-data/03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv"
    response = requests.get(url)

    if response.status_code == 200:
        data = StringIO(response.text)
        return pd.read_csv(data, delimiter=';')
    else:
        print("Failed to download CSV file. Status code:", response.status_code)
    return pd.DataFrame()
    
def get_plejehjemsdata():
    return pd.read_csv("https://steenhulthin.github.io/infectious-diseases-data/28_plejehjem_ugeoversigt.csv", delimiter=';')
