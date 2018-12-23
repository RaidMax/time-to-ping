from pygal import Line
from pygal.style import Style
import time

class LatencyGraph:
    GRAPH_MAX_PADDING = 10
    def __init__(self, latency_monitor):
        self.latency_monitor = latency_monitor
        self.latency_monitor.start()

    def get_graph(self):
        self._build_graph()
        return self.pygal_graph.render(is_unicode=True)

    def _build_graph(self):
        style = Style(background='transparent', plot_background='transparent', colors=('#2d89ef', '#da532c', '#603cba', '#99b433'),
            title_font_family='Segoe UI',
            legend_font_family='Segoe UI')

        max_latency = max(filter(lambda r : r is not None, [host_value.get_max_time() for host_key, host_value in self.latency_monitor.get_results().items()]))
        min_latency = min(filter(lambda r : r is not None, [host_value.get_min_time() for host_key, host_value in self.latency_monitor.get_results().items()]))
        avg_latency = min(filter(lambda r : r is not None, [host_value.get_avg_time() for host_key, host_value in self.latency_monitor.get_results().items()]))

        self.pygal_graph = Line(show_dots=False,
            title='Max—%i Min—%i Avg—%i' % (max_latency,min_latency, avg_latency),
            style=style,
            range=(0, 100 if max_latency is None else max_latency + 10),
            x_label_rotation=90,
            disable_xml_declaration=True,
            show_x_labels=False,
            height=800,
            width=1920)
        self.pygal_graph.x_labels = []

        for host_key, host_value in self.latency_monitor.get_results().items():
            if len(self.pygal_graph.x_labels) == 0:
                self.pygal_graph.x_labels = [result['time'] for result in host_value.get_ping_times()]

            self.pygal_graph.add(host_key, [result['latency'] for result in host_value.get_ping_times()])
