## Task Description
You are tasked with building a web application that allows users to receive notifications when the price of a given stock reaches a certain threshold. The application should allow users to enter a stock ticker symbol and a price threshold, and it should send a notification (e.g. an email or a text message) to the user when the stock's price reaches or exceeds the threshold.
To build this application, you will need to use the [Yahoo Finance API](https:/finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC) to retrieve stock market data.
In addition to the above requirements, your application should also have the following features:
- A feature that allows users to specify the frequency at which the stock's price should be checked (e.g. every hour, every day, etc.)
- A feature that allows users to specify the type of notification they would like to receive (e.g. email, text message, etc.)
To complete this challenge, you should create a web application using Python and the Flask web framework. The application should have a user-friendly interface and should be able to retrieve and process the required stock data in a clear and concise manner. 


### User Inputs
- Stock ticker symbol i-e symbol of company like META etc
- Price threshold 
- Frequency at which stock price should be checked
    - May be a radio button with options hour and day
- Users can specify type of notification
    - Another radio button for email and text message

### Main feature
- When Stock price exceeds the user's threshold send an email notification to user 
- SMTP may be used for email, Twillio for SMS

### Tools To be used
- Python
- Flask (backend)
- HTML, CSS, JS for Frontend 
- yfinance for api data