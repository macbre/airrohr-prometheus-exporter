"""
Test utils.py
"""
from typing import List

from prometheus_client import Metric

from utils import SensorsDataCollector, SensorData


def test_sensors_data_collector():
    sensor_a = SensorData(
        sensor_id='foo-123',
        last_read=123456,
        meta=dict(software_version='1.0.0'),
        metrics=dict(
            temp='23.5'
        )
    )
    sensor_b = SensorData(
        sensor_id='foo-245',
        last_read=123456,
        meta=dict(software_version='1.2.0'),
        metrics=dict(
            temp='18.5',
            pressure='1024'
        )
    )

    collector = SensorsDataCollector(sensors_data=[sensor_a, sensor_b], prefix='test_airrohr_')

    # check what kind of metrics are emitted
    metrics: List[Metric] = list(collector.collect())

    assert [metric.name for metric in metrics] == [
        'test_airrohr_info',
        'test_airrohr_last_measurement_timestamp',
        'test_airrohr_pressure',
        'test_airrohr_temp',
    ]

    # test one of the metrics
    info = metrics[0]
    assert len(info.samples) == 2
    assert info.samples[0].labels == {'sensor_id': 'foo-123', 'software': '1.0.0'}
    assert info.samples[1].labels == {'sensor_id': 'foo-245', 'software': '1.2.0'}
