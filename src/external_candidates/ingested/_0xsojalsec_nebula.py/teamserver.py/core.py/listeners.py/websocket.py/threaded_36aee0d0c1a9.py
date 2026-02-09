# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Nebula\teamserver\core\Listeners\WebSocket\threaded.py
import threading
import time

global c, d
c = 0
d = 0


def checkandrun():
    global c, d
    while True:
        if c == 1:
            break
        d += 1
        print(str(d))
        time.sleep(5)


t = threading.Thread(target=checkandrun)
t.start()

command = input(">>>")
while True:
    if command == "inc":
        c += 1
        break
