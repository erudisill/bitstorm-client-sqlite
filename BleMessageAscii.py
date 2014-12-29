'''
Created on Dec 29, 2014

@author: ericrudisill
'''
import time

class BleMessageAscii(object):

    def __init__(self, raw):
        self.raw = raw
        parts = self.raw.replace('*', '').split(' ')
        self.mac = parts[0]
        self.rssi = int(parts[1], 16)
        self.temp = int(parts[2], 16)
        self.batt = int(parts[3], 16)
        self.cs = int(parts[4], 16)
        self.ts = time.time()
     
    def __str__(self):
        return "M:{0} R:{1:02X} T:{2:04X} B:{3:04X} C:{4:02X} TS:{5}". \
                format(self.mac, self.rssi, self.temp, self.batt, self.cs, self.ts)
    
    