import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.setup_app()

        self.setup_sidebar()
        self.setup_main_frame()

    def setup_app(self):
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('green')

        self.title('is_nic_cage')
        self.geometry('1200x600')
        self.minsize(900, 400)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def setup_sidebar(self):
        self.sidebar = customtkinter.CTkFrame(self, width=150)
        self.sidebar.grid(row=0, column=0, padx=10, pady=20, sticky='news')

    def setup_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky='news')
