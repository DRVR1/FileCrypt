#proyect started 6/2/2023 (d m yyyy) 

#importing required modules
import tkinter
import customtkinter
from res import config
from PIL import Image,ImageTk
import funcs
from tkinter.messagebox import askquestion
from tkinter import ttk
#==================================================================|gui|======================================================================================================
#config objects
files = config.files()

#if compiled with nuitka or pyinstaller, look for the new paths
if funcs.isFrozen():
    files.title_image = funcs.resource_path(files.title_image)
    files.icon = funcs.resource_path(files.icon)
    files.szip = funcs.resource_path(files.szip)
else:
    print('not frozen')

#create the main window
def window_main():
    #load config
    wind = config.Main_Window()

    #main window
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue") 
    app = customtkinter.CTk() 
    app.title(wind.menu_title)
    app.resizable(0,0)
    extsize = (wind.menu_sizeX+wind.menu_borderpadding,wind.menu_sizeY+wind.menu_borderpadding)
    app.minsize(extsize[0],extsize[1])
    app.iconbitmap(files.icon)

    #create a border for the app to look nice (is a bigger frame behind the main frame)
    if wind.window_borderframe:
        extframe = customtkinter.CTkFrame(
            master=app,
            width=extsize[0], 
            height=extsize[1],
            bg_color=wind.window_border_color,
            fg_color=wind.window_border_color
            )
        extframe.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)


    #creating custom frame (main frame)
    frame=customtkinter.CTkFrame(
        master=app, 
        width=wind.menu_sizeX,
        height=wind.menu_sizeY,
        fg_color=wind.menu_background_color
        )

    frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

    #title (since fonts are tricky, let's just put a nice image with a nice font as title)
    #font made by: Mew Too, Robert Jablonski  https://www.fontspace.com/hi-font-f21431
    im0 = Image.open(files.title_image).resize((wind.titleImage_size))
    im1 = ImageTk.PhotoImage(im0)
    tit = customtkinter.CTkLabel(master=frame,image=im1,text='',width=3)
    tit.place(rely=0.1,relx=0.5,anchor=tkinter.CENTER)

    #info box
    inf = customtkinter.CTkTextbox(
        state='disabled',
        master=frame,
        width=wind.textbox_X,
        height=wind.textbox_Y,
        font=(wind.textbox_font,wind.textbox_fontsize)
        )
    inf.place(rely=0.7,relx=0.5,anchor=tkinter.CENTER)

    #tell the writter where the info box is!
    funcs.wr.create(inf)
    #now we can print the output in the infobox from other modules!!

    #ask to generate keys with a password
    #cases when user wants to generate a key pair:
    # 1 without password
    # 2 with new password
    # 3 already has password
    # 4 already has password but wants another one
    # 5 already has password and wants no password
    def askWithPassword():
        if(funcs.keys.password): 
            res = askquestion(title='FileCrypt',message='A password was already loaded, do you want to reuse it?')
            if res == 'yes': # 3
                funcs.keys.savekeys()
                pass
            else:
                funcs.keys.password = ''
                funcs.wr.write('password removed.')
                extframe.configure(fg_color=wind.window_border_color)
                #ask if create new password
                res = askquestion(title='FileCrypt',message='Create another password?')
                if res=='yes': #4
                    window_passwordInput(app,extframe) 
                else: #5
                    funcs.keys.savekeys()
                    pass
        else:
            res = askquestion(title='FileCrypt',message='Protect your private key with a password?')
            if res=='yes':# 2 generate new password
                window_passwordInput(app,extframe) 
            else:# 1 without password
                funcs.keys.savekeys() 
                pass

    #Generate Keys
    but = customtkinter.CTkButton(
        master=frame,
        width=wind.button_X,
        height=wind.button_Y,
        text='Generate New Keys',
        fg_color=wind.button_color,
        font=(wind.button_font,wind.button_fontsize),
        border_color=wind.button_border_color,
        border_width=wind.button_bordersize,
        command= askWithPassword
        )

    but.place(rely=0.25,relx=0.5,anchor=tkinter.CENTER)


    def askEncrypt():
        #place a new frame to overlap other widgets
        frame = customtkinter.CTkFrame(master=app,fg_color=wind.menu_background_color,width=wind.menu_sizeX,height=wind.menu_sizeY)
        frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        def back(*args):
            for widget in args:
                widget.destroy()

        #button encrypt
        but = customtkinter.CTkButton(
            master=frame,
            width=wind.button_X,
            height=wind.button_Y,
            text='Encrypt',
            fg_color=wind.button_color,
            font=(wind.button_font,wind.button_fontsize),
            border_color=wind.button_border_color,
            border_width=wind.button_bordersize,
            )
        but.place(rely=0.2,relx=0.5,anchor=tkinter.CENTER)

        #button decrypt
        but = customtkinter.CTkButton(
            master=frame,
            width=wind.button_X,
            height=wind.button_Y,
            text='Decrypt',
            fg_color=wind.button_color,
            font=(wind.button_font,wind.button_fontsize),
            border_color=wind.button_border_color,
            border_width=wind.button_bordersize,
            )
        but.place(rely=0.24,relx=0.5,anchor=tkinter.CENTER)
        #button Select files
        but = customtkinter.CTkButton(
            master=frame,
            width=wind.button_X,
            height=wind.button_Y,
            text='Select files',
            fg_color=wind.button_color,
            font=(wind.button_font,wind.button_fontsize),
            border_color=wind.button_border_color,
            border_width=wind.button_bordersize,
            )
        but.place(rely=0.3,relx=0.5,anchor=tkinter.CENTER)

        #button select folders
        but = customtkinter.CTkButton(
            master=frame,
            width=wind.button_X,
            height=wind.button_Y,
            text='Select folders',
            fg_color=wind.button_color,
            font=(wind.button_font,wind.button_fontsize),
            border_color=wind.button_border_color,
            border_width=wind.button_bordersize,
            )
        but.place(rely=0.4,relx=0.5,anchor=tkinter.CENTER)

        #button back (destroy all widgets)
        but2 = customtkinter.CTkButton(
            master=frame,
            width=60,
            height=30,
            text='Back',
            fg_color=wind.button_color,
            font=(wind.button_font,wind.button_fontsize),
            border_color=wind.button_border_color,
            border_width=wind.button_bordersize,
            command=lambda: back(but,but2,frame) #input widgets to destroy, here
            )
        but2.place(rely=0.05,relx=0.09,anchor=tkinter.CENTER)


    #button encrypt
    but = customtkinter.CTkButton(
        master=frame,
        width=wind.button_X,
        height=wind.button_Y,
        text='Encrypt/Decrypt',
        fg_color=wind.button_color,
        font=(wind.button_font,wind.button_fontsize),
        border_color=wind.button_border_color,
        border_width=wind.button_bordersize,
        command=askEncrypt
        )
    but.place(rely=0.38,relx=0.5,anchor=tkinter.CENTER)


    # bottom info
    inf2 = customtkinter.CTkLabel(
        master=frame,
        text='testing edition - do not use for real purposes'
        )
    inf2.place(rely=0.98,relx=0.27,anchor=tkinter.CENTER)


    app.mainloop()


