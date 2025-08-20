import pandas as pd
from db import fetch_transactions

def export_to_excel(user_id, filename="data/finance_report.xlsx"):
    data = fetch_transactions(user_id)
    df = pd.DataFrame(data, columns=["id","user_id","type","category","amount","date"])
    df.to_excel(filename, index=False)
    return filename

def export_to_csv(user_id, filename="data/finance_report.csv"):
    data = fetch_transactions(user_id)
    df = pd.DataFrame(data, columns=["id","user_id","type","category","amount","date"])
    df.to_csv(filename, index=False)
    return filename
