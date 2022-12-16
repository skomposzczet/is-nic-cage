import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.setup_app()

    def setup_app(self):
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('green')

        self.title('is_nic_cage')
        self.geometry('1200x600')
