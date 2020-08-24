"""
Test utils.py
"""
from utils import format_prometheus_metric


def test_format_prometheus_metric():
    assert format_prometheus_metric(metric_name='foo_bar', metric_help='Help', value='12.4') \
        == 'HELP foo_bar Help\nTYPE foo_bar gauge\nfoo_bar 12.4'

    assert format_prometheus_metric(metric_name='foo_bar', metric_help='Help', value='12.4', labels={}) \
        == 'HELP foo_bar Help\nTYPE foo_bar gauge\nfoo_bar 12.4'

    assert format_prometheus_metric(metric_name='foo_bar', metric_help='Help', value='12.4', labels={'id': '12345'}) \
        == 'HELP foo_bar Help\nTYPE foo_bar gauge\nfoo_bar {id="12345"} 12.4'

    assert format_prometheus_metric(metric_name='foo_bar', metric_help='Help', value='12.4', labels={'id': '12345', 'version': '1.0.0'}) \
        == 'HELP foo_bar Help\nTYPE foo_bar gauge\nfoo_bar {id="12345",version="1.0.0"} 12.4'
