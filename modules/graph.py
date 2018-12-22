from pygal import Line
import time

class LatencyGraph:
    def __init__(self, latency_monitor):
        self.latency_monitor = latency_monitor
        self.latency_monitor.start()


    def get_graph(self):
        self._build_graph()
        return self.pygal_graph.render_response()

    def _build_graph(self):
        self.pygal_graph = Line()
        self.pygal_graph.add('Latency', [])
        self.pygal_graph.x_labels = [result['time'] for result in self.latency_monitor.get_results()]
        self.pygal_graph.add('Latency', [result['latency'] for result in self.latency_monitor.get_results()])

