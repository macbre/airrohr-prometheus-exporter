# airrohr-prometheus-exporter
This a HTTP server that accepts data sent by [`airrohr` AirQuality monitoring station](https://github.com/Naesstrom/Airrohr-kit) (temperature, pressure and PM metrics) and exposes them to [Prometheus](https://prometheus.io/)' metrics collector. You can then plot them with [Grafana](https://grafana.com/).

## HTTP endpoints

#### `POST /data.php`

[Set up your airrohr station](https://sensor.community/en/sensors/dnms#Configure_the_station) to "Send data to custom API" and provide the IP address and port where `airrohr-prometheus-exporter` runs.

#### Example request

```
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

#### `GET /metrics`

Exposes metrics collected from airrohr stations in Prometheus format.

##### An example

```
# HELP airrohr_info Information about the sensor.
# TYPE airrohr_info gauge
airrohr_info {sensor_id="esp8266-12326597",software="NRZ-2020-129"} 1
# HELP airrohr_bme280_temperature bme280_temperature metric
# TYPE airrohr_bme280_temperature gauge
airrohr_bme280_temperature {sensor_id="esp8266-12326597"} 20.28
# HELP airrohr_bme280_pressure bme280_pressure metric
# TYPE airrohr_bme280_pressure gauge
airrohr_bme280_pressure {sensor_id="esp8266-12326597"} 100166.37
...
```

#### `GET /metrics.json`

Exposes metrics collected from airrohr stations in JSON format.

##### An example

```json
{
  "sensors": [
    {
      "meta": {
        "software_version": "NRZ-2020-129"
      }, 
      "metrics": {
        "bme280_humidity": "57.33", 
        "bme280_pressure": "100166.37", 
        "bme280_temperature": "20.28", 
        "max_micro": "11204", 
        "min_micro": "32", 
        "samples": "4354329", 
        "signal": "-33"
      }, 
      "sensor_id": "esp8266-12326597"
    }, 
    {
      "meta": {
        "software_version": "NRZ-2020-129"
      }, 
      "metrics": {
        "bme280_humidity": "73.07", 
        "bme280_pressure": "100206.13", 
        "bme280_temperature": "16.61", 
        "max_micro": "20407", 
        "min_micro": "33", 
        "samples": "4353673", 
        "sds_p1": "0.60", 
        "sds_p2": "0.40", 
        "signal": "-91"
      }, 
      "sensor_id": "esp8266-12331981"
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
FLASK_ENV=devel PORT=55123 python app.py
curl 0:55123/data.php -H 'X-Sensor: foo' -H 'Content-Type: application/json' -d '{"esp8266id": "12331981", "software_version": "NRZ-2020-129", "sensordatavalues":[{"value_type":"SDS_P1","value":"0.40"},{"value_type":"SDS_P2","value":"0.20"},{"value_type":"BME280_temperature","value":"20.47"},{"value_type":"BME280_pressure","value":"100613.25"},{"value_type":"BME280_humidity","value":"69.02"},{"value_type":"samples","value":"4222662"},{"value_type":"min_micro","value":"32"},{"value_type":"max_micro","value":"3301275"},{"value_type":"signal","value":"-94"}]}'
```
