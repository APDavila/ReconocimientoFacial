import cv2

image = cv2.imread('test/andres.jpg')
roi = image[240:375, 215:365]

cv2.imshow('roi', roi)
cv2.imshow('original', image)
cv2.waitKey(0)
cv2.destroyAllWindows()