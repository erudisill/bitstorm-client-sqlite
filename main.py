'''
Created on Dec 29, 2014

@author: ericrudisill
'''
import socket
from MessageAsciiFactory import MessageAsciiFactory
from BitStormDb import BitStormDb
import sys
import time

HOST, PORT = "localhost", 1337

def client(ip, port):
    db = BitStormDb()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    maf = MessageAsciiFactory()
    numRecords = 0
    recordsInFrame = 0
    recordsPerSec = 0.0
    frameStartTime = time.time()
    try:
        while True:
            response = sock.recv(1024)
            if not response: 
                break
            records = maf.receive(response)
            for r in records:
                #print '[RCV] ' + str(r)
                db.insertRecord(r)
                numRecords = numRecords + 1
                recordsInFrame = recordsInFrame + 1
                elapsed = time.time() - frameStartTime
                if elapsed >= 1.0:
                    recordsPerSec = recordsInFrame / elapsed
                    frameStartTime = time.time()
                    recordsInFrame = 0
                msg = "\rRecords: {0}      RPS: {1:.2f}\t".format(numRecords, recordsPerSec)
                sys.stdout.write(msg)
                sys.stdout.flush()
                
    except Exception:
        pass
    finally:
        db.close()
        sock.close()
    
    
if __name__ == '__main__':
    print "\r\n\r\nBitStorm Client Sqlite"
    print "Press Ctrl-C to exit."
    client(HOST, PORT)