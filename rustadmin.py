#! /usr/bin/env python
import websocket
import json


class RustAdmin(object):
    def __init__(self, url, passwd):
        self.ws = websocket.create_connection("ws://" + url + '/' + passwd)

    def sndcommand(self, msg):
        print("Sending Message")
        packet = {
                    "Identifier": "1",
                    "Message": msg,
                    "Name": "WebRcon"
                 }
        self.ws.send(json.dumps(packet))
        print("Sent")
        print("Receiving...")
        result = json.loads(self.ws.recv())
        self.ws.close()
        return result
