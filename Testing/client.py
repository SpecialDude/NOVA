import socket
import threading
import queue
import os
import sys


args = sys.argv[1:]

if len(args) > 0:
    hostname = args[0]

else:
    hostname = socket.gethostname()


name = socket.gethostname()


port = 9999
server = None

NUMBER_OF_JOBS = 2
job_number = [1, 2]
queing = queue.Queue()

online = False



print("\n------------------------------> NOVA <------------------------------")
print("\t\t\t\t\t\ta wlan Instant chatAPP\n\n")




def create_socket():
    global server

    try:
        server = socket.socket()
    except socket.error as errmsg:
        print('Trouble creating socket: ' + str(errmsg))

def connect_server():
    global online
    try:
        server.connect((hostname, port))
        server.send(name.encode())
        print('connected to', hostname)
        print()
        send_msg()
    except socket.error as errmsg:
        print('Trouble connecting to server: ' + str(errmsg))
        server.close()
        connect_server()

def send_msg():
    global online
    while True:
        msg = input('You> ')
        msg = msg.encode()
        server.send(msg)
            
def receive_message():
    while True:
        if server  == None:
            continue
        try:
            msg = server.recv(1024)
            msg = msg.decode()
            print(('\n') + (hostname + '> ' + msg).rjust(os.get_terminal_size().columns))
            print( '\n' + 'you> ', end='')
        except:
            pass

def create_worker():
    for _ in range(NUMBER_OF_JOBS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        x = queing.get()
        if x == 1:
            create_socket()
            connect_server()
        if x == 2:
            receive_message()
        queing.task_done()

def create_jobs():
    for i in job_number:
        queing.put(i)
    queing.join()

create_worker()
create_jobs()
