# This file will contain some globally used constants and variables
import os
# For importing data from .env file
with open('.env', 'r') as f:
    for line in f:
        # Ignore empty lines and comments
        if not line.strip() or line.startswith('#'):
            continue

        # Split the line into key and value
        key, value = line.strip().split('=', 1)

        # Set the environment variable
        os.environ[key] = value

# imported data
RAPID_API_KEY = os.environ['RAPID_API_KEY']
RAPID_API_HOST = os.environ['RAPID_API_HOST']
SENDER_MAIL = os.environ['SENDER_MAIL']
SENDER_PWD = os.environ['SENDER_PWD']
TWILIO_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_PHONE_NUMBER']