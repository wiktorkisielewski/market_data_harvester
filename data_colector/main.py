import websocket
import os
import json
import datetime
import time
import psycopg2

time.sleep(5)

token = os.environ.get('FINHUB_KEY')
exchange = os.environ.get('EXCHANGE')
instrument = os.environ.get('INSTRUMENT')
psql_user = os.environ.get('POSTGRES_USER')
psql_pass = os.environ.get('POSTGRES_PASSWORD')

c = psycopg2.connect(database=exchange, user=psql_user, password=psql_pass, host='postgres', port='5432')
cur = c.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS {} 
                        (TIME_STAMP BIGINT NOT NULL, 
                        QUOTE REAL NOT NULL,
                        VOLUME REAL NOT NULL
                        );'''.format(instrument))
c.commit()

def on_message(ws, message):
    start_time = time.time()
    data = json.loads(message)['data']
    for i in data:
        quote = i['p']
        volume = i['v']
        timestamp = i['t']
        print('------------->', timestamp, quote, volume)
        cur.execute('''INSERT INTO {}(TIME_STAMP, QUOTE, VOLUME) VALUES({}, {}, {})'''.format(instrument, timestamp, quote, volume))
        c.commit()
    print("--- %s seconds ---" % (time.time() - start_time))

def on_error(ws, error):
    print(error, '\n### {}'.format(datetime.datetime.now()))

def on_close(ws):
    print('### closed | {} ###'.format(datetime.datetime.now()))

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BNBUSDT"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token={}".format(token), on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()