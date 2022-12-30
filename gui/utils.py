import PIL
import requests
import shutil
from tempfile import gettempdir
import customtkinter
import cv2
import os


def scaled_image(filename, maxsize):
    image = PIL.Image.open(filename)
    if image.size == maxsize:
        factor = 1
    elif image.width / image.height > maxsize[0] / maxsize[1]:
        factor = maxsize[0] / image.width
    else:
        factor = maxsize[1] / image.height
    return customtkinter.CTkImage(image, size=(image.width * factor, image.height * factor))


def download_image(url):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise Exception('Failed to download file.')

    filename = f'{gettempdir()}/{url.split("/")[-1]}'
    r.raw.decode_content = True
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return filename


class PopupWindow(customtkinter.CTkToplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.message = message

        self.geometry("400x200")
        self.lift()
        self.attributes("-topmost", True)
        self.after(10, self._print_message)
        self.grab_set()
        self.resizable(False, False)

    def _print_message(self):
        label = customtkinter.CTkLabel(self, text=self.message, font=('TkFixedFont', 20))
        label.pack(fill='x', padx=20, pady=40)

        button = customtkinter.CTkButton(self, width=100, text='Ok', command=self._leave)
        button.pack(fill='x', padx=20, pady=20)

    def _leave(self):
        self.grab_release()
        self.destroy()


class ErrorWindow(PopupWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.title('Something went wrong')


class ResultWindow(PopupWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.title('Result')


def detect_image(image, filename):
    path = './Faces'
    for f in os.listdir(path):
        os.remove((os.path.join(path, f)))

    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        extracted_face = img[y:y + h + 1, x:x + w + 1]
        cv2.imwrite('./Faces/' + str(h) + '.jpg', extracted_face)
    return img

