import cv2
import os
import errno
from os import remove
from os import path

#Utilizando la camara por
web_cam = cv2.VideoCapture(0)

cascPath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

count = 0

print("¿Con que nombre desea guardar al nuevo usuario?")
nombre = input()



try:
    os.mkdir("."+"/imagenes/"+nombre)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


while(True):
    
    _, imagen_marco = web_cam.read()

    grises = cv2.cvtColor(imagen_marco, cv2.COLOR_BGR2GRAY)

    rostro = faceCascade.detectMultiScale(grises, 1.5, 5)

    for(x,y,w,h) in rostro:
        cv2.rectangle(imagen_marco, (x,y), (x+w, y+h), (255,0,0), 4)
        count += 1
       
        cv2.imwrite("imagenes/"+nombre+"/"+nombre+"_"+str(count)+".jpg", imagen_marco[y:y+h, x:x+w])
        cv2.imshow("Capturando rostro de usuario "+nombre, imagen_marco)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    elif count >= 100:
        break


# Cuando todo está hecho, liberamos la captura
web_cam.release()

if path.exists("./entrenamiento.yml"):
    remove("./entrenamiento.yml")
if path.exists("./labels.pickle"):
    remove("./labels.pickle")

os.system("entrenamientoCamara.py")
cv2.destroyAllWindows()

