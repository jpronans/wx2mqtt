
from ConfigParser import SafeConfigParser
import logging
import aprslib
import paho.mqtt.publish as mqtt 

parser = SafeConfigParser()
parser.read('config.ini')


def callback(packet):
    if 'from' in packet and 'comment' in packet:
        print packet['from']+' '+packet['comment']
    if 'status' in packet:
	    print packet['status']
    if 'from' in packet:
        print("From {} Direction: {}, Speed {}".format(packet['from'],packet['wind_direction'], packet['wind_speed']))
    if 'wind_gust' in packet:
	  print "gust %d" % packet['wind_gust']
    if 'temp' in packet:
        print "temp %+2.2f" % packet['temp']
	mqtt.single("house/outside/temp",'{:-2.2f}'.format(packet['temp']),hostname="192.168.1.253") 
    if 'rain_1h' in packet:
	    print "rain 1h %+2.2f" % packet['rain_1h']
    if 'rain_24h' in packet:
        print "rain 24h %+2.2f" % packet['rain_24h']
    if 'rain_since_mid' in packet:
	    print "rain since midnight %2.2f" % packet['rain_since_mid']
    if 'humidity' in packet:
	    print "humidity %d" % packet['humidity']
    if 'hPa' in packet:
	    print "pressure %+5.2f" % packet['hPa'] 	  
    print packet['raw']
#  if 'course' in packet:
#	print "Oh oh"

#logging.basicConfig(level=logging.DEBUG)

aprs = aprslib.IS(parser.get('aprs_parms', 'callsign'),
                  parser.get('aprs_parms', 'password'),
                  parser.get('aprs_parms', 'host'),
                  parser.get('aprs_parms', 'port'))

aprs.set_filter(parser.get('aprs_parms', 'filter'))
aprs.connect()
# by default `raw` is False, then each line is ran through aprslib.parse()
aprs.consumer(callback)
