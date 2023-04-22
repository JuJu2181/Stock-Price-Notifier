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
# for twilio 
from twilio.rest import Client

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
def send_mail(symbol, threshold, currentPrice, subscriber_email,email_type="price_update"):
    # sender's email
    sender = SENDER_MAIL
    # receiver's email
    recipients = [subscriber_email]
    # Email Content 
    if email_type == "price_update":
        subject = f"Stock Price Alert for {symbol}"
        body = f"""
        <h2> Notification for {symbol} </h2>
        <p>Current Price of {symbol} is {currentPrice}. It has crossed the threshold value of {threshold} set by you.</p>
        <br>
        This is the Way ✌🏻🕊️
        """
    elif email_type == "new_entry":
        subject = f"Subscription Added for {symbol}"
        body = f"""
        <p>Dear Customer, you have successfully added subscription for {symbol}. Your current price threshold is {threshold}. You will get notified if the current price exceeds this threshold.</p>
        <br>
        This is the Way ✌🏻🕊️
        """
    # using MIME on body to send html content
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    # for sending to multiple recipients
    msg['To'] = ', '.join(recipients)
    # Setup SMTP server 
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(SENDER_MAIL,SENDER_PWD)
    smtp_server.sendmail(sender,recipients,msg.as_string())
    smtp_server.quit()
    print(f"Email sent successfully to {subscriber_email}")
    
# function to send message
def send_message(symbol, threshold, currentPrice, subscriber_number,msg_type="price_update"):
    # set up twilio api
    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    # message when price is updated and exceeds threshold
    if msg_type == "price_update":
        message = client.messages.create(
            from_=TWILIO_NUMBER,
            body=f"Current Price of {symbol} is {currentPrice}. It has crossed the threshold value of {threshold} set by you.\n~ This is the Way",
            to='+977'+subscriber_number  
        )
    # Default message when user adds new entry
    elif msg_type == "new_entry":
        message = client.messages.create(
            from_=TWILIO_NUMBER,
            body=f"Dear Customer, you have successfully added subscription for {symbol}. Your current price threshold is {threshold}. You will get notified if the current price exceeds this threshold.\n~ This is the Way",
            to='+977'+subscriber_number  
        )
    print(f"Message sent successfully to {subscriber_number}")

# function to send notification
def send_notification(symbol,threshold,currentPrice,subscriber_email,subscriber_number,notification_mode="email",notification_type="price_update"):
    if notification_mode == "email":
        # send email for new entry
        send_mail(symbol,threshold,currentPrice,subscriber_email,notification_type)
    elif notification_mode == "text-msg":
        # send message for new entry
        send_message(symbol,threshold,currentPrice,subscriber_number,notification_type)


# def schedule(frequency):
#     if frequency == "minutely":
#         schedule.every(1).minutes.do(main)
    