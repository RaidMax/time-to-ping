from flask import Flask, render_template
from modules.config import Config
from modules.latency import Latency

app = Flask(__name__)
config = Config('configuration.json' if not app.debug else 'configuration.dev.json')
ping = Latency(config.get_value('ping_hosts'), config.get_value('ping_interval'))
ping.start()

@app.route('/')
def index():
    return render_template('ping.html')
