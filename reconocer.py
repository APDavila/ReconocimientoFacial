import cv2
import train, detect, config, imutils, argparse
from os import remove
import pickle
from PIL import Image, ImageFilter
import numpy as np

def RecognizeFace(image, faceCascade, eyeCascade, faceSize, threshold):
    found_faces = []
    recognizer = train.trainRecognizer("train", faceSize, showFaces=True)
    gray, faces = detect.detectFaces(image, faceCascade, eyeCascade, returnGray=1)
    for ((x, y, w, h), eyedim)  in faces:
        label, confidence = recognizer.predict(cv2.resize(detect.levelFace(gray, ((x, y, w, h), eyedim)), faceSize))
        if confidence < threshold:
            found_faces.append((label, confidence, (x, y, w, h)))

    return found_faces

def RecognizeFace(image, faceCascade, eyeCascade, faceSize, threshold):
    found_faces = []
    recognizer = train.trainRecognizer("train", faceSize, showFaces=True)
    gray, faces = detect.detectFaces(image, faceCascade, eyeCascade, returnGray=1)
    for ((x, y, w, h), eyedim)  in faces:
        label, confidence = recognizer.predict(cv2.resize(detect.levelFace(gray, ((x, y, w, h), eyedim)), faceSize))
        if confidence < threshold:
            found_faces.append((label, confidence, (x, y, w, h)))

    return found_faces

def validacionRecorteRostro(imgPath):
    #Cargamos el archivo con los datos xml del rostro
    face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
    #Leemos la imagen
    img = cv2.imread(imgPath)
    rostrosDetectado=False
    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    array_rostros = face_cascade.detectMultiScale(img_gris, 1.3, 5)
    #Detectamos si existen rostros 
    for (x,y,w,h) in array_rostros:
        #Bandera que indica si existen rostros o no
        rostrosDetectado = True
        cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)
        roi = img[y:y+h,x:x+w]
        #Guardamos la imagen con el rostro recortado 
        cv2.imwrite(imgPath,roi)

    if rostrosDetectado == False:
        return("Error")
    else:
        #Proceso de transformación y afinamiento de la imagen
        foto = Image.open(imgPath).convert('L')
        #Laplace
        coeficientes = [1, 1, 1, 1, -8, 1, 1, 1, 1]
        datos_laplace = foto.filter(ImageFilter.Kernel((3,3), coeficientes, 1)).getdata()
        #datos de la imagen
        datos_imagen = foto.getdata()
        #factor de escalado
        w = 1 / 5
        #datos de imagen menos datos de Laplace escalados
        datos_nitidez = [datos_imagen[x] - (w * datos_laplace[x]) for x in range(len(datos_laplace))]
        imagen_nitidez = Image.new('L', foto.size)
        imagen_nitidez.putdata(datos_nitidez)
        imagen_nitidez.save(imgPath)
        foto.close()
        imagen_nitidez.close()
        return ("Succesfully")


def deteccionRostro(imgPath):
    nombre = "No se detectaron rostros"
    cascPath = "cascades/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    eyeCascade = cv2.CascadeClassifier("cascades/haarcascade_eye.xml")
    smileCascade = cv2.CascadeClassifier("cascades/haarcascade_smile.xml")
    reconocimiento = cv2.face.LBPHFaceRecognizer_create()
    reconocimiento.read("entrenamiento.yml")

    etiquetas = {"nombre_persona" : 1 }
    with open("labels.pickle",'rb') as f:
        pre_etiquetas = pickle.load(f)
        etiquetas = { v:k for k,v in pre_etiquetas.items()}

    
    # Capture el marco
    marco = cv2.imread(imgPath)
    grises = cv2.cvtColor(marco, cv2.COLOR_BGR2GRAY)    
    rostros = faceCascade.detectMultiScale(grises, 1.5, 5)
    print(imgPath)
    # Dibujar un rectángulo alrededor de los rostros
    for (x, y, w, h) in rostros:
        roi_gray = grises[y:y+h, x:x+w]
        roi_color = marco[y:y+h, x:x+w]

        # reconocimiento
        id_, conf = reconocimiento.predict(roi_gray)
        print(conf)
        if conf >= 4  and conf < 85:
                    
            font = cv2.FONT_HERSHEY_SIMPLEX            

            nombre = etiquetas[id_]
            if conf >50:
                print("entra en el desconocido")
                #print(conf)
                nombre = "Desconocido"
            

            color = (248,25,25)
            grosor = 1
            cv2.putText(marco, nombre, (x,y), font, 1, color, grosor, cv2.LINE_AA)
            

        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_gray)
        
        cv2.rectangle(marco, (x, y), (x+w, y+h), (168, 25, 25), 2)

        rasgos = smileCascade.detectMultiScale(roi_gray)
        for(ex,ey,ew,eh) in rasgos:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (168, 25, 25), 2)

    # Marco
    marco_display = cv2.resize(marco, (600, 350), interpolation = cv2.INTER_CUBIC)
    cv2.imshow('Detectando Rostros', marco_display)
    #Al momento de capturar liberamos
    cv2.destroyAllWindows()
    return nombre


