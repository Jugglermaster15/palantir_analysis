import yfinance as yf
import pandas as pd
import schedule
import time

def update_data():
    # Fetch data
    pltr = yf.Ticker("PLTR")
    historical_data = pltr.history(period="max")
    financials = pltr.financials
    balance_sheet = pltr.balance_sheet
    cash_flow = pltr.cashflow

    # Save data to CSV
    historical_data.to_csv("historical_data.csv")
    financials.to_csv("financials.csv")
    balance_sheet.to_csv("balance_sheet.csv")
    cash_flow.to_csv("cash_flow.csv")
    print("Data updated at:", time.ctime())

# Schedule updates daily at 9:00 AM
schedule.every().day.at("09:00").do(update_data)

while True:
    schedule.run_pending()
    time.sleep(1)
