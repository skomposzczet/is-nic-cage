import customtkinter
from tkinter import ttk

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.setup_app()

        self.setup_sidebar()
        self.setup_main_frame()
        self.setup_buttons()

    def setup_app(self):
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('green')

        self.title('is_nic_cage')
        self.geometry('1200x600')
        self.minsize(900, 400)
        self.font = ('TkFixedFont', 14)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def setup_sidebar(self):
        self.sidebar = customtkinter.CTkFrame(self, width=150)
        self.sidebar.grid(row=0, column=0, padx=10, pady=20, sticky='news')

    def setup_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky='news')

    def setup_buttons(self):
        self.create_files_button()
        self.create_web_button()
        self.create_separator()
        self.create_apply_button()

    def create_files_button(self):
        self.load_button_files = customtkinter.CTkButton(self.sidebar, text='Load image from files', font=self.font, command=self.callback_files)
        self.load_button_files.grid(row=0, padx=20, pady=20, sticky='ew')

    def create_web_button(self):
        self.load_button_web = customtkinter.CTkButton(self.sidebar, text='Load image from web', font=self.font, command=self.callback_web)
        self.load_button_web.grid(row=1, padx=20, pady=10, sticky='ew')

    def create_separator(self):
        ttk.Separator(self.sidebar, orient='vertical').grid(row=2, sticky='ew', padx=10, pady=10)

    def create_apply_button(self):
        self.apply_button = customtkinter.CTkButton(self.sidebar, text='CHECK IF CAGE', font=self.font, command=self.callback_apply, state='disabled', fg_color='SpringGreen4')
        self.apply_button.grid(row=3, padx=20, pady=10, sticky='ew')

    def callback_files(self):
        self.unlock_apply_button()
        print('files')

    def callback_web(self):
        self.unlock_apply_button()
        print('web')
    
    def unlock_apply_button(self):
        self.apply_button.configure(state='normal')

    def callback_apply(self):
        print('apply')