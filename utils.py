"""
Utility functions
"""


def format_prometheus_metric(
        metric_name: str, metric_help: str, value: str, labels: dict = None,
        metric_type: str = 'gauge'):
    """
    Format a line with Prometheus metrics
    """
    # An example:
    #
    # HELP node_cooling_device_max_state Maximum throttle state of the cooling device
    # TYPE node_cooling_device_max_state gauge
    # node_cooling_device_max_state{name="0",type="Processor"} 7

    lines = list()

    labels_formatted = ''
    if labels:
        labels_formatted = '{' + ','.join([
            f'{key}="{value}"'
            for key, value in labels.items()
        ]) + '} '

    lines.append(f'HELP {metric_name} {metric_help}')
    lines.append(f'TYPE {metric_name} {metric_type}')
    lines.append(f'{metric_name} {labels_formatted}{value}')

    return '\n'.join(lines)
