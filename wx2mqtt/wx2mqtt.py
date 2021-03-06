from configparser import SafeConfigParser
import time
import aprslib
import logging
import paho.mqtt.client as mqtt
import string
import random

parser = SafeConfigParser()
parser.read('config.ini')
if parser.get('logging', 'level') == "debug":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# Thanks g0hww for his patient explanations
class extractor:
    def __init__(self, key, topic='unknown', fmt='{0}'):
        self.key = key
        self.topic = 'wx/'+topic+'/{0}'
        self.fmt = fmt

    def extract(self, client, packet):
        if self.key in packet:
            client.publish(self.topic.format(self.key, packet[self.key]),
                           self.fmt.format(packet[self.key]))
            # Crude Rate Limit
            time.sleep(1)
            logging.info('Pushed {} value of {} to MQTT'.format(self.key, packet[self.key]))


def callback(packet):

    logging.debug(packet['raw'])

    if 'weather' in packet:
        if 'from' in packet:
            t = packet['from']
            # Connect to the broker
            client = mqtt.Client(parser.get('mqtt', 'clientname') +randomString(), clean_session=True)
            # Put in some error checking
            client.connect(parser.get('mqtt', 'server'))

            extractors = [extractor("wind_direction", topic=t),
                          extractor("wind_speed", topic=t, fmt="{:3.2f}"),
                          extractor("wind_gust", topic=t, fmt="{:3.2f}"),
                          extractor("temperature", topic=t, fmt="{:-3.2f}"),
                          extractor("rain_1h", topic=t, fmt="{:4.2f}"),
                          extractor("rain_since_midnight", topic=t, fmt="{:4.2f}"),
                          extractor("rain_24h", topic=t, fmt="{:4.2f}"),
                          extractor("humidity", topic=t),
                          extractor("pressure", topic=t)
                          ]
            for thingy in extractors:
                thingy.extract(client, packet['weather'])
            # close the mqtt connection
            client.disconnect()





# Prepare the APRS connection
aprs = aprslib.IS(parser.get('aprs', 'callsign'),
                  parser.get('aprs', 'password'),
                  parser.get('aprs', 'host'),
                  parser.get('aprs', 'port'))

# Listen for specific packet
aprs.set_filter(parser.get('aprs', 'filter'))

# Open the APRS connection to the server
aprs.connect()

# Set a callback for when a packet is received
aprs.consumer(callback)
