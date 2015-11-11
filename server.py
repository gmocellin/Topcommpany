import socket

endereco = ('localhost', 10000)
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

sock.bind (endereco)
sock.listen (1)
while True:
    print 'waiting connection'
    connection, client_address = sock.accept()
    print 'connection from', client_address
    try:
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(24)
            print 'received "%s"' % data
            if not data:
                print 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()
