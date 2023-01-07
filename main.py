import time
from datetime import datetime
import threading
import requests
from dotenv.main import load_dotenv
import os
import argparse


parser=argparse.ArgumentParser()

parser.add_argument("-p", "--path", help="Log file path to monitor.", required=True)
parser.add_argument("-mt", "--max_time", help="Max time in seconds to wait before send a message.", required=True)
parser.add_argument("-ph","--phrase", help="Phrase to monitor.", required=True)
args = parser.parse_args()

log_name = args.path
max_time = int(args.max_time)
phrase_to_monitor = args.phrase

load_dotenv()

def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line

logfile = open(log_name)
loglines = follow(logfile)

last_time_last_log = datetime.now()


def analyze_time(last_time_last_log):
    while True:
        delta = datetime.now() - last_time_last_log
        sec = delta.total_seconds()

        if sec > max_time:
            send_to_telegram(f'Se dejo de obtener logs con la frase {phrase_to_monitor} que se esta monitoreando.')
            break
        global stop_thread
        if stop_thread:
            break


def send_to_telegram(message):

    apiToken = os.environ['apiToken']
    chatID = os.environ['chatID']
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    except Exception as e:
        pass


stop_thread = False
for line in loglines:
    last_time_last_log = datetime.now()
    if not phrase_to_monitor.lower() in line.lower():
        stop_thread = False
        x = threading.Thread(target=analyze_time, args=(last_time_last_log,))    
        x.start()
    else:
        stop_thread = True

    
        
        
    


