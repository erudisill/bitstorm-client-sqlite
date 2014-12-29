'''
Created on Dec 29, 2014

@author: ericrudisill
'''
from BleMessageAscii import BleMessageAscii

class MessageAsciiFactory(object):

    def __init__(self):
        self.buffer = ''
    
    def receive(self, data):
        results = []
        self.buffer = ''.join([self.buffer, data])
        while True:
            p = self.buffer.partition('\n')
            if p[1] == '\n':
                try:
                    results.append(BleMessageAscii(p[0]))
                except Exception:
                    pass
                self.buffer = p[2]
            else:
                return results
        