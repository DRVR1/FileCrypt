#proyect started 6/2/2023 (d m yyyy) 

#importing required modules
import tkinter
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askquestion
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename

import random
import tkfilebrowser
import pathlib
import os
import customtkinter
import sys
from tkinter.messagebox import showinfo
import pathlib
import fast_file_encryption as ffe
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
        self.textbox.see("end")
        self.textbox.update()
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
        self.publicKey = ''
        self.privateKey = ''

        #user selected files - dir
        self.targets = []
        self.errors = []

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

    def savekeys(self,passw=False): #enter password and zip 
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
                if(passw):
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

    def encrypt_Private(self):
            #encrypt source
            if not self.private_path:
                print('private key path not set, cant encrypt private.')
                return
            if not self.password:
                print('error, not password given to decrypt private key.')
                return
            self.private_encrypted_path = pathlib.Path(os.path.join(self.folder_path,self.name_private_encrypted))
            pyAesCrypt.encryptFile(self.private_path, self.private_encrypted_path, self.password)
            self.safedelete(self.private_path,3)#safe delete source (decrypted private key)

    def printPaths(self): #prints user selected files in the textbox
        self.writer_Encrypt_Decrypt_Window.clear()
        if not self.targets:
            writer_Encrypt_Decrypt_Window.write('No files selected')
            return
        lenght = len(self.targets)
        if lenght > 3000:
            self.writer_Encrypt_Decrypt_Window.write(str(lenght) + ' files selected')
            return
        for path in self.targets:
            self.writer_Encrypt_Decrypt_Window.write('Selected: ' + path)
        pass

    def select_folders(self):
        #dirs = tkfilebrowser.askopendirnames(None,title='Select folder/s')
        dir = askdirectory(title='Select folder')
        #for folder in dirs:
        for path, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith('.lnk'):
                    continue
                fullpath = os.path.join(path,file)
                if fullpath not in self.targets:
                    self.targets.append(fullpath)
        self.printPaths()            
        pass 

    def select_files(self):
        files = askopenfilenames(title='Add files (you can select multiple files at once)')
        for file in files: 
            if file in self.targets: #if file already was selected, continue
                continue
            self.targets.append(file) 
        self.printPaths()
        pass

    def clearTargets(self):
        self.targets = []
        self.writer_Encrypt_Decrypt_Window.clear()
        self.writer_Encrypt_Decrypt_Window.write('No files selected')
    def encrypt_files(self):
        self.errors = []
        excluded = False
        errordeleting = False
        errorEncrypting = False
        if not self.publicKey:
            writer_Encrypt_Decrypt_Window.write('No public key loaded. Please select your public key.')
            self.loadpublic()
            return
        if not self.targets:
            self.writer_Encrypt_Decrypt_Window.write('No files/folder selected')
            return
        self.writer_Encrypt_Decrypt_Window.clear()
        for target in self.targets:
            if target.endswith('.ffe'):
                writer_Encrypt_Decrypt_Window.write('excluding ' + target + ' was already encrypted.')
                excluded = True
                continue
            encryptor = ffe.Encryptor(self.publicKey)
            try:
                destiny = target + '.ffe'
                target = pathlib.Path(target)
                destiny = pathlib.Path(destiny)
                self.writer_Encrypt_Decrypt_Window.write('Encrypting ' + str(target))
                encryptor.copy_encrypted(target,destiny)
                self.writer_Encrypt_Decrypt_Window.write('Encrypted ' + str(target))
            except:
                errorEncrypting = True
                errormsj = 'Error encrypting ' + str(target)
                writer_Encrypt_Decrypt_Window.write(errormsj)
                self.errors.append(errormsj)
                continue
            try:
                self.safedelete(target)
            except:
                errordeleting = True
                errormsj = 'Error deleting unencrypted ' + str(target)
                writer_Encrypt_Decrypt_Window.write(errormsj)
                self.errors.append(errormsj)
                os.remove(destiny)
            pass
        if excluded:
            showinfo('File/s were excluded','Looks like some files were already encrypted and have been exluded from the encryption.')
        if errordeleting:
            showinfo('Error deleting unencrypted file/s','An error ocurred while trying to delete an unencrypted file/s, please look at the log and delete those files, for safety. ')
        if errorEncrypting:
            showinfo('Error encrypting file/s','An error ocurred while trying to encrypt a file. Maybe permisions are needed, or the file was already encrypted. Please check the log ')
        if excluded or errordeleting or errorEncrypting:
            self.writer_Encrypt_Decrypt_Window.clear()
            for error in self.errors:
                self.writer_Encrypt_Decrypt_Window.write(error)

    def decrypt_files(self,extframe,app,wind,window_passwordInput):

        if not self.privateKey:
            self.writer_Encrypt_Decrypt_Window.write('No private key loaded, please select your private key.')
            self.loadprivate(extframe,app,wind,window_passwordInput)
            return

        if not self.targets:
            self.writer_Encrypt_Decrypt_Window.write('No files/folder selected')
            return
        decryptor = ffe.Decryptor(self.privateKey)

        self.decrypt_errors = []

        for file in self.targets:
            if not file.endswith('.ffe'):
                writer_Encrypt_Decrypt_Window.write('excluding ' + file + ' was not encrypted or does not exist.')
                continue

            destiny = file[:-4] #removes .ffe extension
            try:
                writer_Encrypt_Decrypt_Window.write('Decrypting ' + file + '.')
                decryptor.copy_decrypted(pathlib.Path(file),pathlib.Path(destiny))
                writer_Encrypt_Decrypt_Window.write('Decrypted ' + file + '.')
            except:
                error = 'Error decrypting file ' + str(file) + ' check if other program opened the file.'
                writer_Encrypt_Decrypt_Window.write(error)
                self.decrypt_errors.append(error)
                continue
            try:
                os.remove(file)
            except:
                error = 'Error deleting encrypted file ' + file + ' But was decrypted sucessfully.'
                writer_Encrypt_Decrypt_Window.write(error)
                self.decrypt_errors.append(error)
        
        if self.decrypt_errors:
            self.writer_Encrypt_Decrypt_Window.clear()
            showinfo('Errors, check the log','There were errors when decrypting file/s. Please check the log.')
            for error in self.decrypt_errors:
                self.writer_Encrypt_Decrypt_Window.write(error)

    def loadpublic(self): #enter password and unzip
        showinfo('Information','An explorer window will popup, please select your public key')
        self.public_path = askopenfilename(title='Select your public key') # show an "Open" dialog box and return the path to the selected file
        self.publicKey=ffe.read_public_key(pathlib.Path(self.public_path))
        self.writer_Encrypt_Decrypt_Window.write('Public key loaded from ' + self.public_path)

    def decryptPrivate(self): #after getting the password, decrypt private key
        try:   
            home = os.path.expanduser('~')
            tempf = os.path.join(home,str(random.randint(99,999999999)))
            pyAesCrypt.decryptFile(self.private_encrypted_path,tempf,self.password) #writes decrypted private key to RAM
            self.privateKey = ffe.read_private_key(pathlib.Path(tempf))
            self.safedelete(tempf)
            self.writer_Encrypt_Decrypt_Window.write('Private key loaded from ' + self.private_encrypted_path)   
        except:
            self.writer_Encrypt_Decrypt_Window.write('Error decrypting private key, check your password!')


    def loadprivate(self,extframe,app,wind,window_passwordInput): 
        showinfo('Information','An explorer window will popup, please select your private key')
        self.private_path = askopenfilename(title='Select your private key') # show an "Open" dialog box and return the path to the selected file
        try:
            self.privateKey=ffe.read_private_key(pathlib.Path(self.private_path))
            self.writer_Encrypt_Decrypt_Window.write('Private key loaded from ' + self.private_path)   
        except:
            writer_Encrypt_Decrypt_Window.write('Error loading private key. It may be encrypted, or wrong path.')
            self.private_encrypted_path = self.private_path
            self.private_path = ''
            res = askquestion('Password','Are you trying to open an encrypted private key?')
            if res=='yes':
                window_passwordInput(app,extframe,loadingprivate=True) #decrypt after password input
                return
            else:
                return
    
    def unload_keys(self):
        self.publicKey = ''
        self.privateKey = ''
        self.public_path = ''
        self.private_path = ''
        self.writer_Encrypt_Decrypt_Window.write('Keys were unloaded.')
#objects
writer_main_window = Writer() # a writer for the main window
writer_Encrypt_Decrypt_Window = Writer() # a writer for the encrypt_decrypt window
keys = Keys(writer_main_window,writer_Encrypt_Decrypt_Window)