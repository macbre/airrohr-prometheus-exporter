"""
Utility functions
"""
from dataclasses import dataclass
from typing import List, Dict, Iterator

from prometheus_client import Metric


@dataclass
class SensorData:
    """
    Storage for a single sensor's data
    """
    sensor_id: str
    last_read: int
    meta: Dict[str, str]
    metrics: Dict[str, str]


# pylint:disable=too-few-public-methods
class SensorsDataCollector:
    """
    Converts SensorData dataclasses into Prometheus Metrics
    """
    def __init__(self, sensors_data: List[SensorData], prefix: str):
        self.sensors_data = sensors_data
        self.prefix = prefix

    def collect(self) -> Iterator[Metric]:
        """
        Do the conversion
        """
        # Metric(name, documentation, typ, unit)
        #
        # system information metric
        metric = Metric(
            name=f'{self.prefix}info', documentation='Information about the sensor.', typ='gauge')

        for sensor in self.sensors_data:
            metric.add_sample(name=f'{self.prefix}info', value=1, labels={
                'sensor_id': sensor.sensor_id,
                'software': sensor.meta.get('software_version', '')
            })
        yield metric

        # last measurement metric
        metric = Metric(
            name=f'{self.prefix}last_measurement',
            documentation='When was the most recent data received.',
            typ='gauge',
            unit='timestamp'
        )

        for sensor in self.sensors_data:
            metric.add_sample(
                name=f'{self.prefix}last_measurement',
                value=sensor.last_read,
                labels={
                    'sensor_id': sensor.sensor_id,
                })
        yield metric

        # sensors data
        # iterate through all metrics
        sensors_metrics = []

        for sensor in self.sensors_data:
            sensors_metrics += sensor.metrics.keys()

        for metric_name in sorted(set(sensors_metrics)):
            metric = Metric(
                name=f'{self.prefix}{metric_name}',
                documentation=f'{metric_name} metric from airrohr.',
                typ='gauge'
            )

            for sensor in self.sensors_data:
                if (value := sensor.metrics.get(metric_name)) is not None:
                    metric.add_sample(
                        name=f'{self.prefix}{metric_name}', value=value,
                        timestamp=sensor.last_read, labels={
                            'sensor_id': sensor.sensor_id,
                        })
            yield metric
