from PIL import Image, ImageFilter
 
def tratar_imagen(imagePath):
    foto = Image.open(imagePath).convert('L')
    
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
    imagen_nitidez.save(imagePath)
    
    foto.close()
    imagen_nitidez.close()