from flask import Flask, render_template
from modules.config import Config
from modules.latency import Latency
from modules.graph import LatencyGraph

app = Flask(__name__)
config = Config('configuration.json' if not app.debug else 'configuration.dev.json')
latency = Latency(config.get_value('ping_hosts'), config.get_value('ping_interval'))
graph = LatencyGraph(latency)

@app.route('/')
def index():
    return render_template('ping.html')

@app.route('/graph')
def graph_route():
    return graph.get_graph()
