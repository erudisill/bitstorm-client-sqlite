'''
Created on Jan 21, 2015

@author: ericrudisill


typedef struct {
    uint16_t header;
    uint32_t received_count;
    uint32_t received_bytes;
    uint32_t secs_count;
    uint32_t ticks_count;
    uint32_t ticks_count_prev;
    uint16_t ticks_count_delta;
    uint32_t received_count_prev;
    uint16_t received_delta;
    uint32_t error_count;
    uint32_t error_count_prev;
    uint16_t error_delta;
    uint32_t error_queue_count;
    uint32_t error_queue_count_prev;
    uint16_t error_queue_delta;
    uint16_t dequeue_count;
    uint16_t queue_count;
    uint16_t recs_per_sec;
} status_t;

HIIIIIHIHIIHIIHHHH

'''
import struct

class StatusMessage(object):

    def __init__(self, raw=None):
        self.raw = raw
        if not raw is None:
            self.decode(self.raw) 
        
    def __repr__(self):
        return "{0}\tR:{1} (+{2})\tRps:{3}\tE:{4} (+{5})\tQ:{6}\tQe:{7} (+{8})\tD:{9}\tB:{10}\tT:{11}"    \
            .format(self.secs_count, self.received_count, self.received_delta, self.recs_per_sec,           \
                    self.error_count, self.error_delta, self.queue_count, self.error_queue_count,           \
                    self.error_queue_delta, self.dequeue_count, self.received_bytes,                        \
                    self.ticks_count_delta)
    
    def decode(self, data):
        fmt = '<HIIIIIHIHIIHIIHHHH'
        x = struct.unpack_from(fmt, data)
        self.header = x[0]
        self.received_count = x[1]
        self.received_bytes = x[2]
        self.secs_count = x[3]
        self.ticks_count = x[4]
        self.ticks_count_prev = x[5]
        self.ticks_count_delta = x[6]
        self.received_count_prev = x[7]
        self.received_delta = x[8]
        self.error_count = x[9]
        self.error_count_prev = x[10]
        self.error_delta = x[11]
        self.error_queue_count = x[12]
        self.error_queue_count_prev = x[13]
        self.error_queue_delta = x[14]
        self.dequeue_count = x[15]
        self.queue_count = x[16]
        self.recs_per_sec = x[17]
        
        
        
        
              