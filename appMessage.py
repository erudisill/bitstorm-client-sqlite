'''
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct AppMessage
    {
        public byte messageType;
        public byte nodeType;
        public UInt64 extAddr;
        public UInt16 shortAddr;
        public UInt64 routerAddr;
        public UInt16 panId;
        public byte workingChannel;
        public UInt16 parentShortAddr;
        public byte lqi;
        public sbyte rssi;
        public byte ackByte;

        public UInt32 battery;
        public UInt32 temperature;

        public byte cs;     
    }
'''

import struct 
import time

class AppMessage:

    def __init__(self, raw=None):
        self.raw = raw
        if not raw is None:
            self.decode(self.raw) 

    def __repr__(self):
        return  'messageType: {0:#04x}, '    \
                'nodeType: {1:#04x}, '          \
                'extAddr: {2:#018x}, '           \
                'shortAddr: {3:#06x}, '           \
                'routerAddr: {4:#018x}, '           \
                'panId: {5:#06x}, '           \
                'workingChannel: {6:#04x}, '           \
                'parentShortAddr: {7:#06x}, '           \
                'lqi: {8:#04x}, '           \
                'rssi: {9}, '           \
                'ackByte: {10:#04x}, '           \
                'battery: {11:#06x}, '           \
                'temperature: {12:#06x}, '           \
                'cs: {13:#04x} '           \
                .format(self.messageType, self.nodeType, self.extAddr, self.shortAddr,  \
                        self.routerAddr, self.panId, self.workingChannel, self.parentShortAddr, \
                        self.lqi, self.rssi, self.ackByte, self.battery, self.temperature, self.cs)
    
   

    def decode(self, data):
        fmt = '<BBQHQHBHBbBIIB'
        x = struct.unpack_from(fmt, data)
        self.messageType = x[0]
        self.nodeType = x[1]
        self.extAddr = x[2]
        self.mac = "{0:016X}".format(x[2])
        self.shortAddr = x[3]
        self.routerAddr = x[4]
        self.router = "{0:016X}".format(x[4])
        self.panId = x[5]
        self.workingChannel = x[6]
        self.parentShortAddr = x[7]
        self.lqi = x[8]
        self.rssi = x[9]
        self.ackByte = x[10]
        self.battery = x[11]
        self.temperature = x[12]
        self.cs = x[13]        
        self.ts = time.time()