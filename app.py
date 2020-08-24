"""
airrohr-prometheus-exporter web-app
"""
import logging
from os import getenv

from flask import Flask, request
app = Flask(__name__)

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('airrohr-prometheus-exporter')


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
    # X-Sensor: esp8266-12331981
    sensor_id = request.headers.get('X-Sensor', 'unknown')

    # You need to set the request content type to application/json
    payload = request.get_json()

    if sensor_id is None or payload is None:
        return 'Bad request / no payload / no X-Sensor header set', 400

    logger.info('Got metrics from "%s" sensor', sensor_id)
    return 'Metrics received', 201


if __name__ == "__main__":
    # Start the server
    app.run(port=getenv('PORT', '80'), debug=True)
