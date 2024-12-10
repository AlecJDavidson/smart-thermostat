from machine import Pin
import dht
from settings import dht_sensor_pin
 
sensor = dht.DHT11(Pin(dht_sensor_pin))

def get_temp():
  try:
    sensor.measure()
    t = sensor.temperature()
    return t
  except OSError as e:
    print('Temp Sensor Reading Failed')

def get_humidity():
  try:
    sensor.measure()
    h = sensor.humidity()
    return h
  except OSError as e:
    print('Humidity Sensor Reading Failed')
   
