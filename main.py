'''
Created on Dec 29, 2014

@author: ericrudisill
'''
import socket
from MessageAsciiFactory import MessageAsciiFactory
from BitStormDb import BitStormDb

HOST, PORT = "localhost", 1337

def client(ip, port):
    db = BitStormDb()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    maf = MessageAsciiFactory()
    try:
        while True:
            response = sock.recv(1024)
            if not response: 
                break
            records = maf.receive(response)
            for r in records:
                print '[RCV] ' + str(r)
                db.insertRecord(r)
    except Exception:
        pass
    finally:
        db.close()
        sock.close()
    
    
if __name__ == '__main__':
    client(HOST, PORT)