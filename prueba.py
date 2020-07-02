from PIL import Image, ImageFilter
import numpy as np
import cv2
  
#Cargamos el archivo con los datos xml del rostro
face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
#Leemos la imagen
img = cv2.imread("test/andres.jpg")
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
    cv2.imwrite("test/recorte.jpg",roi)

if rostrosDetectado == False:
    print("No se detectaron rostros")
else:
    #Proceso de transformación y afinamiento de la imagen
    foto = Image.open("test/recorte.jpg").convert('L')
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
    imagen_nitidez.save("test/recorte.jpg")
    foto.close()
    imagen_nitidez.close()
