#proyect started 6/2/2023 (d m yyyy) 

#importing required modules
import tkinter
import sys
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
    funcs.writer_main_window.create(inf)
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
                funcs.keys.savekeys(True)
                pass
            else:
                funcs.keys.password = ''
                funcs.keys.writer_main_window.write('password removed.')
                extframe.configure(fg_color=wind.window_border_color)
                #ask if create new password
                res = askquestion(title='FileCrypt',message='Create another password?')
                if res=='yes': #4
                    window_passwordInput(app,extframe,savekeys=True) 
                else: #5
                    funcs.keys.savekeys(False)
                    pass
        else:
            res = askquestion(title='FileCrypt',message='Protect your private key with a password?')
            if res=='yes':# 2 generate new password
                window_passwordInput(app,extframe,savekeys=True) 
            else:# 1 without password
                funcs.keys.savekeys(False) 
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
        command=askWithPassword
        )
    but.place(rely=0.25,relx=0.5,anchor=tkinter.CENTER)


    #Clear Textbox
    cleartx = customtkinter.CTkButton(
        master=frame,
        width=wind.button_clear_X,
        height=wind.button_clear_Y,
        text='Clear',
        fg_color=wind.button_color,
        font=(wind.button_font,wind.button_fontsize),
        border_color=wind.button_border_color,
        border_width=wind.button_bordersize,
        command= funcs.writer_main_window.clear
        )
    cleartx.place(rely=0.965,relx=0.85,anchor=tkinter.CENTER)

    def askEncrypt(): # a tab that overlaps main window
        wind2 = config.Encrypt_Decrypt_Window()
        #place a new frame to overlap other widgets        
        frame = customtkinter.CTkFrame(master=app,fg_color=wind2.menu_background_color,width=wind2.menu_sizeX,height=wind2.menu_sizeY)
        frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        def back(*args):
            for widget in args:
                widget.destroy()

        #button encrypt
        but_encrypt = customtkinter.CTkButton(
            master=frame,
            width=wind2.button_X,
            height=wind2.button_Y,
            text='Encrypt',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=funcs.keys.encrypt_files
            )
        but_encrypt.place(rely=0.16,relx=0.14,anchor=tkinter.CENTER)

        #button decrypt
        but_Decrypt = customtkinter.CTkButton(
            master=frame,
            width=wind2.button_X,
            height=wind2.button_Y,
            text='Decrypt',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=lambda: funcs.keys.decrypt_files(extframe,app,wind,window_passwordInput)
            )
        but_Decrypt.place(rely=0.16,relx=0.38,anchor=tkinter.CENTER)

        #button Select files
        but_Select = customtkinter.CTkButton(
            master=frame,
            width=wind2.button_X,
            height=wind2.button_Y,
            text='Select\nfiles',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=funcs.keys.select_files
            )
        but_Select.place(rely=0.16,relx=0.66,anchor=tkinter.CENTER)

        #button select folders
        but_Select2 = customtkinter.CTkButton(
            master=frame,
            width=wind2.button_X,
            height=wind2.button_Y,
            text='Select\nfolder',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=funcs.keys.select_folders
            )
        but_Select2.place(rely=0.16,relx=0.88,anchor=tkinter.CENTER)

        #button save
        but_save = customtkinter.CTkButton(
            master=frame,
            width=wind2.button_X,
            height=wind2.button_Y,
            text='Save log',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=funcs.writer_Encrypt_Decrypt_Window.save
            )
        but_save.place(rely=0.94,relx=0.15,anchor=tkinter.CENTER)

        #button unload keys
        but_unload_keys = customtkinter.CTkButton(
            master=frame,
            width=wind2.button_X,
            height=wind2.button_Y,
            text='Unload keys',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=funcs.keys.unload_keys
            )
        but_unload_keys.place(rely=0.94,relx=0.45,anchor=tkinter.CENTER)

        #Remove selection
        but_remove_targets = customtkinter.CTkButton(
            master=frame,
            width=wind2.button_X,
            height=wind2.button_Y,
            text='Remove selection',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=funcs.keys.clearTargets
            )
        but_remove_targets.place(rely=0.94,relx=0.8,anchor=tkinter.CENTER)

        #info box
        info2 = customtkinter.CTkTextbox(
            state='disabled',
            master=frame,
            width=wind2.textbox_X,
            height=wind2.textbox_Y,
            font=(wind2.textbox_font,wind2.textbox_fontsize)
            )
        info2.place(rely=0.56,relx=0.5,anchor=tkinter.CENTER)
        funcs.writer_Encrypt_Decrypt_Window.create(info2)
        funcs.writer_Encrypt_Decrypt_Window.write('Warning: program may seem unresponsive when selecting large amounts of files.')

        #button back (destroy all widgets)
        but2 = customtkinter.CTkButton(
            master=frame,
            width=60,
            height=30,
            text='Back',
            fg_color=wind2.button_color,
            font=(wind2.button_font,wind2.button_fontsize),
            border_color=wind2.button_border_color,
            border_width=wind2.button_bordersize,
            command=lambda: back(but_Decrypt,but_encrypt,but2,info2,but_Select,but_Select2,frame,but_remove_targets) #input widgets to destroy, here
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
        text='github.com/DRVR1'
        )
    inf2.place(rely=0.98,relx=0.08,anchor=tkinter.CENTER)


    app.mainloop()


# NEW password input
def window_passwordInput(parent:customtkinter.CTk,extframe:customtkinter.CTk.frame,savekeys = False, loadingprivate = False):
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
    pop.attributes('-fullscreen',True)

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
        pop.destroy()
        funcs.keys.loadpassword(password1)
        text = 'Password loaded sucessfully.'
        try: 
            funcs.writer_main_window.write(text)
            funcs.writer_Encrypt_Decrypt_Window.write(text)
        except:
            pass
        if savekeys:
            funcs.keys.savekeys(True)
        if loadingprivate:
            funcs.keys.decryptPrivate()

    
    def esq(event):
        funcs.writer_main_window.write('Operation canceled.')
        pop.destroy()


    passinp1.bind('<Return>',enter)
    passinp2.bind('<Return>',enter)
    passinp1.bind('<Escape>',esq)
    passinp2.bind('<Escape>',esq)


window_main()
