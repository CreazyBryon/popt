from datetime import datetime
import logging
from . import gui_helper as pgui
from .http_helper import apost


def hud_emit(record):
    msg = record.getMessage()
    pgui.show_hud(msg)
    pgui.update_hud(msg)

def http_emit(record):
    msg1 = record.getMessage()
    #send async http request to server to log the message
    print(f"Sending log to server: {msg1}")
    #apost('http://localhost:3000/api/pop/logs', json_body ={'message': msg1}, timeout=60)
    #url = 'https://joofoo002.azurewebsites.net/api/pop/logs'
    url='http://localhost:3000/api/pop/logs'
    body = {
        'message': msg1,
        'time': datetime.now().isoformat().replace("+00:00", "Z")
    }

    apost(url, json_body=body, timeout=60)    
 


def setup_logging():
    print("Setting up logging configuration...")
    log_file = f"logs\\pop_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_format = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
    formatter = logging.Formatter(log_format)

    #file_handler = logging.FileHandler(log_file, encoding="utf-8")
    #file_handler.setLevel(logging.DEBUG)
    #file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    hud_handler = logging.Handler()
    hud_handler.setLevel(logging.ERROR)
    hud_handler.setFormatter(formatter)
    hud_handler.emit = hud_emit

    http_handler = logging.Handler()
    http_handler.setLevel(logging.CRITICAL)
    http_handler.setFormatter(formatter)
    http_handler.emit = http_emit

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    #logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(hud_handler)
    logger.addHandler(http_handler)