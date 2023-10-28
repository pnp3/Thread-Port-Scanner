"""Thread Port Scanner Implementation"""
#importation
from queue import Queue
import threading
import socket

# Global Variables
target = "127.0.0.1"
q = Queue()
OpenPorts = []

# port scan function (sockets)
def portScan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for the socket connection
        sock.connect((target, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

# mode selection function
def ModeSelector(mode):
    if mode == 1:
        for port in range(1, 1024):  # Change the upper range limit to include port 1023
            q.put(port)
    elif mode == 2:
        for port in range(1, 49152):  # Change the upper range limit to include port 49151
            q.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            q.put(port)
    elif mode == 4:
        ports_input = input("Please enter your desired ports: ")
        ports = ports_input.split()
        ports = list(map(int, ports))
        for port in ports:
            q.put(port)

# worker - if queue not empty => add to our list of open ports
def PortsQueuer():
    while not q.empty():
        port = q.get()
        if portScan(port):
            print("Port {} is open!".format(port))
            OpenPorts.append(port)

# thread function
def run_scanner(threads, mode):
    ModeSelector(mode)

    thread_list = []

    for _ in range(threads):
        thread = threading.Thread(target=PortsQueuer)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("The open ports are:", OpenPorts)

run_scanner(100, 1)
