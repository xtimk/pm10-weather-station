## New Library Not working with raspberry PI 2
# import adafruit_dht

## Using old deprecated library 4 now..
import Adafruit_DHT

def get_dht22_temperature_c(pin_data):
	humidity, temperature = Adafruit_DHT.read_retry(22,pin_data)
	return temperature

def get_dht22_humidity(pin_data):
	humidity, temperature = Adafruit_DHT.read_retry(22,pin_data)
	return humidity
