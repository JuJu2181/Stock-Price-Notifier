# For creating database for subscription entries and intializing it with some values
import sqlite3

connection = sqlite3.connect('database.db')

# Read schema
with open('schema.sql') as f:
    connection.executescript(f.read())
    
cur = connection.cursor()

# # Insert values
# cur.execute("INSERT INTO subscribers (email,phone_number,symbol,threshold,frequency,notification_mode) VALUES (?,?,?,?,?,?)", ("anishshilpakar8@gmail.com",9861028287,"META",100,"minutely","email"))

# cur.execute("INSERT INTO subscribers (email,phone_number,symbol,threshold,frequency,notification_mode) VALUES (?,?,?,?,?,?)", ("azayn.cilpakar@gmail.com",9861028287,"TSLA",200,"hourly","text-msg"))
            
connection.commit()
connection.close()