import PIL
import requests
import shutil
from tempfile import gettempdir
import customtkinter

def scaled_image(filename, maxsize):
    image = PIL.Image.open(filename)
    if image.size == maxsize:
        factor = 1
    elif image.width/image.height > maxsize[0]/maxsize[1]:
        factor = maxsize[0]/image.width
    else:
        factor = maxsize[1]/image.height
    return customtkinter.CTkImage(image, size=(image.width*factor, image.height*factor))

def download_image(url):
    r = requests.get(url, stream = True)
    if r.status_code != 200:
        raise Exception('Failed to download file.')

    filename = f'{gettempdir()}/{url.split("/")[-1]}'
    r.raw.decode_content = True
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return filename


class ErrorWindow(customtkinter.CTkToplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.message = message
        
        self.title('Something went wrong')
        self.geometry("400x200")
        self.lift()
        self.attributes("-topmost", True)
        self.after(10)
        self.grab_set()
        self.resizable(False, False)

        self._print_message()

    def _print_message(self):
        label = customtkinter.CTkLabel(self, text=self.message, font=('TkFixedFont', 20))
        label.pack(fill='x', padx=20, pady=40)

        button = customtkinter.CTkButton(self, width=100, text='Ok', command=self._leave)
        button.pack(fill='x', padx=20, pady=20)

    def _leave(self):
        self.grab_release()
        self.destroy()
