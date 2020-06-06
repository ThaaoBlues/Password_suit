import os
from functools import partial
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
import pyperclip
from flask import Flask, render_template, request
from flaskwebgui import FlaskUI #get the FlaskUI class
import os
import time
from random import randint, choice
import string



app = Flask(__name__)

# Feed it the flask app instance 
ui = FlaskUI(app)



# main page
@app.route("/", methods = ['POST','GET'])
def index():
    if request.method == "POST":
        text = request.form['text']
        print(text)
        search(text)
    else:
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

        f = open("data/data1.BLUE", "r")
        i = 2
        liste = []
        for lines in f:
            liste.insert(i, lines)
            i += 1
        return render_template("index.html",liste = liste)




#trigered when add auth data button pressed
@app.route("/add_data/", methods = ['POST','GET'])

def add_data():
    if request.method == "POST":
        #backup et retour a l'acceuil
        backupsite(request.form['site'],request.form['id'],request.form['pass'])

        #update the websites list and pass it to the html
        return render_template("index.html",liste = website_list())
    else:
        return render_template("add_data.html")





#trigered when button generate password pressed
@app.route("/mdp_generator/", methods = ['POST','GET'])

def mdp_generator():
    #create the root tk to show message box
    root = Tk()
    #Tk().withdraw()
    root.lift()

    #generate password
    all_char = string.ascii_letters + string.punctuation + string.digits
    password = ''
    for i in range(randint(8,18)):
        password = password + choice(all_char)

    messagebox.showinfo("MOT DE PASSE",
    "MOT DE PASSE COPIE DANS LE PRESSE PAPIER :: \n {}".format(password))
    #copy in clipboard
    pyperclip.copy(password)

    root.destroy()
    #redirect
    return render_template("index.html",liste = website_list())




#triggered when click on the seaarch button
@app.route("/search/", methods = ['POST','GET'])

def show_search_results():
    print("search")
    if request.method == "POST":
        site = request.form['website_name']
        
        print(site)
        search(site)
        return render_template("index.html",liste = website_list())

    else:
        return render_template("index2.html",liste = website_list())






#functions not triggered by GUI



#refresh website list
def website_list():
    f = open("data/data1.BLUE", "r")
    i = 2
    liste = []
    for lines in f:
        liste.insert(i, lines)
        i += 1

    return liste


#backup function used to add a website
def backupsite(site,username,password):
    f = open("data/data1.BLUE", "a")
    f.write(str(site + "\n"))
    f.close()
    f = open(str("data/websites/" + site + ".data.BLUE"), "wb")
    key_file = open("data/key/key.key")
    key = key_file.read()
    key_file.close()
    fernet = Fernet(key)
    encrypted_username = fernet.encrypt(username.encode())
    encrypted_passw = fernet.encrypt(password.encode()) 
    f.write(encrypted_username)
    f.write(b"\n")
    f.write(encrypted_passw)
    f.close()



#function to search and display creds of a website
def search(site):
    #create the root tk to show message box
    root = Tk()
    #root.withdraw()
    root.lift()
    try:
        #get decrypt key
        key_file = open("data/key/key.key")
        key = key_file.read()
        key_file.close()
        fernet = Fernet(key)
        f = open(str("data/websites/" + site + ".data.BLUE"),"rb")
        encrypted_usr = f.readline()
        encrypted_passw = f.readline()
        
        #show creds
        messagebox.showinfo(str("INFORMATIONS DE : " + site), b"username :: \n" + fernet.decrypt(encrypted_usr)+ b"\npassword :: \n"+fernet.decrypt(encrypted_passw))
        pyperclip.copy(str(fernet.decrypt(encrypted_passw)).strip('b').strip("'"))
        messagebox.showinfo("MOT DE PASSE COPIE", "Mot de passe copié dans le press-papier, \nvous n'avez plus qu'à le coller dans le formulaire du site")
    except:
        messagebox.showerror(str("SITE INTROUVABLE : " + site),
                             "Verifiez que le site que vous avez demandé est bien dans la liste.")

    root.destroy()
#run app
ui.run()
