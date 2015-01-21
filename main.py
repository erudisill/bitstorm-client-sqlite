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
import json
import requests

HOST, PORT = "localhost", 1337

tags = {}

class Tag(object):
    def __init__(self):
        self.router = ""
        self.mac = ""
        self.rssi = -99
        self.count_better = 0

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
#     20 Lot A,   21 Lot B,   30 Lot C
#      /api/BitStorm/RelocateTag
#     {
#     BinId
#     Mac
#     LocationId
#     }
# data = json.dumps({'BinId':30, 'Mac':'99:99:99:99:99:97'})
# headers = {'content-type': 'application/json;charset=utf-8'}
# r = requests.post(uniurl, data, headers=headers)
    global tags
    r = AppMessage(data)
    db.insertAppMessageRecord(r)
    try:
        tag = tags[r.mac]
        # Tag exists, check for new router proximity
        if r.rssi > -40:
            if r.router != tag.router:
                tag.count_better = tag.count_better + 1
                if tag.count_better >= 3:
                    tag.router = r.router
                    tag.count_better = 0
                    try:
                        if r.router.lower() == '0004251ca0f65c28':
                            bin = 20
                        elif r.router.lower() == '0004251ca0f65c35':
                            bin = 21
                        else:
                            bin = 30
                        pairs = [r.mac[i:i+2] for i in range(0, len(r.mac), 2)]
                        mac_fmt = ":".join(pairs)
#                         data = json.dumps({'BinId':bin, 'Mac': mac_fmt})
#                         headers = {'content-type': 'application/json;charset=utf-8'}
#                         r = requests.post("http://unison-alt.cphandheld.com/api/BitStorm/RelocateTag", data, headers=headers)
                        print 'MOVE ' + str(mac_fmt) + ' TO ' + str(bin)
                    except Exception as ex:
                        print ex
    except Exception as ex:
        # First time seeing the tag, create a dummy record
        tag = Tag()
        tag.mac = r.mac
        tag.router = "xxxx"
        tag.rssi = r.rssi
        tag.count_better = 0
        tags[r.mac] = tag
        
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
                        
            except Exception as ex:
                numErrors = numErrors + 1
                print str(ex)

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