# airrohr-prometheus-exporter
This a HTTP server that accepts data sent by [`airrohr` AirQuality monitoring station](https://sensor.community/en/sensors/airrohr/) (temperature, pressure and PM metrics) and exposes them to [Prometheus](https://prometheus.io/)' metrics collector.

You can then plot them with [Grafana](https://grafana.com/) and have Prometheus alerting you on the measurements. Observability!

<img width="889" alt="Screenshot 2023-11-21 at 11 03 10" src="https://github.com/macbre/airrohr-prometheus-exporter/assets/1929317/8496cf0f-b35b-4960-959b-700d23cf4b20">

## Run using Docker

Up to date container image can be fetched from [GitHub's Container Registry](https://github.com/macbre/airrohr-prometheus-exporter/pkgs/container/airrohr-prometheus-exporter) and run via:

```
docker run --detach --restart unless-stopped -p 55123:8888 --name airrohr -t ghcr.io/macbre/airrohr-prometheus-exporter:latest
```

And then:

```
$ curl 0:55123/metrics
# HELP airrohr_info Information about the sensor.
# TYPE airrohr_info gauge
# HELP airrohr_last_measurement_timestamp When was the most recent data received.
# TYPE airrohr_last_measurement_timestamp gauge
```

## Set up your Airrohr sensors

1. Visit the `/config` page of your sensor.
2. Enable the "Send data to custom API" option.
3. Provide the hostname and the port where your `airrohr-prometheus-exporter` instance is running. Keep `/data.php` as the path.

For instance:

<img width="618" alt="Screenshot 2023-11-21 at 11 06 17" src="https://github.com/macbre/airrohr-prometheus-exporter/assets/1929317/de0291f9-6fb4-4377-8208-55c935a0309a">

## HTTP endpoints

#### `POST /data.php`

[Set up your airrohr station](https://sensor.community/en/sensors/dnms#Configure_the_station) to "Send data to custom API" and provide the IP address and port where `airrohr-prometheus-exporter` runs.

#### Example request

```yaml
POST /data.php HTTP/1.1
Host: my.host.name:1234
User-Agent: NRZ-2020-129/12331981
Connection: close
Accept-Encoding: identity;q=1,chunked;q=0.1,*;q=0
Authorization: Basic xxx
Content-Type: application/json
X-Sensor: esp8266-12331981
Content-Length: 481

{"esp8266id": "12331981", "software_version": "NRZ-2020-129", "sensordatavalues":[{"value_type":"SDS_P1","value":"0.40"},{"value_type":"SDS_P2","value":"0.20"},{"value_type":"BME280_temperature","value":"20.47"},{"value_type":"BME280_pressure","value":"100613.25"},{"value_type":"BME280_humidity","value":"69.02"},{"value_type":"samples","value":"4222662"},{"value_type":"min_micro","value":"32"},{"value_type":"max_micro","value":"3301275"},{"value_type":"signal","value":"-94"}]}
```

Or from debug logs (via airrohr sensor web UI):

```yaml
## Sending as csv: 
CSV Output: {"software_version": "NRZ-2024-136-B1", "sensordatavalues":[{"value_type":"temperature","value":"35.20"},{"value_type":"humidity","value":"45.30"},{"value_type":"samples","value":"1133404"},{"value_type":"min_micro","value":"25"},{"value_type":"max_micro","value":"99760"},{"value_type":"interval","value":"30000"},{"value_type":"signal","value":"-65"}]}
```

#### `GET /metrics`

Exposes metrics collected from airrohr stations in Prometheus format.

##### An example

```
# HELP airrohr_info Information about the sensor.
# TYPE airrohr_info gauge
airrohr_info{sensor_id="esp8266-12331981",software="NRZ-2020-129"} 1.0
airrohr_info{sensor_id="esp8266-12326597",software="NRZ-2020-129"} 1.0
# HELP airrohr_last_measurement_timestamp When was the most recent data received.
# TYPE airrohr_last_measurement_timestamp gauge
airrohr_last_measurement{sensor_id="esp8266-12331981"} 1.598988915e+09
airrohr_last_measurement{sensor_id="esp8266-12326597"} 1.598988842e+09
# HELP airrohr_bme280_humidity bme280_humidity metric from airrohr.
# TYPE airrohr_bme280_humidity gauge
airrohr_bme280_humidity{sensor_id="esp8266-12331981"} 67.89 1598988915000
airrohr_bme280_humidity{sensor_id="esp8266-12326597"} 56.13 1598988842000
...
```

#### `GET /metrics.json`

Exposes metrics collected from airrohr stations in JSON format.

##### An example

```json
{
  "sensors": [
    {
      "last_read": 1598988915,
      "meta": {
        "software_version": "NRZ-2020-129"
      },
      "metrics": {
        "bme280_humidity": "67.89",
        "bme280_pressure": "101114.53",
        "bme280_temperature": "19.07",
        "max_micro": "20783",
        "min_micro": "27",
        "samples": "4195163",
        "sds_p1": "0.30",
        "sds_p2": "0.10",
        "signal": "-93"
      },
      "sensor_id": "esp8266-12331981"
    },
    {
      "last_read": 1598988842,
      "meta": {
        "software_version": "NRZ-2020-129"
      },
      "metrics": {
        "bme280_humidity": "56.13",
        "bme280_pressure": "101068.25",
        "bme280_temperature": "20.91",
        "max_micro": "2809",
        "min_micro": "32",
        "samples": "4387819",
        "signal": "-25"
      },
      "sensor_id": "esp8266-12326597"
    }
  ]
}
```

## Prometheus

And an entry to `scrape_configs` section in your `prometheus.yml` in order to scrape metrics from this exporter:

```yaml
scrape_configs:
  - job_name: 'airrohr'
    static_configs:
    - targets:
      # /metrics path is automatically added by Prometheus when scraping metrics
      # please adjust the port below
      - your.server.address:55123
```


## Local development

Start this server locally and make a request using `curl`:

```
FLASK_ENV=devel HTTP_PORT=55123 python app.py
curl 0:55123/data.php -H 'X-Sensor: foo' -H 'Content-Type: application/json' -d '{"esp8266id": "12331981", "software_version": "NRZ-2020-129", "sensordatavalues":[{"value_type":"SDS_P1","value":"0.40"},{"value_type":"SDS_P2","value":"0.20"},{"value_type":"BME280_temperature","value":"20.47"},{"value_type":"BME280_pressure","value":"100613.25"},{"value_type":"BME280_humidity","value":"69.02"},{"value_type":"samples","value":"4222662"},{"value_type":"min_micro","value":"32"},{"value_type":"max_micro","value":"3301275"},{"value_type":"signal","value":"-94"}]}'
```

### Docker container

```
docker pull ghcr.io/macbre/airrohr-prometheus-exporter:latest
docker run --detach --restart unless-stopped -p 55123:8888 --name airrohr -t ghcr.io/macbre/airrohr-prometheus-exporter
```

Or build it from the source code:

```
docker build -t airrohr .
docker run --detach --restart unless-stopped -p 55123:8888 --name airrohr -t airrohr
```

## Links

* [airRohr Sensor Firmware for SPS30, SDS011, DHT22, BMP180, BMP/E 280 and many more](https://github.com/opendata-stuttgart/sensors-software/blob/master/airrohr-firmware/Readme.md)
* [airRohr source code](https://github.com/opendata-stuttgart/sensors-software)
* [airRohr firmware flashing tool](http://firmware.sensor.community/airrohr/flashing-tool/)
