# for backend
from flask import Flask

from utils import *
from routes import blueprint

import asyncio 
import threading

if __name__ == '__main__':
    # Background thread for sending notifications
    t1 = threading.Thread(target=schedule_notification,name="Schedule Notifications")
    t1.start()
    
    app = Flask(__name__)
    
    # Registering blue prints 
    app.register_blueprint(blueprint)
    app.run(host='127.0.0.1',port=2002,debug=True)
