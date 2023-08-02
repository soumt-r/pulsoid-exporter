import threading
import prometheus_client
from prometheus_client import start_http_server, Gauge
import time
import os
import websocket
import json

# parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="name of the metric", default=os.environ.get("METRIC_NAME", "user1"))
parser.add_argument("-p", "--port", help="port of the metric", default=int(os.environ.get("METRIC_PORT", 8000)))
parser.add_argument("-u", "--url", help="url of the heart rate data (pulsoid)", default=os.environ.get("METRIC_HR_URL", "none"))
parser.add_argument("-t", "--timeout", help="timeout of the metric", default=int(os.environ.get("METRIC_TIMEOUT", 5)))
args = parser.parse_args()

METRIC_NAME = args.name
METRIC_PORT = args.port
METRIC_HR_URL = args.url
METRIC_TIMEOUT = args.timeout

if METRIC_HR_URL == "none":
    print("METRIC_HR_URL is not set")
    exit(1)

prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)

HR_GAUGE = Gauge('heart_rate', 'Heart Rate', ["name"])
LAST_UPDATE = time.time()

HR_GAUGE.labels(METRIC_NAME)

def on_message(ws, message):
    global LAST_UPDATE
    data = json.loads(message)
    if "data" in data:
        now_hr = data["data"]["heartRate"]
        HR_GAUGE.labels(METRIC_NAME).set(now_hr)
        LAST_UPDATE = time.time()

def timeout_check():
    while True:
        if time.time() - LAST_UPDATE > METRIC_TIMEOUT:
            HR_GAUGE.clear()
        time.sleep(1)

if __name__ == "__main__":
    start_http_server(METRIC_PORT)
    ws = websocket.WebSocketApp(f"{METRIC_HR_URL}",
                                on_message=on_message)
    
    ws_thread = threading.Thread(target=ws.run_forever, daemon=True)
    ws_thread.start()

    timeout_thread = threading.Thread(target=timeout_check, daemon=True)
    timeout_thread.start()


    try:    
      while True:
          time.sleep(1)
    except KeyboardInterrupt:
      print("KeyboardInterrupt")
      ws.close()

        