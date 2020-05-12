import os
from functools import partial
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet

class gestionnaire():
    def __init__(self):
        self.search_var, self.site, self.username, self.password, self.fenetre_menu, self.liste, self.add_window = '', '', '', '', '', '',''
        self.init_backup()
        self.init_window()

    def init_backup(self):
        try:
            init_file = open("data/data1.BLUE")
            init_file.close()
        except:
            try:
                os.mkdir("data")
            except:
                pass
            finally:
                os.mkdir("data/websites")
                os.mkdir("data/key")
                init_file = open("data/data1.BLUE", "w")
                init_file.close()
                key_file = open("data/key/key.key","wb")
                key_file.write(Fernet.generate_key())
                key_file.close()
                
    def init_window(self):
        self.fenetre_menu = Tk()
        self.search_var = StringVar()
        self.fenetre_menu.title("GESTIONNAIRE DE MOTS DE PASSES")
        self.fenetre_menu.minsize(height=600, width=800)
        self.liste = Listbox(self.fenetre_menu)
        f = open("data/data1.BLUE", "r")
        self.liste.insert(1, "SITES :")
        i = 2
        for lines in f:
            self.liste.insert(i, lines)
            i += 1
        self.liste.pack()
        bouton_add = Button(self.fenetre_menu, text="ajouter des données d'authentification", command=self.add_credentials)
        bouton_add.pack()
        entry_search = Entry(self.fenetre_menu, textvariable=self.search_var)
        entry_search.pack(pady=40)
        self.search_var.set("nom du site")
        search_bouton = Button(self.fenetre_menu, text="afficher les infromations",
                               command=partial(self.search))
        search_bouton.pack()
        self.fenetre_menu.mainloop()

    def add_credentials(self):
        self.add_window = Toplevel(self.fenetre_menu)
        self.site = StringVar()
        self.site.set("exemple.com")
        self.username = StringVar()
        self.username.set("Nom d'utilisateur")
        self.password = StringVar()
        self.password.set("Mot de passe")
        self.add_window.title("ajouter des données d'authentification")
        self.add_window.minsize(height=300, width=400)
        entry_site = Entry(self.add_window, textvariable=self.site)
        entry_site.pack()
        entry_username = Entry(self.add_window, textvariable = self.username)
        entry_username.pack()
        entry_password = Entry(self.add_window, textvariable = self.password, show = "*")
        entry_password.pack()
        bouton_valider = Button(self.add_window, text="VALIDER",
                                command=partial(self.backupsite))
        bouton_valider.pack(pady=20)
        self.add_window.mainloop()

    def backupsite(self):
        f = open("data/data1.BLUE", "a")
        f.write(str(self.site.get() + "\n"))
        f.close()
        f = open(str("data/websites/" + self.site.get() + ".data.BLUE"), "wb")
        key_file = open("data/key/key.key")
        key = key_file.read()
        key_file.close()
        fernet = Fernet(key)
        encrypted_username = fernet.encrypt(self.username.get().encode())
        encrypted_passw = fernet.encrypt(self.password.get().encode()) 
        f.write(encrypted_username)
        f.write(b"\n")
        f.write(encrypted_passw)
        f.close()
        f = open("data/data1.BLUE", "r")
        self.liste.delete(0,END)
        self.liste.insert(1, "SITES :")
        i = 2
        for lines in f:
            self.liste.insert(i, lines)
            i += 1
        self.add_window.destroy()
        

    def search(self):
        site = self.search_var.get()
        try:
            key_file = open("data/key/key.key")
            key = key_file.read()
            key_file.close()
            fernet = Fernet(key)
            f = open(str("data/websites/" + site + ".data.BLUE"),"rb")
            encrypted_usr = f.readline()
            encrypted_passw = f.readline()
            messagebox.showinfo(str("INFORMATIONS DE : " + site), b"username :: \n" + fernet.decrypt(encrypted_usr)+ b"\npassword :: \n"+fernet.decrypt(encrypted_passw))
        except:
            messagebox.showerror(str("SITE INTROUVABLE : " + site),
                                 "Verifiez que le site que vous avez demandé est bien dans la liste.")


gestionnaire1 = gestionnaire()
