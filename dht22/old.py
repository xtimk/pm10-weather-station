import board
import adafruit_dht

def get_dht22_temperature_c(pin_data):
	temperature_c = -99
	try:
		dhtDevice = adafruit_dht.DHT22(pin_data)
		temperature_c = dhtDevice.temperature
	except Exception as e:
		print(e)
	return temperature_c

def get_dht22_humidity(pin_data):
	try:
		dhtDevice = adafruit_dht.DHT22(pin_data)
		humidity = dhtDevice.humidity
	except Exception as e:
		print(e)
	return humidity
