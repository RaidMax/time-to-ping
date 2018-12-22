from threading import Thread, Event, Timer
from pings import Ping
from modules.ping_result import PingResult

class Latency(Thread):
    def __init__(self, ping_hosts, interval):
        self.MIN_INTERVAL = 20
        self.ping_hosts = ping_hosts
        self.interval = interval
        self.ping_results = {}
        self.on_stop = Event()

        if interval < self.MIN_INTERVAL:
            print('** %i is below the minimum interval of 20ms' % interval)
            self.interval = self.MIN_INTERVAL

        Thread.__init__(self)

    def run(self):
        print('* begin pinging hosts')
        while not self.on_stop.wait(self.interval / 1000.0):
            for host in self.ping_hosts:
                if host not in self.ping_results:
                    self.ping_results[host] = PingResult()
               
                response = Ping().ping(host)
                if not self.ping_results[host].add_time(response.max_rtt):
                    self.ping_results[host] = PingResult()

    def stop(self):
        self.on_stop.set()
        print ('* sent stop signal')

    def get_results(self):
        return self.ping_results[self.ping_hosts[0]].ping_times