'''
Created on Dec 29, 2014

@author: ericrudisill
'''
import socket
from binascii import hexlify
from MessageAsciiFactory import MessageAsciiFactory

HOST, PORT = "localhost", 1337

def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    maf = MessageAsciiFactory()
    while True:
        response = sock.recv(1024)
        if not response: 
            break
        messages = maf.receive(response)
        for m in messages:
            print '[RCV] ' + str(m)
    sock.close()
    
    
if __name__ == '__main__':
    client(HOST, PORT)