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
# for database 
import sqlite3
# for regex
import re 

##################################### 
##   Data ingestion Functions      ##
#####################################
# function to fetch data from api (Optional)
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

# function to fetch data using yfinance (I used this)
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
    
##################################### 
##         Validation Functions    ##
#####################################

# function to check if the ticker exists or not
def check_ticker_exists(symbol):
    try:
        msft = yf.Ticker(symbol)
        data = msft.info
        return True
    except:
        return False 
    
# To validate if the email exists or not
def validate_email(email):
    # Email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if email matches pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False
    
# To validate if the phone number exists or not
def validate_number(number):
    # Phone number regex pattern
    phone_number_pattern = r'^\+\d{1,3}\d{10}$'

    # Check if phone number matches pattern
    if re.match(phone_number_pattern, number):
        return True
    else:
        return False
    
# To validate if the price is valid number or not
def validate_price(price):
    try:
        price = float(price)
        return True 
    except:
        return False
    
##################################### 
##         Email/Text Messaging    ##
#####################################

# function to send email
def send_mail(symbol, threshold, currentPrice, subscriber_email, frequency, email_type="price_update"):
    try:
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
            <p>Dear Customer, you have successfully added {frequency} subscription for {symbol}. Your current price threshold is {threshold}. You will get notified if the current price exceeds this threshold.</p>
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
    except Exception as e:
        print(f"Error sending email to {subscriber_email}")
        print(f"Following Exception Occured: ")
        print(e)
    
# function to send message
def send_message(symbol, threshold, currentPrice, subscriber_number,frequency,msg_type="price_update"):
    try:
        # set up twilio api
        client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
        # message when price is updated and exceeds threshold
        if msg_type == "price_update":
            message = client.messages.create(
                from_=TWILIO_NUMBER,
                body=f"Current Price of {symbol} is {currentPrice}. It has crossed the threshold value of {threshold} set by you.\n~ This is the Way",
                to=subscriber_number  
            )
        # Default message when user adds new entry
        elif msg_type == "new_entry":
            message = client.messages.create(
                from_=TWILIO_NUMBER,
                body=f"Dear Customer, you have successfully added {frequency} subscription for {symbol}. Your current price threshold is {threshold}. You will get notified if the current price exceeds this threshold.\n~ This is the Way",
                to=subscriber_number  
            )
        print(f"Message sent successfully to {subscriber_number}")
    except Exception as e:
        print(f"Error sending email to {subscriber_number}")
        print(f"Following Exception Occured: ")
        print(e)

# function to send notification
def send_notification(symbol,threshold,currentPrice,subscriber_email,subscriber_number,frequency,notification_mode="email",notification_type="price_update"):
    if notification_mode == "email":
        # send email for new entry
        send_mail(symbol,threshold,currentPrice,subscriber_email,frequency,notification_type)
    elif notification_mode == "text-msg":
        # send message for new entry
        send_message(symbol,threshold,currentPrice,subscriber_number,frequency,notification_type)


##################################### 
##         DATABASE Functions      ##
#####################################

# connecting to database 
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# add new user to database
def add_user(email,phone_number,symbol,threshold,frequency,notification_mode):
    conn = get_db_connection()
    conn.execute("INSERT INTO subscribers (email,phone_number,symbol,threshold,frequency,notification_mode) VALUES (?,?,?,?,?,?)", (email,phone_number,symbol,threshold,frequency,notification_mode))
    conn.commit()
    conn.close()
    print("New Subscriber Added")

# fetch all existing users from database
def get_users(subscribe_mode="minutely"):
    conn = get_db_connection() 
    all_subscribers = conn.execute('SELECT * FROM subscribers ORDER BY created DESC').fetchall()
    minutely_subscribers = conn.execute('SELECT * FROM subscribers WHERE frequency="minute"').fetchall()
    hourly_subscribers = conn.execute('SELECT * FROM subscribers WHERE frequency="hour"').fetchall()
    daily_subscribers = conn.execute('SELECT * FROM subscribers WHERE frequency="day"').fetchall()
    conn.close()
    print(f"There are {len(minutely_subscribers)} minutely subscribers currently")
    print(f"There are {len(hourly_subscribers)} hourly subscribers currently")
    print(f"There are {len(daily_subscribers)} daily subscribers currently")
    if subscribe_mode == "minutely":
        return minutely_subscribers
    elif subscribe_mode == "hourly":
        return hourly_subscribers
    elif subscribe_mode == "daily":
        return daily_subscribers
    elif subscribe_mode == "all":
        return all_subscribers


##################################### 
##SEND NOTIFICATIONS USING SCHEDULE##
#####################################

# notify the current subscribers
def notify_subscribers(subscribers):
    for subscriber in subscribers:
        currentPrice = fetch_data(subscriber['symbol'])
        if currentPrice > subscriber['threshold']:
            send_notification(subscriber['symbol'],subscriber['threshold'],currentPrice,subscriber['email'],subscriber['phone_number'],subscriber['frequency'],notification_mode=subscriber['notification_mode'],notification_type="price_update")
    print("Done")

# function to notify subscribers based on their frequency
def notify_minutely_subscriber():
    print("Notifying minutely subscriber at", datetime.now())
    minutely_subscribers = get_users("minutely")
    if len(minutely_subscribers) > 0:
        notify_subscribers(minutely_subscribers)
        print(f"Notified {len(minutely_subscribers)} subscribers")
    else:
        print("No minutely subscribers yet!")

# function to notify hourly subscriber
def notify_hourly_subscriber():
    print("Notifying hourly subscriber at", datetime.now())
    hourly_subscribers = get_users("hourly")
    if len(hourly_subscribers) > 0:
        notify_subscribers(hourly_subscribers)
        print(f"Notified {len(hourly_subscribers)} subscribers")
    else:
        print("No hourly subscribers yet!")

# function to notify daily subscriber
def notify_daily_subscriber():
    print("Notifying daily subscriber at", datetime.now())
    daily_subscribers = get_users("daily")
    if len(daily_subscribers) > 0:
        notify_subscribers(daily_subscribers)
        print(f"Notified {len(daily_subscribers)} subscribers")
    else:
        print("No daily subscribers yet!")

# for scheduling notification
def schedule_notification():
    schedule.every().minute.do(notify_minutely_subscriber)
    schedule.every(1).hour.do(notify_hourly_subscriber)
    schedule.every().day.at("08:00").do(notify_daily_subscriber)
    while True:
        schedule.run_pending()
        time.sleep(1)
    