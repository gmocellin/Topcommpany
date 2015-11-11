#coding: utf-8

import socket

endereco = ('localhost', 10000)
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

sock.bind (endereco)
sock.listen (1)
while True:
    print 'Esperando conexão...'
    connection, client_address = sock.accept()
    print 'Conexão por', client_address
    try:
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(24)
            print 'Sensor indica: %s graus' % data
            if not data:
                print 'Fim da leitura do', client_address
                break

    finally:
        # Clean up the connection
        connection.close()
