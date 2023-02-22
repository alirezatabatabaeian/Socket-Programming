from email.errors import HeaderParseError
from http import client
import socket
import json
import psutil
import time
from random import choice

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_.send(send_length)
    client_.send(message)


client_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        client_.connect(ADDR)
    except:
        try:
            jsonResult = {"CPU_Utilization": psutil.cpu_percent(1)}
            jsonResult = json.dumps(jsonResult)
            send(jsonResult)
            time.sleep(1)
            char = choice(["a", "b", "c", "A", "B", "C"])
            if (char == "a") or (char == "A"):
                jsonResult = {"A_Pressed": "1"}
                jsonResult = json.dumps(jsonResult)
                send(jsonResult)
                time.sleep(1)
        except:
            client_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Trying to ReConnect")
