"""
airrohr-prometheus-exporter web-app
"""
import logging
import time
from os import getenv
from typing import Dict

from flask import Flask, request, jsonify, Response
from prometheus_client import generate_latest
from utils import SensorData, SensorsDataCollector

app = Flask(__name__)

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('airrohr-prometheus-exporter')


# keep track of sensors data received
sensors: Dict[str, SensorData] = {}


@app.route('/')
def hello_world():
    """
    We just say hello here
    """
    return """
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>airrohr-prometheus-exporter</title>
    <style>body {
  font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,Liberation Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;
  margin: 0;
}
header {
  background-color: #e6522c;
  color: #fff;
  font-size: 1rem;
  padding: 1rem;
}
main {
  padding: 1rem;
}
li {
  line-height: 1.5em;
}

</style>
  </head>
  <body>
    <header>
      <h1>airRohr Exporter</h1>
    </header>
    <main>
      <h2>Prometheus <a href="https://github.com/opendata-stuttgart/sensors-software">airRohr</a> Exporter</h2>
      <div>
        <ul>
          <li><a href="/metrics">Metrics</a></li>
          <li><a href="https://github.com/macbre/airrohr-prometheus-exporter">Visit GitHub</a></li>
        </ul>
      </div>
    </main>
  </body>
</html>
""".strip()


@app.route('/metrics')
def metrics():
    """
    Expose metrics for the Prometheus collector
    """
    collector = SensorsDataCollector(sensors_data=list(sensors.values()), prefix='airrohr_')

    return Response(generate_latest(registry=collector), mimetype='text/plain')


@app.route('/metrics.json')
def metrics_json():
    """
    Expose metrics in JSON format
    """
    return jsonify({
        'sensors': list(sensors.values())
    })


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

    # store received metrics
    sensors[sensor_id] = SensorData(
        sensor_id=sensor_id,
        last_read=int(time.time()),
        meta={
            'software_version': payload.get('software_version', 'unknown')  # NRZ-2020-129
        },
        metrics={
            # bme280_temperature: 20.47
            str(metric['value_type']).lower(): metric['value']
            for metric in payload.get('sensordatavalues')
            if 'value_type' in metric and 'value' in metric
        }
    )

    return 'Metrics received', 201


if __name__ == "__main__":
    # Start the server
    app.run(
        host='0.0.0.0',
        port=getenv('HTTP_PORT', '8888'),
        debug=getenv('FLASK_DEBUG', '1') == '1'
    )