# NEW password input
def window_passwordInput(parent:customtkinter.CTk,extframe:customtkinter.CTk.frame): #TODO refactor, double password.
    #load config 
    wind = config.Password_input_window()

    #create window
    pop = customtkinter.CTkToplevel(fg_color=wind.menu_background_color)

    #title
    im0 = Image.open(files.title_image).resize(wind.titleImage_size)
    im1 = ImageTk.PhotoImage(im0)
    tit = customtkinter.CTkLabel(master=pop,image=im1,text='',width=3)
    tit.place(rely=0.1,relx=0.5,anchor=tkinter.CENTER)

    title = customtkinter.CTkLabel(master=pop,text='Enter your password',font=wind.password_title_font)
    title.place(anchor=tkinter.CENTER,rely=0.4,relx=0.5)
    
    #window settings
    pop.title('Password prompt')
    pop.iconbitmap(files.icon)
    pop.wm_attributes("-topmost", 1)

    #pop.geometry('800x500')
    pop.attributes('-fullscreen',True)

    #cancel button
    #cancel esq
    #enter button

    #password1 entry
    passinp1 = customtkinter.CTkEntry(master=pop,width=wind.password_entry_size[0],height=wind.password_entry_size[1],show='*')
    passinp1.place(anchor=tkinter.CENTER,rely=0.5,relx=0.5)
    passinp1.after(100, passinp1.focus_set)

    #password2 entry
    passinp2 = customtkinter.CTkEntry(master=pop,width=wind.password_entry_size[0],height=wind.password_entry_size[1],show='*')
    passinp2.place(anchor=tkinter.CENTER,rely=0.56,relx=0.5)

    #what happens when user press enter
    def enter(event):
        password1 = passinp1.get()
        password2 = passinp2.get()
        if not password1 or not password2:
            title.configure(text='A password field is empty')
            return
        if password1 != password2:
            title.configure(text='Passwords do not match')
            return
        funcs.keys.loadpassword(password2)
        extframe.configure(fg_color=wind.window_border_color_alert)
        funcs.wr.write('Password loaded sucessfully. You can use it multiple times in this session, remember to close the program after use. The border color is red beacuse password is loaded')
        pop.destroy()
        funcs.keys.savekeys()
        #change parent frame color
        
        

    def esq(event):
        funcs.wr.write('Operation canceled.')
        pop.destroy()


    passinp1.bind('<Return>',enter)
    passinp2.bind('<Return>',enter)
    passinp1.bind('<Escape>',esq)
    passinp2.bind('<Escape>',esq)


window_main()
