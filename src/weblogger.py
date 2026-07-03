import logging
import webbrowser
from flask import Flask,render_template
from threading import Thread,Timer
import queue 
import datetime

class WebLogger:
    MAX_QUEUE = 2000
    _event_queue: queue.Queue = queue.Queue(maxsize=MAX_QUEUE)
    
    def __init__(self):
        self._app = Flask(__name__)
        self.define_route()
        self._start_logging()

    def define_route(self):
        @self._app.route("/")
        def index():
            #add in the HTML file
            return render_template("baseLog.html")
        

    def _start_logging(self,port: int = 5000, open_browser: bool = True):
        server_thread = Thread(
            target = lambda:self._app.run(
                host = "0.0.0.0",
                port = port,
                debug = False,
                use_reloader = False
            ),
            daemon=True
        ).start()

        if open_browser:
            Timer(
                1.0,
                lambda:webbrowser.open(f"http://localhost:{port}")
            ).start()


class LogHandler(logging.Handler):

    def emit(self,record:logging.LogRecord):
        logEntry = {
            "type" : "log",
            "time" : datetime.fromtimestamp(record.created).strftime("%H:%M:%S"),
            "level" : record.levelname,
            "logger" : record.name,
            "message" : self.format(record)
        }

