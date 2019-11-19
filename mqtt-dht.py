#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import time
import Adafruit_DHT
from configparser import ConfigParser
import sys

config = ConfigParser(delimiters=('=', ))
config.read(sys.path[0] + '/config.ini')

sensor_type = config['sensor'].get('type', 'dht22').lower()

if sensor_type == 'dht22':
    sensor = Adafruit_DHT.DHT22
elif sensor_type == 'dht11':
    sensor = Adafruit_DHT.DHT11
elif sensor_type == 'am2302':
    sensor = Adafruit_DHT.AM2302
else:
    raise Exception('Supported sensor types: DHT22, DHT11, AM2302')

pin = config['sensor'].get('pin', 10)
topic = config['mqtt'].get('topic', 'temperature/dht22')
decim_digits = config['sensor'].getint('decimal_digits', 2)
sleep_time = config['sensor'].getint('interval', 60)
qos = config['mqtt'].getint('qos', 0)
retain = config['mqtt'].getboolean('retain', 'false')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))

client = mqtt.Client(client_id=config['mqtt'].get('clientid',''))
client.on_connect = on_connect
client.username_pw_set(config['mqtt'].get('username',''),config['mqtt'].get('password',''))
client.connect(config['mqtt'].get('hostname', 'homeassistant'),
               config['mqtt'].getint('port', 1883))
client.loop_start()

while True:

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:

        #client.publish(topic + '/temperature', round(temperature, decim_digits))
        #client.publish(topic + '/humidity', round(humidity, decim_digits))
        client.publish(topic + '/temperature', temperature, qos, retain)
        client.publish(topic + '/humidity', humidity, qos, retain)
        
        print('Published. Sleeping ...')
    else:
        print('Failed to get reading. Skipping ...')

    time.sleep(sleep_time)
