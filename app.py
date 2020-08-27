"""
airrohr-prometheus-exporter web-app
"""
import logging
from dataclasses import dataclass
from os import getenv
from typing import Dict

from flask import Flask, request, jsonify, Response

from utils import format_prometheus_metric

app = Flask(__name__)

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('airrohr-prometheus-exporter')


@dataclass
class SensorData:
    """
    Storage for a single sensor data
    """
    sensor_id: str
    meta: Dict[str, str]
    metrics: Dict[str, str]


# keep track of sensors data received
sensors: Dict[str, SensorData] = dict()


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
    def format_sensors(prefix: str):
        for sensor in sensors.values():
            # sensor's metadata
            yield format_prometheus_metric(
                metric_name=f'{prefix}_info',
                metric_help='Information about the sensor.',
                value='1',
                labels=dict(
                    sensor_id=sensor.sensor_id,
                    software=sensor.meta.get('software_version', '')
                )
            ) + '\n'

            # sensor's metrics
            for metric, value in sensor.metrics.items():
                yield format_prometheus_metric(
                    metric_name=f'{prefix}_{metric}',
                    metric_help=f'{metric} metric',
                    value=str(value),
                    labels=dict(
                        sensor_id=sensor.sensor_id
                    )
                ) + '\n'

    return Response(format_sensors(prefix='airrohr'), mimetype='text/plain')


@app.route('/metrics.json')
def metrics_json():
    """
    Expose metrics in JSON format
    """
    return jsonify(dict(
        sensors=list(sensors.values())
    ))


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
        meta=dict(
            software_version=payload.get('software_version', 'unknown')  # NRZ-2020-129
        ),
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
    app.run(host='0.0.0.0', port=getenv('PORT', '8888'), debug=getenv('FLASK_DEBUG', '1') == 1)
