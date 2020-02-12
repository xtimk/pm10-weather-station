# Particulate Raspberry Pi Station
Python based batch software that collects Temperature Humidity PM2.5 and PM10 from sensors and stores them in an Elasticsearch instance.

## What do you need to run this project
 - A `Raspberry Pi`. Project was tested on a `RPi 2`, but it should be compatible with `RPi 3` and `4`)
 - `DHT11` or `DHT22` (or both if you want) temperature & humidity sensors. 
I would recommend the `DHT22`  since it's far more precise than `DHT11`. You may also need a `10K Ohm` resistor if you have the standalone modules.
 - `SDS011` pm2.5 and pm10 sensor. In this project you will attach this sensor to an usb port of the RPi


## Wiring Raspberry with DHT11/DHT22
`DHT11/DHT22` are distributed in two versions:
 - A PCB module mounted with 3 pins. You don't need any extra resistor because it's included in the PCB
 - A standalone module with 4 pins. If you have this you also need a `10K Ohm` resistor.

Below are shown two examples configured to use `pin 4` as data, but you can use any pin data you want.


#### Example of wiring the PCB module:
![3 Pin Configuration](docs/images/3pin-dht11.png)


#### Here is an example of wiring the standalone module:
![4 Pin Configuration](docs/images/4pin-dht11.png)


You can find the detailed description about wiring raspberry with the `DHT11/DHT22` on [circuitbasics.com](http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/)

## Prerequisites
You will need `python3` on your RPi in order to run this project.
To install the required libraries you can run
```bash
pip3 install -r requirements.txt
```
## Configuration
You can set your elasticsearch instance in the `config.yaml` file. It is also supported elasticsearch instance with basic authentication.

Example:
```bash
## Config
#### PIN CONFIGURATION
## Set here data pins used by the dht11 and dht22 sensors
dht11_data_pin: 4
dht22_data_pin: 17

#### Usb port where SDS001 is attached
## Set here the right device where SDS011 is attached
## Hint: you can use "dmesg | grep usb" and find something like:
## [17.383277] usb 1-1.2: ch341-uart converter now attached to ttyUSB0
sds011_serial_port: "/dev/ttyUSB0"


#### ELASTICSEARCH OUTPUT
## set here elasticsearch address. Include also the port
es_address: "my-es-instance:9200"
es_proto: "http"

## set this to 0 if you're not enabled auth in your es cluster
## set this to 1 if you're using basic auth
es_basic_auth: 1

## set elasticsearch user and password
es_user: "elastic"
es_pass: "MYNASASECRETEPASSWORD"

## set elasticsearch index name
es_index_name: "my-pm10-station"
```
## Testing Sensors
You can run all tests to verify that all sensors are ok:
```bash
./run_tests.sh
```
If it's all ok the output should look like:
```bash
Starting tests...
........
----------------------------------------------------------------------
Ran 8 tests in 11.869s

OK
```

## Run the Project

You can run the project once by executing
```bash
python 3 read_sensors_data.py
```

This will measure temperature humidity pm2.5 and pm10, index them to Elasticsearch, and print to console all these values
```bash
----- SENSORS DATA -----
* DHT11 Sensor data:
* >> Temperature: 6.00°C (±2°C)
* >> Humidity : 50.00 % (±5%)
------------------------
* DHT22 Sensor data:
* >> Temperature: 6.70°C (±0.5°C)
* >> Humidity : 67.30 % (±2-5 %)
------------------------
* SDS011 Sensor data:
* >> PM2.5: 35.30 µg/m^3 (Rel. Error: 10%)
* >> PM10 : 58.10 µg/m^3 (Rel. Error: 10%)
------------------------
```

The `read_sensors_data.py` is intended to be run every `x` minutes. 
Assuming you have cloned the repo in `/root` we can for example setup `cron` in order to gather sensors data every 2 minutes
Open crontab
```bash
crontab -e
```
And add the following line
```bash
*/2 * * * *  root  python3 /root/pm10-weather-station/read_sensors_data.py
```
