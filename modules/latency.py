from threading import Thread, Event, Timer
from pings import Ping
from modules.ping_result import PingResult

class Latency(Thread):
    def __init__(self, ping_hosts, interval):
        self.MIN_INTERVAL = 20
        self.ping_hosts = ping_hosts
        self.interval = interval
        self.ping_results = {}
        self.on_stop_set = Event()

        if interval < self.MIN_INTERVAL:
            print('** %i is below the minimum interval of 20ms' % interval)
            self.interval = self.MIN_INTERVAL

        Thread.__init__(self)

    def run(self):
        print('* begin pinging hosts')
        while not self.on_stop_set.wait(self.interval / 1000.0):
            for host in self.ping_hosts:
                if host not in self.ping_results:
                    self.ping_results[host] = PingResult(host)
               
                response = Ping().ping(host)
                self.ping_results[host].add_time(response.max_rtt)

    def stop(self):
        self.on_stop_set.set()
        print ('sent stop signal')