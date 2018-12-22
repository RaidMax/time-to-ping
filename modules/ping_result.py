import time

class PingResult:
    MAX_RESULTS = 1024
    
    def __init__(self):
        self.total_pings = 0
        self.lost_packets = 0
        self.max_rtt = None
        self.min_rtt = None
        self.avg_rtt = None
        self.ping_times = []

    def add_time(self, latency):
        if self.total_pings == PingResult.MAX_RESULTS:
            return False

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

            self.ping_times.append({ 
                    'time' : int(round(time.time() * 1000)),  
                    'latency' : latency
                })

        return True

    def get_max_time(self):
        return self.max_rtt

    def get_min_time(self):
        return self.min_rtt

    def get_avg_time(self):
        return self.avg_rtt