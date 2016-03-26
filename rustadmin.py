#! /usr/bin/env python
import websocket
import json
from settings import mode


class RustAdmin(object):
    def __init__(self, url, passwd):
        if mode != 'test':
            self.ws = websocket.create_connection("ws://" + url + '/' + passwd)
        self.mode = mode

    def sndcommand(self, msg):
        print("Sending Message")
        packet = {
                    "Identifier": "1",
                    "Message": msg,
                    "Name": "WebRcon"
                 }
        if self.mode == 'test':
            print("Sent")
            print("Recieving")
            return "{'Message', 'test message'}"
        else:
            self.ws.send(json.dumps(packet))
            print("Sent")
            print("Receiving...")
            result = json.loads(self.ws.recv())
            self.ws.close()
            return result
