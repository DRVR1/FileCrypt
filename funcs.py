#proyect started 6/2/2023 (d m yyyy) 

#importing required modules
import tkinter
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askquestion
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
import wx.lib.agw.multidirdialog as MDD
import wx
import os
import customtkinter
import sys
from tkinter.messagebox import showinfo
import pathlib
import fast_file_encryption as ffe
from res import config
import pyAesCrypt

#check if the program was frozen with pyinstaller/nuitka
def isFrozen():
    try:
        sys._MEIPASS
        return True
    except:
        return False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#this writes in the main window textbox, we call the write() method from the main class giving the created textbox as parameter, so we can print from this module
class Writer():
    def __init__(self) -> None:
        self.lineNumber = -1
    def create(self,textbox:customtkinter.CTkTextbox):
        self.textbox = textbox
    def write(self,input):
        self.textbox.configure(state='normal')
        self.lineNumber += 1
        self.textbox.insert(tkinter.INSERT,str(self.lineNumber)+'. ' + input + '\n')
        self.textbox.configure(state='disabled')
    def save(self):
        file = asksaveasfilename(title='Select where to save your file',defaultextension='.txt',initialfile='FileCrypt-log')
        if file:
            f = open(file,'w')
            f.write(self.textbox.get(1.0,'end'))
            f.close()
        pass
    def clear(self):
        self.lineNumber = -1
        self.textbox.configure(state='normal')
        self.textbox.delete(1.0,'end')
        self.textbox.configure(state='disabled')
        pass


class Keys():
    def __init__(self, writer_main_window:Writer,writer_Encrypt_Decrypt_Window:Writer) -> None:
        #key names
        self.name_public = 'publicKey.txt'
        self.name_private = 'privateKey.txt'
        self.name_private_encrypted= 'privateKey.enc.txt'
        self.name_folder = 'keys'

        #user
        self.password = ''
        self.folder_path = ''
        self.public_path = ''
        self.private_path = ''
        self.private_encrypted_path = ''

        #user selected files - dir
        self.targets = []

        #objects
        self.writer_main_window = writer_main_window
        self.writer_Encrypt_Decrypt_Window = writer_Encrypt_Decrypt_Window

    def loadpassword(self,password):
        self.password = password
        pass

    def safedelete(self,path, passes=1): #secure delete feature, credits to kindall https://stackoverflow.com/a/17455478
        with open(path, "ba+") as delfile:
            length = delfile.tell()
        with open(path, "br+") as delfile:
            for i in range(passes):
                delfile.seek(0)
                delfile.write(os.urandom(length))
        os.remove(path)

    def savekeys(self): #enter password and zip 
        showinfo('Information','An explorer window will popup, please select the directory where the keys folder will be created.') 
        path = askdirectory(title='Select the folder where the keys folder will be saved',mustexist=True) 

        if path:
            self.folder_path = path + '/' + self.name_folder
            try:
                self.writer_main_window.write('Trying to create dir in: ' + self.folder_path)
                os.mkdir(self.folder_path)
                self.writer_main_window.write('Dir created')
            except:
                error_string = 'The folder "' + self.name_folder + '" already exists in "' + self.folder_path +'". Cannot create new keys.'
                self.writer_main_window.write(error_string)
                showinfo('Error',error_string) 
                return
                pass
            self.writer_main_window.write('Folder path is: ' + self.folder_path)
            self.writer_main_window.write('Generating keys')
            try:
                self.public_path = pathlib.Path(os.path.join(self.folder_path,self.name_public))
                self.private_path = pathlib.Path(os.path.join(self.folder_path,self.name_private))

                ffe.save_key_pair(public_key=self.public_path,private_key=self.private_path)
                self.writer_main_window.write('Keys generated')
                if(self.password):
                    self.writer_main_window.write('Encrypting private key with loaded password')
                    try:
                        self.encrypt_Private()
                        self.writer_main_window.write('Private key encrypted')
                    except:
                        self.writer_main_window.write('ERROR ENCRYPTING PRIVATE KEY')
                else:
                    self.writer_main_window.write('Warning! private key was not encrypted, please save it in a safe place!')
            except:
                self.writer_main_window.write('Error generating keys')
        else:
            self.writer_main_window.write('Operation canceled.')

    def printPaths(self): #prints selected files and dirs in the selected textbox
        self.writer_Encrypt_Decrypt_Window.clear()
        for path in self.targets:
            self.writer_Encrypt_Decrypt_Window.write(path)
        pass

    def select_folders(self):
        a = wx.App(0)
        dialog = MDD.MultiDirDialog(None, title="Press (ctrl + click) to select multiple folders", defaultPath=os.getcwd(),agwStyle=MDD.DD_MULTIPLE|MDD.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() != wx.ID_OK: #if close
            dialog.Destroy()
        folders = dialog.GetPaths()
        for folder in folders:
            print(folder)
        pass #TODO continue

    def select_files(self):
        files = askopenfilenames(title='Add files (you can select multiple files at once)')
        for file in files: 
            if file in self.targets: #if file already was selected, continue
                continue
            self.targets.append(file) 
        self.printPaths()
        pass

    def encrypt_Private(self):
        if self.public_path:
            res = askquestion
            pass
        #encrypt source
        if not self.private_path:
            print('private key path not set, cant encrypt private.')
            return
        self.private_encrypted_path = pathlib.Path(os.path.join(self.folder_path,self.name_private_encrypted))
        pyAesCrypt.encryptFile(self.private_path, self.private_encrypted_path, self.password)
        #safe delete source (decrypted private key)
        self.safedelete(self.private_path,3)

    def loadpublic(self): #enter password and unzip
        showinfo('Information','An explorer window will popup, please select your public key')
        filename = askopenfilename(title='Open keys file') # show an "Open" dialog box and return the path to the selected file
        self.publicKey=ffe.read_public_key(ffe)
        print('filename is: ' + filename)

#objects
writer_main_window = Writer() # a writer for the main window
writer_Encrypt_Decrypt_Window = Writer() # a writer for the encrypt_decrypt window
keys = Keys(writer_main_window,writer_Encrypt_Decrypt_Window)