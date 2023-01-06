import cv2


def detect_face(filename):

    extracted_faces = []

    img = cv2.imread(filename)
    if img is None:
        return extracted_faces

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for x, y, w, h in faces:
        extracted_faces.append(img[y:y + h + 1, x:x + w + 1])

    return extracted_faces
