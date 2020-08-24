"""
airrohr-prometheus-exporter web-app
"""
from os import getenv

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    We just say hello here
    """
    return 'Hello, World!'


@app.route('/metrics')
def metrics():
    """
    Expose metrics for the Prometheus collector
    """
    return '# airrohr-prometheus-exporter metrics'


@app.route('/data.php', methods=('POST',))
def data():
    """
    Collects incoming data from airrohs stations
    """
    return '', 201


if __name__ == "__main__":
    """
    Start the server
    """
    app.run(port=getenv('PORT', '80'), debug=True)
