import pandas as pd
import requests
from io import StringIO

def get_csv_data(url, backup_file_path=None):
    response = requests.get(url)

    if response.status_code == 200:
        data = StringIO(response.text)
        return pd.read_csv(data, delimiter=';')
    else:
        print("Failed to download CSV file. Status code:", response.status_code)
        if backup_file_path is None:
            print("No backup file path provided.")
            return pd.DataFrame()
        else:
            return pd.read_csv(backup_file_path, delimiter=';')

def get_confirmed_admitted_deceased_per_day_per_sex():
    return get_csv_data("https://steenhulthin.github.io/infectious-diseases-data/03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv", r'./data/03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv')
    
def get_plejehjemsdata():
    df = get_csv_data("https://steenhulthin.github.io/infectious-diseases-data/28_plejehjem_ugeoversigt.csv")
    df.__dict__["tested"] = "Antal tests blandt beboere"
    return df

def get_testede_column_name():
    return "Antal tests blandt beboere"

def get_positive_column_name():
    return "Bekræftede tilfælde beboere"

def get_dead_column_name():
    return "Dødsfald blandt bekræftede beboere"

color_tested = "limegreen"
color_positive = "teal"
color_admitted = "orangered"
color_dead = "crimson"

emoji_tested = "🧪"
emoji_positive = "🦠"
emoji_admitted = "🛌"
emoji_dead = "💀"