# PULSOID Exporter
This is a simple exporter for [PULSOID](https://pulsoid.net) or [Stromno](https://stromno.com) to use with [Prometheus](https://prometheus.io/).
You can use it to monitor your heart rate like geek. 

## Usage
### without Docker
Clone the repository and run the exporter with the following command:
```bash
git clone https://github.com/soumt-r/pulsoid-exporter.git
cd pulsoid-exporter
```

```bash
pip install -r requirements.txt
python3 exporter.py -u wss://ramiel.pulsoid.net/listen/{pulsoid_or_stromno_widget_key} -n {metric_name}
```

### with Docker
```bash
docker run -p 8000:8000 -e METRIC_HR_URL=wss://ramiel.pulsoid.net/listen/{pulsoid_or_stromno_widget_key} -e METRIC_HR_NAME={metric_name} -d --name pulsoid-exporter soumt/pulsoid-exporter
```