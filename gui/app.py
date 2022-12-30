import customtkinter
from tkinter import ttk
from tkinter import filedialog
import os
import PIL
import cv2
from .utils import download_image, scaled_image, ErrorWindow, ResultWindow, detect_image


class App(customtkinter.CTk):
    def __init__(self, callback_function):
        super().__init__()
        self.callback = callback_function

        self.setup_app()

        self.setup_sidebar()
        self.setup_main_frame()

        self.setup_buttons()
        self.setup_image()

    def setup_app(self):
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('green')

        self.title('is_nic_cage')
        width, height = 900, 400
        self.geometry(f'{width}x{height}')
        self.minsize(width, height)
        self.font = ('TkFixedFont', 14)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def setup_sidebar(self):
        self.sidebar = customtkinter.CTkFrame(self, width=150)
        self.sidebar.grid(row=0, column=0, padx=10, pady=20, sticky='news')
        self.sidebar.grid_rowconfigure(4, weight=1)

    def setup_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky='news')

    def setup_buttons(self):
        self.create_files_button()
        self.create_web_button()
        self.create_separator()
        self.create_apply_button()
        self.create_exit_button()

    def create_files_button(self):
        self.load_button_files = customtkinter.CTkButton(self.sidebar, text='Load image from files', font=self.font,
                                                         command=self.callback_files)
        self.load_button_files.grid(row=0, padx=20, pady=20, sticky='ew')

    def create_web_button(self):
        self.load_button_web = customtkinter.CTkButton(self.sidebar, text='Load image from web', font=self.font,
                                                       command=self.callback_web)
        self.load_button_web.grid(row=1, padx=20, pady=10, sticky='ew')

    def create_separator(self):
        ttk.Separator(self.sidebar, orient='vertical').grid(row=2, sticky='ew', padx=10, pady=10)

    def create_apply_button(self):
        self.apply_button = customtkinter.CTkButton(self.sidebar, text='CHECK IF CAGE', font=self.font,
                                                    command=self.callback_apply, state='disabled',
                                                    fg_color='SpringGreen4')
        self.apply_button.grid(row=3, padx=20, pady=10, sticky='ew')

    def create_exit_button(self):
        self.exit_button = customtkinter.CTkButton(self.sidebar, text='Exit', font=self.font, fg_color='purple',
                                                   hover_color='dark violet', command=self.leave)
        self.exit_button.grid(row=4, padx=20, pady=20, sticky='sew')

    def callback_files(self):
        filename = filedialog.askopenfilename(initialdir=os.path.expanduser('~'), title='Select image')
        cv2.imwrite('./Faces/detectedImage.jpg', detect_image(cv2.imread(filename), filename))
        if not filename:
            return
        if self.display_image('./Faces/detectedImage.jpg'):
            self.unlock_apply_button()

    def callback_web(self):
        url = customtkinter.CTkInputDialog(text="Paste link to image:", title="Load image from web").get_input()
        if not url:
            return
        try:
            filename = download_image(url)
        except Exception as e:
            ErrorWindow(self, 'Failed to download image')
        else:
            img = cv2.imread(filename)
            cv2.imwrite('./Faces/detectedImage.jpg', detect_image(cv2.imread(filename), filename))
            if self.display_image('./Faces/detectedImage.jpg'):
                self.unlock_apply_button()

    def unlock_apply_button(self):
        self.apply_button.configure(state='normal')

    def callback_apply(self):
        result = self.callback(self.currently_displayed_image)
        ResultWindow(self, result)

    def setup_image(self):
        self.image_label = customtkinter.CTkLabel(self.main_frame, text='')
        self.image_label.pack(padx=30, pady=30)

    def display_image(self, filename):
        try:
            image = scaled_image(filename, maxsize=(500, 300))
            self.image_label.configure(image=image)
        except PIL.UnidentifiedImageError:
            ErrorWindow(self, 'Unrecognized file format')
            return False
        self.currently_displayed_image = filename
        return True

    def leave(self):
        # os.remove('./Faces/detectedImage.jpg')
        self.destroy()
