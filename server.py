import socket
import sys
import threading
import time
from queue import Queue


# socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1024))
s.listen(5)

# vars
NUM_THREADS = 2
JOB_NUM = [1, 2]
queue = Queue()
allCxns = []
allAdrs = []

lastMsg = ''
counter = 0

while True:
    # accepts client
    clt, adr = s.accept()
    print(f"Connection to {adr} established")
    msg = clt.recv(1024).decode('utf-8')
    print(msg)
    # checks if GET request from browser
    if (msg.startswith('GET')):
        clt.send(bytes('\nHTTP/1.x 200 OK\n', 'utf-8'))
        clt.send(bytes(f'''<!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>

            <body>
                <p>Pogs: {counter}</p>
            </body>

            </html>''', 'utf-8'))
    else:
        if (msg != str(counter)):
            print(msg)
        elif(msg == '10'):
            break
        counter = msg

clt.close()

# handling connections from multiple clients and saves to lists


def acceptCxns():
    # closes cxns when file is restarted
    for c in allCxns:
        c.close()
    del allCxns[:]
    del allAdrs[:]

    while True:
        try:
            cxn, adr = s.accept()
            s.setblocking(1)  # prevents timeout
            allCxns.append(cxn)
            allAdrs.append(adr)

            print(f'connection has been extablished {adr[0]}')
        except:
            print("Error accepting connections")


def sendingData():
    for c in allCxns:
        if c.startwith('GET'):
            c.send(bytes(f'''<!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                </head>

                <body>
                    <p>Pogs: {counter}</p>
                </body>

                </html>''', 'utf-8'))
