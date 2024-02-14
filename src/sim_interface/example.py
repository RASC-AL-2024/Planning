
# example script which connects to unity, and sends a command to rover 0 when a key is pressed

import UdpComms as U
import time
import json

sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

i = 0

test_input = {"id": "0", "type": "MOVE_TO", "x": "18", "y": "40"}
json_string = json.dumps(test_input)
sent = False

input("connected to simulation...")

while True:
    i += 1

    data = sock.ReadReceivedData()

    if data != None:
        print(data)
        
    if not sent:
        sock.SendData(json_string);
        sent = True

    time.sleep(1)
    


