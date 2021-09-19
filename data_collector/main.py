import websocket
import os
import json
import datetime
import time
import psycopg2
import yaml

time.sleep(5)

token = os.environ.get('FINHUB_KEY')
psql_user = os.environ.get('POSTGRES_USER')
psql_pass = os.environ.get('POSTGRES_PASSWORD')

c = psycopg2.connect(database='ticks', user=psql_user, password=psql_pass, host='postgres', port='5432')
cur = c.cursor()

def on_message(ws, message):
    start_time = time.time()
    data = json.loads(message)['data']
    for i in data:
        instrument = i['s'].split(':')[1]
        quote = i['p']
        volume = i['v']
        timestamp = i['t']
        cur.execute('''INSERT INTO {}(TIME_STAMP, QUOTE, VOLUME) VALUES({}, {}, {})'''.format((instrument.replace('/', '_')).replace('-','_'), timestamp, quote, volume))
        c.commit()
        print("-----> %s seconds <-----" % (time.time() - start_time))

def on_error(ws, error):
    print(error, '\n### {}'.format(datetime.datetime.now()))

def on_close(ws):
    print('### closed | {} ###'.format(datetime.datetime.now()))

def on_open(ws):
    with open('data_collector/symbols.yml', 'r') as f:
        symbols = yaml.safe_load(f)
        f.close()
    for i in symbols:
        for j in symbols[i]:
            cur.execute('''CREATE TABLE IF NOT EXISTS {} 
                        (TIME_STAMP BIGINT NOT NULL, 
                        QUOTE REAL NOT NULL,
                        VOLUME REAL NOT NULL
                        );'''.format((j.replace('/', '_')).replace('-','_')))
            c.commit()
            sub = {'type':'subscribe','symbol':''}
            if i != 'stocks':
                sub['symbol'] = str(symbols['exchanges'][i].upper() + ':' + j)
            else:
                sub['symbol'] = str(j).upper()
            print(str(sub).replace("'", "\""))
            ws.send(str(sub).replace("'", "\""))
            time.sleep(1.5)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token={}".format(token), on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()