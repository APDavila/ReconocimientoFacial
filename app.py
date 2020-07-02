import numpy as np
from flask import Flask, render_template, url_for, jsonify, request
from products import products
from io import BytesIO
from PIL import Image
import base64
import json
import PIL, requests
import skimage.io
from os import remove
import os
from reconocer import deteccionRostro,validacionRecorteRostro
from dataBaseService import Database
from tratamiento_imagen import tratar_imagen

app = Flask(__name__)
url = 'https://www.quo.es/wp-content/uploads/2019/10/descubren-quince-de-los-genes-que-dan-forma-al-rostro-humano-1024x640.jpg'
respuesta  = requests.get(url)
imagen = Image.open(BytesIO(respuesta.content))
imagen = imagen.resize([500,300])
imagen_arreglo = np.asarray(imagen)
imagen_original = PIL.Image.fromarray(np.uint8(imagen_arreglo))

@app.route('/')
def index():
    return jsonify({"methods": [ { "id" : "01" , "name" : "register_request" },{"id":"02", "name":"recognition_request"}]})
    



def validateDir(path):
    if os.path.isdir(path):
        print('EL DIRECTORIO YA EXISTE.')
    else:
        os.mkdir(path)
        print("DIRECTORIO CREADO")

def saveUserInTable(nombre,apellido,tipoDocumento,numDocumento,telefono,direccion,email):
    return Database.insert_user(nombre,apellido,tipoDocumento,numDocumento,telefono,direccion,email)
        

def proccessUser(nombre,apellido,tipoDocumento,numDocumento,telefono,direccion,email,base64_1,base64_2,base64_3):
    idInserted = saveUserInTable(nombre,apellido,tipoDocumento,numDocumento,telefono,direccion,email)
    im = Image.open(BytesIO(base64.b64decode(base64_1)))
    im_2 = Image.open(BytesIO(base64.b64decode(base64_2)))
    im_3 = Image.open(BytesIO(base64.b64decode(base64_3)))
    dir = "train/"+str(idInserted)+"_"+nombre+apellido
    validateDir(dir)
    im.save("train/"+str(idInserted)+"_"+nombre+apellido+"/"+nombre + "pattern1.jpg")
    if validacionRecorteRostro("train/"+str(idInserted)+"_"+nombre+apellido+"/"+nombre + "pattern1.jpg") == "Succesfully":
        print("imagen procesada con éxito")
    else:
        Database.delete_user(idInserted)
        return ("Error")
    im_2.save("train/"+str(idInserted)+"_"+nombre+apellido+"/"+nombre + "pattern2.jpg")
    if validacionRecorteRostro("train/"+str(idInserted)+"_"+nombre+apellido+"/"+nombre + "pattern2.jpg") == "Succesfully":
        print("imagen procesada con éxito")
    else:
        Database.delete_user(idInserted)
        return ("Error")
    im_3.save("train/"+str(idInserted)+"_"+nombre+apellido+"/"+nombre + "pattern3.jpg")
    if validacionRecorteRostro("train/"+str(idInserted)+"_"+nombre+apellido+"/"+nombre + "pattern3.jpg") == "Succesfully":
        print("imagen procesada con éxito")
    else:
        Database.delete_user(idInserted)
        return ("Error")
    return idInserted
    
@app.route('/facial_recognition/register_request', methods=['POST'])
def register():
    #Procesamos los archivos recibidos desde el cliente
    idInserted=proccessUser(request.json['nombre'],request.json['apellido'],request.json['tipo_documento'],request.json['num_documento'],request.json['telefono'],request.json['direccion'],request.json['email'],request.json['image'],request.json['image_2'],request.json['image_3'])
    if idInserted == "Error":
        return json.dumps("'error':'no se proceso el registro'")    
    else:
        #Ejecutamos el algoritmo  de entrenamiento con los nuevos datos
        os.system("entrenamiento.py")
        result = {"id":idInserted,"nombre":request.json['nombre'],"apellido":request.json['apellido'],
        "tipo_documento":request.json['tipo_documento'],"num_documento":request.json['num_documento'],
        "direccion":request.json['direccion'],"telefono":request.json['telefono'],
        "email":request.json['email'],"message":"User registered",}
        return json.dumps(result)
    
@app.route('/facial_recognition/recognition_request', methods=['POST']) 
def recognition():
    base64_string = request.json['image']
    im = Image.open(BytesIO(base64.b64decode(base64_string)))
    im.save("test/temp.jpg") 
    tratar_imagen("test/temp.jpg")
    retorno = deteccionRostro("test/temp.jpg")
    #remove("test/temp.jpg")    
    if retorno!="Not found":
        return retorno
    else:
        return jsonify({"error":"User not found"})

@app.route('/facial_recognition/test', methods=['POST'])
def test():
    return "TEST"   

if __name__ =="__main__":
    #app.run(host="172.20.10.38",debug=True, port=5000)
    app.run(debug=True, port=5000)

