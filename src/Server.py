from pickle import TRUE
import socket
import threading
from prometheus_client import start_http_server, Counter, Gauge
import json

start_http_server(8000)
CPU_utlization = Gauge('CPU_Utilization', 'Utilization of CPU', [
                       'method', 'endpoint'])
A_Pressed = Counter("A_Pressed", "Number of 'a' or 'A' Pressed", [
    'method', 'endpoint'])

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    isConnected = TRUE
    while isConnected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"{addr} {msg}")
            dict_msg = json.loads(msg)
            if "CPU_Utilization" in dict_msg:
                CPU_utlization.labels(
                    "", f"{addr}").set(dict_msg["CPU_Utilization"])
            if "A_Pressed" in dict_msg:
                A_Pressed.labels(
                    "", f"{addr}").inc()
            if msg == "!DISCONNECT":
                isConnected = False
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


print("[STARTING] server is starting...")
start()
