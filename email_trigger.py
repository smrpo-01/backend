import time
from datetime import datetime
import urllib3

if __name__ == "__main__":
    time.sleep(60)
    while 1:
        current_time = datetime.time(datetime.now())
       # if current_time >= datetime.time(datetime(2018, 5, 5, 12)) or current_time <= datetime.time(
       #         datetime(2018, 5, 5, 6)):
       #     time.sleep(60 * 60)
       # else:
        try:
            http = urllib3.PoolManager()
            #TODO: spremen na taprav url
            html = http.request('GET', "http://localhost:8000/graphiql?query={mail}").data
            #html = http.request('GET', "http://emineo.eu-de.mybluemix.net/graphiql?query={mail}").data
            print(html)
        except:
            pass
        time.sleep(60)
