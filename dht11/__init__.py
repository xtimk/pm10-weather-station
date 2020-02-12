## New Library Not working with raspberry PI 2
# import adafruit_dht

## Using old deprecated library 4 now..
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

def get_dht11_temperature_c(pin_data):
	humidity, temperature = Adafruit_DHT.read_retry(sensor,pin_data)
	return temperature

def get_dht11_humidity(pin_data):
	humidity, temperature = Adafruit_DHT.read_retry(sensor,pin_data)
	return humidity
