import socket
import threading
import signal
import sys

users = {}

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

##

def handle_client_connection(client_socket,address): 
    print('Accepted connection from {}:{}'.format(address[0], address[1])) # IP & Port
    ip_port = "{}:{}".format(address[0], address[1]) #
    if ip_port not in users:
        users[ip_port] = {"Ip": address[0], "Port": address[1], "Payload": 0}
        
    try:
        while True:
            request = client_socket.recv(1024)
            if not request:
                client_socket.close()
            else:
                msg=request.decode()
                users.get(ip_port)["Payload"] += len(msg)
                payload_amount = str(users.get(ip_port)["Payload"])
                print('Received {}'.format(msg))
                msg=("ECHO: "+msg+"\nBytes: " + str(len(msg)) + "\nPayload amount: "+payload_amount).encode()
                client_socket.send(msg)
    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(address))

ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, tcp_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(ip_addr, tcp_port))

while True:
    client_sock, address = server.accept()
    client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address),daemon=True)
    client_handler.start()


