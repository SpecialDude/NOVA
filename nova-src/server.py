import socket
import threading
from queue import Queue
import os


NUMBER_OF_JOBS = 2
job_number = [1, 2]

queing = Queue()

client = None
address = None
name = None

online = False

print("\n------------------------------> NOVA <------------------------------")
print("\t\t\t\t\t\ta wlan Instant chatAPP\n\n")


def create_socket():
    global hostname
    global port
    global server

    hostname = socket.gethostbyname(socket.gethostname())
    hostname = socket.gethostname()
    #hostname = "0.0.0.0"
    port = 9999
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as errmsg:
        print('Error Creating a socket: ' + str(errmsg))

def bind_socket():
    global hostname
    global port
    global server

    try:
        server.bind((hostname, port))
        print(hostname, "is Waiting for connections")
        server.listen(5)
    except socket.error as errmsg:
        print('Error binding the server socket: ' + str(errmsg))

def accept_connection():
    global client
    global address
    global online
    global name


    try:
        client, address = server.accept()
        name = client.recv(1024).decode()
        #server.setblocking(1)
        print('Now connected to', name)
        print()
        online = True
        send_message()
    except socket.error as errmsg:
        print('Error accepting connection: ' + str(errmsg))
        accept_connection()

def send_message():
    global online
    while True:
        msg = input('You> ')
        msg = msg.encode()
        client.send(msg)

            

def receive_message():
    global online
    while True:
        if client == None:
            continue
        try:
            
            msg = client.recv(1024).decode()
            print('\n' + name + '> ' + msg + '\n' + 'you> ', end='')
            online = True
        except:
            pass

def receive_message():
    global online
    while True:
        if client  == None:
            continue
        try:
            msg = client.recv(1024)
            msg = msg.decode()
            print(('\n') + (name + '> ' + msg).rjust(os.get_terminal_size().columns))
            print( '\n' + 'you> ', end='')
            online = True
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
            bind_socket()
            accept_connection()
        if x == 2:
            receive_message()
        queing.task_done()

def create_jobs():
    for i in job_number:
        queing.put(i)
    queing.join()


create_worker()
create_jobs()



