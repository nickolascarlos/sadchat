import datetime
import time
import threading

import state

def update_time():
    while True:
        now = datetime.datetime.now()
        state.set_time(now.hour, now.minute, now.second)
        time.sleep(1)

t = threading.Thread(target=update_time)
t.start()