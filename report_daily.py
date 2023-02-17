from datetime import datetime
import pandas as pd

def report_sale_amount():
    """making sale amount daily report from csv"""
    convert_month = {"1": "January",
"2":"February" }
    today = datetime.now()
    df = pd.read_excel(f"data/sales_data/{today.year}/{convert_month[str(today.month)]}.xlsx")
    pivote = pd.pivot_table(df,index="transaction_date",columns="store",values="amount",
    aggfunc="sum",margins=True,margins_name="Total")
    pivote.to_csv(f"export/sales_amount_function_{today.year}_{today.month}_{today.day}.csv")
