# airrohr-prometheus-exporter
This a HTTP server that accepts data sent by [`airrohr` AirQuality monitoring station](https://github.com/Naesstrom/Airrohr-kit) (temperature, pressure and PM metrics) and exposes them to Prometheus metrics collector. You can then plot them with Grafana.

## HTTP endpoints

### `POST /data.php`

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

## `GET /metrics`

Exposes metrics collected from airrohr stations in Prometheus format.

#### Metrics exposed

```
# TODO
```

## `GET /metrics.json`

Exposes metrics collected from airrohr stations in Prometheus format.


### Local development

Start this server locally and make a request using `curl`:

```
FLASK_ENV=devel PORT=55123 python app.py
curl 0:55123/data.php -H 'X-Sensor: foo' -H 'Content-Type: application/json' -d '{"esp8266id": "12331981", "software_version": "NRZ-2020-129", "sensordatavalues":[{"value_type":"SDS_P1","value":"0.40"},{"value_type":"SDS_P2","value":"0.20"},{"value_type":"BME280_temperature","value":"20.47"},{"value_type":"BME280_pressure","value":"100613.25"},{"value_type":"BME280_humidity","value":"69.02"},{"value_type":"samples","value":"4222662"},{"value_type":"min_micro","value":"32"},{"value_type":"max_micro","value":"3301275"},{"value_type":"signal","value":"-94"}]}'
```

### Docker container

```
docker build -t airrohr .
docker run --detach --restart unless-stopped -p 55123:8888 --name airrohr -t airrohr
```
