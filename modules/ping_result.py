from queue import Queue
import time

class PingResult:
    MAX_RESULTS = 60
    
    def __init__(self):
        self.total_pings = 0
        self.lost_packets = 0
        self.max_rtt = None
        self.min_rtt = None
        self.avg_rtt = None
        self.ping_times = []
        self.ping_time_queue = Queue(maxsize=PingResult.MAX_RESULTS)

    def add_time(self, latency):
        if self.ping_time_queue.qsize() == PingResult.MAX_RESULTS - 1:
            self.ping_time_queue.get()

        self.total_pings += 1

        if latency is None:
            self.lost_packets += 1
        else:
            # update stats
            if self.total_pings == 1:
                self.avg_rtt = latency
                self.min_rtt = latency
                self.max_rtt = latency
            else:
                if latency > self.max_rtt:
                    self.max_rtt = latency
                if latency < self.min_rtt:
                    self.min_rtt = latency

                count = max(1, self.total_pings - self.lost_packets)
                # keeps a running average of the latency
                self.avg_rtt = (self.avg_rtt * (count - 1) + latency) / count

            self.ping_time_queue.put({ 
                    'time' : int(round(time.time() * 1000)),  
                    'latency' : latency
                })

        return True

    def get_ping_times(self):
        return list(self.ping_time_queue.queue)

    def get_max_time(self):
        return self.max_rtt

    def get_min_time(self):
        return self.min_rtt

    def get_avg_time(self):
        return self.avg_rtt