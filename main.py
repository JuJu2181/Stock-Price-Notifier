# for backend
from flask import Flask, render_template, request 

from utils import *
from config import *

import asyncio 
import threading

app = Flask(__name__)



# main home page
@app.route('/')
def index():
    return render_template('index.html')

# endpoint for processing user input and adding subscription
@app.route("/add_subscription", methods=["POST"])
def add_subscription():
    # return request.form
    # get user input
    subscriber_email = request.form.get("subscriber-email")
    subscriber_number = request.form.get("subscriber-phone")
    stock_ticker_symbol = request.form.get("stock-ticker-symbol")
    price_threshold = request.form.get("price-threshold")
    frequency = request.form.get("frequency")
    notification_mode = request.form.get("notification-mode")
    # Some basic validation
    # validate email 
    if validate_email(subscriber_email) == False:
        return render_template("index.html",error="You have entered an invalid email address. Please enter a valid email address in format user@mail.com.")
    # validate phone number
    if validate_number(subscriber_number) == False:
        return render_template("index.html",error="You have entered an invalid phone number. Please enter a valid phone number in format +[Country_Code]-[10 Digit Number].")
    # validate stock ticker symbol
    if check_ticker_exists(stock_ticker_symbol) == False:
        return render_template("index.html",error="Stock ticker symbol you entered does not exist. Please enter a valid stock ticker symbol.")
    # validate price threshold
    if validate_price(price_threshold) == False:
        return render_template("index.html",error="You have entered an invalid price threshold. Please enter a valid price threshold")
    # add entry to database 
    # remove - before storing in database
    subscriber_number = subscriber_number.replace("-","")
    # convert price to float before storing in database
    price_threshold = float(price_threshold)
    # validating if the user already exists in the database
    try:
        add_user(subscriber_email, subscriber_number, stock_ticker_symbol, price_threshold, frequency, notification_mode)
    except:
        return render_template("index.html",error="You have already subscribed for this stock ticker symbol using this email/phone number. Please enter a different stock ticker symbol or a different email/phone number.")
    # fetch data based on user input
    try:
        currentPrice = fetch_data(stock_ticker_symbol)
    except:
        return render_template("index.html",error="There was an error fetching data. This may be due to poor internet connection")
    # Send notification for new entry
    try:
        send_notification(stock_ticker_symbol, price_threshold, currentPrice, subscriber_email, subscriber_number, frequency, notification_mode, "new_entry")
    except:
        return render_template("index.html",error="Entry was added to database, but error in sending notification. Please check your internet connection")

    all_subscribers = get_users("all")
    
    # result to display in success page
    result = {
        "Current Price": currentPrice,
        "threshold": price_threshold,
        "symbol": stock_ticker_symbol,
        "subscribers": all_subscribers
    }
    
    
    
    return render_template('success.html', result=result)
    

if __name__ == '__main__':
    t1 = threading.Thread(target=schedule_notification,name="Schedule Notifications")
    t1.start()
    app.run(debug=True)
