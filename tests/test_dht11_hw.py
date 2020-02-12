import board
import unittest
from dht11 import get_dht11_temperature_c, get_dht11_humidity

data_pin = 4

class BasicDHT11Tests(unittest.TestCase):

	## Check if get_dht22_temperature_c returns a float value
	def test_temperature_celsius_return_type(self):
		result = get_dht11_temperature_c(data_pin)
		self.assertIsInstance(result, float)

	## Check if get_dht22_temperature_c returns temperature t.c
	## -10 <= temperature <= 50
	def test_temperature_celsius_value_in_human_range(self):
		temperature = get_dht11_temperature_c(data_pin)
		result = (temperature >= -10) and (temperature <= 50)
		self.assertTrue(result)

	## Check if get_dht22_humidity returns a float value
	def test_humidity_return_type(self):
		result = get_dht11_humidity(data_pin)
		self.assertIsInstance(result, float)

	## Check if get_dht22_humidity returns a % value:
	## 0 <= humidity <= 100
	def test_humidity_value_in_correct_range(self):
		humidity = get_dht11_humidity(data_pin)
		result = (humidity >= 0) and (humidity <= 100)
		self.assertTrue(result)

if __name__ == '__main__':
	unittest.main()
	# print("Temperature: " + str(get_dht22_temperature_c(data_pin)) + "°C")
	# print("Humidity   : " + str(get_dht22_humidity(data_pin)) + "%")



