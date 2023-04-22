# for backend
from flask import Flask, render_template, request 

from utils import *
from config import *

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
    # fetch data based on user input
    currentPrice = fetch_data(stock_ticker_symbol)
    # Send notification for new entry
    send_notification(stock_ticker_symbol, price_threshold, currentPrice, subscriber_email, subscriber_number, notification_mode, "new_entry")
    # check if the current price is greater than the threshold price
    if currentPrice > float(price_threshold):
        # send notification
        send_notification(stock_ticker_symbol, price_threshold, currentPrice, subscriber_email, subscriber_number, notification_mode, "price_update")
    result = {
        "Current Price": currentPrice,
        "threshold": price_threshold,
        "symbol": stock_ticker_symbol,
    }
    
    return render_template('success.html', result=result)
    

if __name__ == '__main__':
    app.run(debug=True)
