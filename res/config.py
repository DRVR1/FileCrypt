class Main_Window():
    def __init__(self) -> None:
        #general
        self.menu_title = 'FileCrypt'
        self.menu_sizeX = 600
        self.menu_sizeY = 500
        self.menu_background_color = '#252525'
        #border frame
        self.menu_borderpadding = 3
        self.window_border_size = (self.menu_sizeX+self.menu_borderpadding,self.menu_sizeY+self.menu_borderpadding)
        self.window_border_color = '#1bff00'
        self.window_border_color_alert = '#e20000'
        self.window_borderframe = True
        #title image
        self.titleImage_size = (300,55)
        #buttons
        self.button_X = 120
        self.button_Y = 45
        self.button_fontsize = 20
        self.button_bordersize = 1
        self.button_font = 'comic sans'
        self.button_border_color = '#848484'
        self.button_color = '#000000'
        #clear button
        self.button_clear_X = 120
        self.button_clear_Y = 30
        #info box 
        self.textbox_X = 580
        self.textbox_Y = 230
        self.textbox_fontsize = 15
        self.textbox_font = ''

class Password_input_window(Main_Window):
    #copy config from main window
    def __init__(self) -> None: #The child's __init__() function overrides the inheritance of the parent's __init__() function.
        Main_Window.__init__(self) #To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function:
        self.menu_background_color = '#000000'
        self.password_title_font = ('comic sans',50)
        self.password_entry_size = (800,30)

class Encrypt_Decrypt_Window(Main_Window):
    def __init__(self) -> None:
        Main_Window.__init__(self)
        self.textbox_Y = 330

class files():
    def __init__(self) -> None:
        self.icon = 'res/icon.ico'
        self.font_hi = 'res/HiBlack-n3a1.otf'
        self.title_image = 'res/title.png'
        self.szip='res/7z2201/7za.exe'