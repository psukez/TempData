import json, sys, os, time
from pprint import pprint
from subprocess import call
import paho.mqtt.client as mqtt
import datetime
global strtemp
global strhum
global valorTemp
global valorHum

def file_accessible(filepath, mode):
    #Check if a file exists and is accessible.
    try:
        f = open(filepath, mode)
    except IOError as e:
        return False
    #print "File Ok"
    return True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print ("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("recamara/luz/principal/sonoff/tele/SENSOR")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print (msg.topic+" "+str(msg.payload))
    file="/home/pi/Code/TempData/temp2.json"
    eFile = file_accessible(file, "r")
    titulo = "Recamara"
    grafVar1 = "Temperatura"
    color1 = "red"
    grafVar2 = "Humedad"
    color2 = "blue"
    minVal = 15
    #tiempofinal= (datetime.datetime.now()) #- datetime.timedelta(minutes=1))
    #print tiempofinal.strftime("%H:%M")
    tiempo=(time.strftime("%H:%M"))   #tiempofinal.strftime("%H")+ ":00"
    if eFile:
      with open(file, "r+") as newEntry:
       data_line = json.load(newEntry)
       #print len(data_line["graph"]["datasequences"][0]["datapoints"])
       #print len(data_line["graph"]["datasequences"][1]["datapoints"])
       while len(data_line["graph"]["datasequences"][0]["datapoints"])>12:
        del data_line["graph"]["datasequences"][0]["datapoints"][0]
       while len(data_line["graph"]["datasequences"][1]["datapoints"])>12:
        del data_line["graph"]["datasequences"][1]["datapoints"][0]
        #del data_line["graph"]["datasequences"][1]["datapoints"][1]
       #print len(data_line["graph"]["datasequences"][0]["datapoints"])
       #print len(data_line["graph"]["datasequences"][1]["datapoints"])
       if (msg.topic ==  "recamara/luz/principal/sonoff/tele/SENSOR"):
        strtemp = str(msg.payload)
        positionTemp=strtemp.index('Temperature')
        valorTemp = strtemp[positionTemp+13:positionTemp+17]
       # print (valorTemp)
        data_line["graph"]["datasequences"][0]["datapoints"].append({u'title':tiempo,u'value':valorTemp})
        newEntry.seek(0)
        newEntry.write(json.dumps(data_line,indent=3,separators=(',', ': ')))
        newEntry.truncate()
       if (msg.topic ==  "recamara/luz/principal/sonoff/tele/SENSOR"):
        strhum = str(msg.payload)
        positionHum=strtemp.index('Humidity')
        valorHum = strtemp[positionHum+10:positionHum+14]
       # print (valorHum)
        data_line["graph"]["datasequences"][1]["datapoints"].append({u'title':tiempo,u'value':valorHum})
        newEntry.seek(0)
        newEntry.write(json.dumps(data_line,indent=3,separators=(',', ': ')))
        newEntry.truncate()

    else:
      valorTemp=0
      valorHum=0
      with open(file, "w") as newEntry:
       newEntry.write (json.dumps({'graph':{'title':titulo,'type':"line",'yAxis':{'minValue':minVal},'datasequences':[{'title':grafVar1,'color':color1,'datapoints':[{'title':tiempo,'value':valorTemp}]},{'title':grafVar2,'color':color2,'datapoints':[{'title':tiempo,'value':valorHum}]}]}}, indent=3,separators=(',', ': ')))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.133", 1883, 60)
client.loop_start()
time.sleep (180)
client.loop_stop(force=False)
