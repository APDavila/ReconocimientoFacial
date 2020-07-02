import cv2
import pickle
import time
 


cascPath = "Cascades/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

eyeCascade = cv2.CascadeClassifier("Cascades/haarcascade_eye.xml")
smileCascade = cv2.CascadeClassifier("Cascades/haarcascade_smile.xml")

reconocimiento = cv2.face.LBPHFaceRecognizer_create()
reconocimiento.read("entrenamiento.yml")

etiquetas = {"nombre_persona" : 1 }
with open("labels.pickle",'rb') as f:
    pre_etiquetas = pickle.load(f)
    etiquetas = { v:k for k,v in pre_etiquetas.items()}

web_cam = cv2.VideoCapture(0)
option = True
while option:
    # Capture el marco
    ret, marco = web_cam.read()
    grises = cv2.cvtColor(marco, cv2.COLOR_BGR2GRAY)    
    rostros = faceCascade.detectMultiScale(grises, 1.5, 5)

    # Dibujar un rectángulo alrededor de las rostros
    for (x, y, w, h) in rostros:
        roi_gray = grises[y:y+h, x:x+w]
        roi_color = marco[y:y+h, x:x+w]

        # reconocimiento
        id_, conf = reconocimiento.predict(roi_gray)
        if conf >= 4  and conf < 85:
                    
            font = cv2.FONT_HERSHEY_SIMPLEX            

            nombre = etiquetas[id_]

            if conf < 50:
               print (etiquetas[id_])
               option = True

            if conf > 50:
                #print(conf)
                nombre = "Desconocido"

            color = (248,25,25)
            grosor = 1
            cv2.putText(marco, nombre, (x,y), font, 1, color, grosor, cv2.LINE_AA)
            

        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_gray)
        

    
    # Marco
    marco_display = cv2.resize(marco, (1200, 650), interpolation = cv2.INTER_CUBIC)
    cv2.imshow('Detectando Rostros', marco_display)

    if cv2.waitKey(1) &  0x00 == ord('q'):
        break

#Al momento de capturar liberamos
cv2.destroyAllWindows()