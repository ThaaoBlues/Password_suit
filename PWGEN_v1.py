import re
import string
from random import randint, choice
from tkinter import *
from tkinter import messagebox
import pyperclip
class password_generator():
    def __init__(self):
        print("""
        __________  __      __  ___________________ _______           ____ 
        \______   \/  \    /  \/  _____/\_   _____/ \      \   ___  _/_   |
         |     ___/\   \/\/   /   \  ___ |    __)_  /   |   \  \  \/ /|   |
         |    |     \        /\    \_\  \|        \/    |    \  \   / |   |
         |____|      \__/\  /  \______  /_______  /\____|__  /   \_/  |___|
                  \/          \/        \/         \/              """)
        self.all_char = string.ascii_letters + string.punctuation + string.digits
        self.password = self.generate()
        print("\n\n\n\nMOT DE PASSE :: \n{}\n".format(self.password))
        root = Tk()
        root.withdraw()
        messagebox.showinfo("MOT DE PASSE","MOT DE PASSE COPIE DANS LE PRESSE PAPIER :: \n {}".format(self.password))
        pyperclip.copy(self.password)
        
    def generate(self):
        password = ''
        for i in range(randint(8,18)):
            password = password + choice(self.all_char)
            print(password)
        return password

    
generator1 = password_generator()

