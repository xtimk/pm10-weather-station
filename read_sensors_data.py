#!/usr/bin/python
import sys
import Adafruit_DHT
from elasticsearch import Elasticsearch
import yaml
import time
import datetime
import csv
import os
import json
import serial

from dht22 import get_dht22_temperature_c, get_dht22_humidity
from dht11 import get_dht11_temperature_c, get_dht11_humidity
# from sds011 import get_pm25_pm10
from sds011 import Sds011

def configuration_import(filepath):
	## Now reading from config file
	print(" * Reading Config YAML * ")
	config_file = filepath
	try:
		with open(config_file, 'r') as stream:
			try:
				# print(yaml.safe_load(stream))
				config = yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				print(exc)
	except IOError as e:
		print("ERROR: Config file " + filepath + " not found!")
		print("Exiting due to an error.")
		exit(1)

	print(" * DHT11 data pin configured: " + str(config['dht11_data_pin']) )
	print(" * DHT22 data pin configured: " + str(config['dht22_data_pin']) )

	## If not using basic auth for elasticsearch i will call http(s)://es_address
	if config['es_basic_auth'] == 0:
		es_url = config['es_proto'] + "://" + config["es_address"]
		config['es_url'] = es_url
	## If I'm using basic auth i will call http(s)://es_user:es_pass@es_address
	elif config['es_basic_auth'] == 1:
		es_url = config['es_proto'] + "://" + config['es_user'] + ":" + config['es_pass'] + "@" + config["es_address"]
		config['es_url'] = es_url
	## Else case
	else:
		print(" * Error: es_basic_auth must be set to 0 or 1, check config file.")
		exit(1)
	print(" * Elasticsearch destination node: " + config['es_address'])

	es_index_name = config['es_index_name']
	print(" * Elasticsearch destination index: " + es_index_name)
	## End reading from config file
	print(" * Config YAML loaded correctly * ")
	return config

def elasticsearch_connect(es_url):
	## Try to establish Elasticsearch connection
	print(" * Creating elasticsearh handle.. *")
	try:
		es = Elasticsearch(es_url)
		return es
	except Exception as e:
		print(e)
		exit(1)

def elasticsearch_createIfNotExistIndex(es_handle, index_name):
	print(" * Setting elasticsearh index.. *")	
	## Try to create Elasticsearch index, ignoring 400 caused by IndexAlreadyExistsException
	try:
		es_handle.indices.create(index=index_name, ignore=400)
	except Exception as e:
		print(e)

def elasticsearch_index_document(es_handle, index_name, document):
	try:
		res = es_handle.index(index=index_name, body=document)
	except Exception as e:
		print(e)

if __name__ == '__main__':
	## Getting current dir
	cwd = os.path.dirname(os.path.realpath(__file__))

	## Setup log files path
	log_file = cwd + "/log.csv"
	err_log = cwd + "/err_log.csv"
	conf_file = cwd + "/config.yaml"


	config = configuration_import(conf_file)
	es = elasticsearch_connect(config['es_url'])
	elasticsearch_createIfNotExistIndex(es, config['es_index_name'])

	print(" * Reading data from sensors.. * ")
	timestamp = datetime.datetime.utcnow()

	dht22_temperature = get_dht22_temperature_c(config['dht22_data_pin'])
	dht22_humidity = get_dht22_humidity(config['dht22_data_pin'])

	dht11_temperature = get_dht11_temperature_c(config['dht11_data_pin'])
	dht11_humidity = get_dht11_humidity(config['dht11_data_pin'])

	# ser = serial.Serial('/dev/ttyUSB0')
	# ser.port = "/dev/ttyUSB0"
	# ser.baudrate = 9600

	# ser.open()
	# ser.flushInput()

	########## Using Simple Method ##########
	# pm_results = get_pm25_pm10(ser)
	# pm25 = pm_results['pm25']
	# pm10 = pm_results['pm10']
	########## ################### ##########

	pm_sensor = Sds011("/dev/ttyUSB0", use_query_mode=True)
	pm25, pm10 = pm_sensor.get_pm25_pm10()
	# pm25 = pm_results['pm25']
	# pm10 = pm_results['pm10']


	doc = {
		'dht22_temperature': dht22_temperature,
		'dht22_humidity': dht22_humidity,
		'dht11_temperature': dht11_temperature,
		'dht11_humidity': dht11_humidity,
		'sds011_pm25': pm25,
		'sds011_pm10': pm10,
		'timestamp': timestamp
	}
	print(" * Indexing results into elasticsearch.. * ")
	elasticsearch_index_document(es, config['es_index_name'], doc)
	print(" * All Done * ")


	print("\n * ######################## * \n")
	print("----- SENSORS DATA -----")
	print(" * DHT11 Sensor data:")
	print(" * >> Temperature: {0:.2f}°C (±2°C)".format(dht11_temperature))
	print(" * >> Humidity   : {0:.2f} % (±5%)".format(dht11_humidity))
	
	print("------------------------")

	print(" * DHT22 Sensor data:")
	print(" * >> Temperature: {0:.2f}°C (±0.5°C)".format(dht22_temperature))
	print(" * >> Humidity   : {0:.2f} % (±2-5 %)".format(dht22_humidity))

	print("------------------------")

	print(" * SDS011 Sensor data:")
	print(" * >> PM2.5: {0:.2f} µg/m^3 (±)".format(pm25))
	print(" * >> PM10   : {0:.2f} µg/m^3 (±)".format(pm10))

	print("------------------------")
