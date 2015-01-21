'''
Created on Dec 29, 2014

@author: ericrudisill
'''
import socket
from MessageAsciiFactory import MessageAsciiFactory
from BitStormDb import BitStormDb
import sys
import time
from binascii import hexlify
from appMessage import AppMessage
from cobs import cobs
from statusMessage import StatusMessage

HOST, PORT = "localhost", 1337

class CpSerialBytes(bytearray):
    def __str__(self, *args, **kwargs):
        hexline = hexlify(self)
        n = 2
        pairs = [hexline[i:i+n] for i in range(0, len(hexline), n)]
        final = ("[{0:03}] ".format(len(self)) + " ".join(pairs)).upper()
        return final

def handleStatusMessage(data):
    s = StatusMessage(data)
    return str(s)

def handleAppMessage(data, db):
    r = AppMessage(data)
    db.insertAppMessageRecord(r)

        
def client(ip, port):
    db = BitStormDb()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    #maf = MessageAsciiFactory()
    numErrors = 0
    numRecords = 0
    recordsInFrame = 0
    recordsPerSec = 0.0
    frameStartTime = time.time()
    try:
        while True:
            response = sock.recv(1024)
            if not response: 
                break
            msg2 = ""
            try:
                decoded = bytearray(cobs.decode(response))
                if decoded[0] == 0xAB and decoded[1] == 0xAB:
                    msg2 = handleStatusMessage(decoded)
                    msg = "Records: {0}\tErrors: {1}\tRPS: {2:.2f}\t{3}".format(numRecords, numErrors, recordsPerSec, msg2)
                    print msg
                else:
                    handleAppMessage(decoded, db)
                    numRecords = numRecords + 1
                    recordsInFrame = recordsInFrame + 1
                    elapsed = time.time() - frameStartTime
                    if elapsed >= 5.0:
                        recordsPerSec = recordsInFrame / elapsed
                        frameStartTime = time.time()
                        recordsInFrame = 1
                        
            except Exception:
                numErrors = numErrors + 1

            #sys.stdout.write(msg)
            #sys.stdout.flush()
            
            #data = CpSerialBytes(decoded)
            #print '[RCV] ' + str(data)
#             records = maf.receive(response)
#             for r in records:
#                 #print '[RCV] ' + str(r)
#                 db.insertRecord(r)
#                 numRecords = numRecords + 1
#                 recordsInFrame = recordsInFrame + 1
#                 elapsed = time.time() - frameStartTime
#                 if elapsed >= 5.0:
#                     #print "\r\nrif:{0}   e:{1}".format(recordsInFrame, elapsed)
#                     recordsPerSec = recordsInFrame / elapsed
#                     frameStartTime = time.time()
#                     recordsInFrame = 1
#                 msg = "\rRecords: {0}      RPS: {1:.2f}\t".format(numRecords, recordsPerSec)
#                 sys.stdout.write(msg)
#                 sys.stdout.flush()
                
    except Exception as ex:
        print ex
    finally:
        db.close()
        sock.close()
    
    
if __name__ == '__main__':
    print "\r\n\r\nBitStorm Client Sqlite"
    print "Press Ctrl-C to exit."
    client(HOST, PORT)