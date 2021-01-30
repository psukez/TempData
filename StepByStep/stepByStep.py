import wget 
import csv
import json
import os
import commands
import subprocess as cmd

#borrado de csv antiguo y descarga del nuevo
cmd.call("rm paso.csv",shell=True)
url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto74/paso_a_paso.csv"
wget.download(url, '/home/pi/Code/TempData/StepByStep/paso.csv')

#funcion que chequea estado del archivo
def file_accessible(filepath, mode):
    try:
        f = open(filepath, mode)
    except IOError as e:
        return False
    return True 
    
#variables    
data = []
titulo = "comunas"
Var1 = "Santiago"
Var2 = "El Bosque"
Var3 = "Concepcion"
Var4 = "Calama"
Santiago = "13101"
ElBosque = "13105"
Concepcion = "8101"
Calama = "2201"
EstadoVar1 = "1"
EstadoVar2 = "1"
EstadoVar3 = "1"
EsradoVar4 = "1"
tiempo = "fecha"

#acceso y lectura de archivo csv al array data
file1="/home/pi/Code/TempData/StepByStep/paso.csv"
Csvfile = file_accessible(file1, "r")
if Csvfile:
    with open (file1) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
tiempo = data[0][-1]

#Busca cada comuna en el array data y obtiene el ultimo estado
comuna = Santiago
col = [x[2] for x in data]
if comuna in col:
    for x in range(0,len(data)):
        if comuna == data[x][2]:
            EstadoVar1 = data[x][-1] 

comuna = ElBosque
col = [x[2] for x in data]
if comuna in col:
    for x in range(0,len(data)):
        if comuna == data[x][2]:
            EstadoVar2 = data[x][-1] 

comuna = Concepcion
col = [x[2] for x in data]
if comuna in col:
    for x in range(0,len(data)):
        if comuna == data[x][2]:
            EstadoVar3 = data[x][-1] 

comuna = Calama
col = [x[2] for x in data]
if comuna in col:
    for x in range(0,len(data)):
        if comuna == data[x][2]:
            EstadoVar4 = data[x][-1] 

#verificacion del archivo Json
file2="/home/pi/Code/TempData/StepByStep/gauge.json"
JsonFile = file_accessible(file2, "r")

#modificacion archivo Json
if JsonFile:
    with open(file2, "r+") as newEntry:
        data_line = json.load(newEntry)
        
# Borrado de dato mas antiguo
        while len(data_line["gauge"]["datasequences"][0]["datapoints"])>2:
         del data_line["gauge"]["datasequences"][0]["datapoints"][0]
        while len(data_line["gauge"]["datasequences"][1]["datapoints"])>2:
            del data_line["gauge"]["datasequences"][1]["datapoints"][0]
        while len(data_line["gauge"]["datasequences"][2]["datapoints"])>2:
            del data_line["gauge"]["datasequences"][2]["datapoints"][0]
        while len(data_line["gauge"]["datasequences"][3]["datapoints"])>2:
            del data_line["gauge"]["datasequences"][3]["datapoints"][0]
            
# Ingreso de datos nuevos
        data_line["gauge"]["datasequences"][0]["datapoints"].append({u'title':tiempo,u'value':EstadoVar1})
        newEntry.seek(0) 
        newEntry.write(json.dumps(data_line,indent=3,separators=(',', ': ')))
        newEntry.truncate()
        
        data_line["gauge"]["datasequences"][1]["datapoints"].append({u'title':tiempo,u'value':EstadoVar2})
        newEntry.seek(0) 
        newEntry.write(json.dumps(data_line,indent=3,separators=(',', ': ')))
        newEntry.truncate()
        
        data_line["gauge"]["datasequences"][2]["datapoints"].append({u'title':tiempo,u'value':EstadoVar3})
        newEntry.seek(0) 
        newEntry.write(json.dumps(data_line,indent=3,separators=(',', ': ')))
        newEntry.truncate()
        
        data_line["gauge"]["datasequences"][3]["datapoints"].append({u'title':tiempo,u'value':EstadoVar4})
        newEntry.seek(0) 
        newEntry.write(json.dumps(data_line,indent=3,separators=(',', ': ')))
        newEntry.truncate()
#creacion de archivo Json en caso de que no exista 
else:
    EstadoVar1 = "5"
    EstadoVar2 = "5"
    EstadoVar3 = "5"
    EstadoVar4 = "5"
    with open(file2, "w") as newEntry:
        newEntry.write (json.dumps({'gauge':{'title':titulo,'datasequences':[
           {'title':Var1,'datapoints':[
               {'title':tiempo,'value':EstadoVar1}]},
           {'title':Var2,'datapoints':[
               {'title':tiempo,'value':EstadoVar2}]},
           {'title':Var3,'datapoints':[
               {'title':tiempo,'value':EstadoVar3}]},
           {'title':Var4,'datapoints':[
               {'title':tiempo,'value':EstadoVar4}]},
        ]}}, indent=3,separators=(',', ': ')))
        

