# wx2mqtt

A small program for connecting to the APRS-IS backbone using https://github.com/rossengeorgiev/aprs-python and http://www.eclipse.org/paho/

## Config file

    [aprs] 
    callsign = wx2mqtt
    password = -1
    host = rotate.aprs2.net
    port = 14580
    # See http://www.aprs-is.net/javAPRSFilter.aspx
    filter = t/w

    [mqtt]
    server = 127.0.0.1

# MQTT
It publishes to the MQTT topic ``wx/<received callsign>/<defined extractor>``. Each extractor is the key  of a key value pair that can be returned by the aprs-python library. 


