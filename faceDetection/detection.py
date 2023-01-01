import os
import cv2


def detect_face(filename):
    path = './faces/'
    for f in os.listdir(path):
        os.remove((os.path.join(path, f)))

    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for value, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        extracted_face = img[y:y + h + 1, x:x + w + 1]
        cv2.imwrite(path + str(value) + '.jpg', extracted_face)
    return img
