# This file will contain some utility functions that will be used in the main file
from config import *
# to send api requests to the web
import requests
# for sending emails 
import smtplib 
from email.mime.text import MIMEText
# for data analysis and processing
import pandas as pd
from datetime import datetime, timedelta
# for scheduling 
import schedule 
import time 
# for fetching data from yahoo finance
import yfinance as yf

# function to fetch data from api
def fetch_data_from_api(symbol="TSLA"):
    # API endpoint
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"
    # parameters for API
    region = "US"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    querystring = {"symbol": symbol, "region": region, "from": start_date, "to": end_date}
    # API headers
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    # API response
    response = requests.request("GET", url, headers=headers, params=querystring)
    # parse API response to json format
    data = response.json()
    # create a dataframe from the json response
    df = pd.DataFrame(data["prices"])
    # to convert from unix timestamp to date
    df["date"] = pd.to_datetime(df["date"], unit="s").dt.date
    # only keep the columns we need for price
    df_price = df[['date','open','high','low','close','volume']]
    # print(df_price.head())
    return df_price

# function to fetch data using yfinance
def fetch_data(symbol="TSLA"):
    msft = yf.Ticker(symbol)
    # getting ome price details from this response 
    prevClosingPrice = msft.info['previousClose']
    openPrice = msft.info['open']
    dayLowPrice = msft.info['dayLow']
    dayHighPrice = msft.info['dayHigh']
    currentPrice = msft.info['currentPrice']
    volume = msft.info['volume']
    # get all stock info
    result = {
        "prevClosingPrice": prevClosingPrice,
        "openPrice": openPrice,
        "dayLowPrice": dayLowPrice,
        "dayHighPrice": dayHighPrice,
        "currentPrice": currentPrice,
        "volume": volume,
    }
    # print(result)
    # returning only the current price for further processing
    return currentPrice
    
# function to send notification
def send_notification(symbol, threshold, currentPrice, subscriber_email, notification_mode="email"):
    # sender's email
    sender_mail = SENDER_MAIL
    sender_pwd = SENDER_PWD