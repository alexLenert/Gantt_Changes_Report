# -*- coding: utf-8 -*-
"""
Created on Fri May 19 01:42:46 2023

@author: Student
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 14:18:10 2023
"""

from abc import ABC, abstractmethod
import threading
import time
from Pfade import Path
from tkinter import Tk, Button, Label, Listbox, ANCHOR, Frame, ttk
from tkinter import Scrollbar
import os

txt_folder = os.path.join(os.path.dirname(os.path.abspath(__name__)), os.pardir,'Data')
email_adressen = os.path.join(txt_folder, 'email_adressen.txt')

class App_abstrakt(ABC):

    @abstractmethod
    def dateien_to_listbox(self):
        pass

    @abstractmethod
    def email_to_listbox(self):
        pass

    @abstractmethod
    def select1(self):
        pass

    @abstractmethod
    def select2(self):
        pass

    @abstractmethod
    def select3(self):
        pass

    @abstractmethod
    def insert_email(self):
        pass

    @abstractmethod
    def setAuswahl_XML(self):
        pass

    @abstractmethod
    def setAuswahl_E_Mail(self):
        pass


pfad = Path()


class App(App_abstrakt):
    def __init__(self):
        super().__init__()
        self.selected_elements = []
        self.auswahl_1 = ""
        self.auswahl_2 = ""
        self.auswahl_3 = ""
        self.path = pfad.einlesen  # Pfad aus dem Ur-Modul
        self.dateien = self.verzeichnis()
        self.datei_email_adressen = "email_adressen.txt"
        self.master = Tk(className=" Projekt XML-Gantt-Vergleich")
        self.frame = Frame(self.master, bg="lightblue")
        self.master.geometry("800x500")
        self.frame.place(x=0, y=0, width=800, height=500)

        self.choosed_1 = ttk.Label(self.master, text="______Auswahl:_____")
        self.choosed_2 = ttk.Label(self.master, text="______Auswahl:_____")
        self.e_mail_choosed = ttk.Label(self.master, text="____Email_____")
        self.email_eingabe = ttk.Entry(self.master)

        self.choosed_1.place(x=235, y=130, width=120, height=40)
        self.choosed_2.place(x=440, y=130, width=120, height=40)
        self.e_mail_choosed.place(x=440, y=250, width=120, height=20)
        self.email_eingabe.place(x=235, y=360, width=150, height=25)

        self.ueberschrift = Label(self.frame, text="Projekt XML-Gantt-Vergleich : ", border=3, borderwidth=3,
                                  bg="#0F11F1", justify="center")
        self.ueberschrift.place(x=195, y=20, width=400, height=25)

        listbox1 = self.dateien_to_listbox()
        listbox1.place(x=30, y=60, width=180, height=250, border="inside")

        chose_1_button = Button(self.master, text="xml_1 auswaehlen", border="3", bg="lightgreen",
                                command=lambda: self.select1(listbox1))
        chose_1_button.place(x=235, y=60, width=120, height=50)

        auforderung = Label(self.frame, text="Email der Liste hizufügen")
        auforderung.place(x=235, y=330, width=260, height=25)

        listbox2 = self.dateien_to_listbox()
        listbox2.place(x=580, y=60, width=180, height=250, border="inside")

        chose_2_button = Button(self.master, text="xml_2 auswaehlen", border="3", bg="lightgreen",
                                command=lambda: self.select2(listbox2))
        chose_2_button.place(x=440, y=60, width=120, height=50)

        listbox_email = self.email_to_listbox()
        listbox_email.place(x=235, y=210, width=180, height=100)

        chose_Email_button = Button(self.master, text="E-Mail auswaehlen", border="3", bg="lightgreen",
                                    command=lambda: self.select3(listbox_email))
        chose_Email_button.place(x=440, y=210, width=120, height=20)

        add_Email_button = Button(self.master, text="Add E-Mail", border="3", bg="lightgreen",
                                  command=lambda: self.insert_email(self.email_eingabe, listbox_email))
        add_Email_button.place(x=395, y=360, width=100, height=25)

        vergleich_button = Button(self.master, text="vergleichen", border="3", bg="blue", fg="yellow",
                                  command=lambda: self.setAuswahl_XML())
        vergleich_button.place(x=310, y=430, width=180, height=50)

        self.master.mainloop()

    def verzeichnis(self):
        dateien = os.listdir(self.path)
        return dateien

    def dateien_to_listbox(self):
        listbox = Listbox(self.master, bg="lightgrey")

        for i in self.dateien:
            listbox.insert("end", i)

        return listbox

    def email_to_listbox(self):
        listbox = Listbox(self.master, bg="lightgrey")

        with open(self.datei_email_adressen, "r") as f:
            liste_email = f.read()
            liste_email = liste_email.split(", ")
        for i in liste_email:
            listbox.insert("end", i)

        return listbox

    def select1(self, listbox1):
        self.auswahl_1 = listbox1.get(ANCHOR)
        self.choosed_1.configure(text=self.auswahl_1)
        self.choosed_1.place(x=235, y=130, width=120, height=40)
        #print(self.choosed_1.cget("text"))

    def select2(self, listbox2):
        self.auswahl_2 = listbox2.get(ANCHOR)
        self.choosed_2.configure(text=self.auswahl_2)
        self.choosed_2.place(x=440, y=130, width=120, height=40)
        #print(self.choosed_2.cget("text"))

    def select3(self, listbox_email):
        self.auswahl_3 = listbox_email.get(ANCHOR)
        self.e_mail_choosed.configure(text=self.auswahl_3)
        self.e_mail_choosed.place(x=440, y=250, width=120, height=20)
        print(self.e_mail_choosed.cget("text"))

    def insert_email(self, email_eingabe, listbox_email):
        eingabe = email_eingabe.get()
        listbox_email.insert("end", eingabe)


    def setAuswahl_XML(self):
        if self.auswahl_1 and self.auswahl_2:
            self.beenden()
        return [self.auswahl_1, self.auswahl_2]

    def setAuswahl_E_Mail(self):
        #print(self.auswahl_3)
        self.beenden()
        return self.auswahl_3
    

    def beenden(self):
        time.sleep(1)
        self.master.quit()


class App_1(App_abstrakt):
    def __init__(self):
        super().__init__()
        self.selected_elements = []
        self.auswahl_1 = ""
        self.auswahl_2 = ""
        self.auswahl_3 = []
        self.auswahl_4 = ""
        self.path = pfad.einlesen # Pfad aus dem Ur-Modul
        self.dateien = self.verzeichnis()
        self.datei_email_adressen = email_adressen
        self.master = Tk(className=" Projekt XML-Gantt-Vergleich")
        self.frame = Frame(self.master,bg= "lightblue")
        self.master.geometry("800x600")
        self.frame.place(x= 0, y= 0, width=800, height=600 )

        self.choosed_1 = ttk.Label(self.master, text="______Auswahl:_____")
        self.choosed_2 = ttk.Label(self.master, text="______Auswahl:_____")
        self.e_mail_choosed = ttk.Label(self.master, text="____Email_____")
        self.email_eingabe = ttk.Entry(self.master)
        #self.choosed_1.pack(pady=10)
        #self.choosed_2.pack(pady=10)
        
        self.choosed_1.place(x= 420,y=60)
        self.choosed_2.place(x= 420,y=85)
        self.e_mail_choosed.place(x=410, y=330, height=25)
        self.email_eingabe.place(x= 410, y= 360, width= 150,height=25)
        
        
        
        self.ueberschrift = Label(self.frame, text="Projekt XML-Gantt-Vergleich : ", border=3, borderwidth=3, bg="#0F11F1",justify="center") 
        self.ueberschrift.place(x=195,y=20,width=400,height=25)
        
        
        
        listbox1 = self.dateien_to_listbox(self.dateien)
        listbox1.place(x= 30, y= 60, width=240,height=250, border="inside")
        
        scrollbar = Scrollbar(listbox1, orient="vertical") # Zuordnung
        scrollbar.config(command=listbox1.yview) # Ausführung
        scrollbar.pack(side="right", fill="y") # Position
        
        
        chose_1_button = Button(self.master, text="Alte XML auswaehlen",border= "3", bg= "lightgreen", command=lambda: self.select1(listbox1, chose_1_button))
        chose_1_button.place(x=290,y=60, width=120,height=50)
        
        # auforderung = Label(self.frame, text="Email der Liste hizufügen")      
        # auforderung.place(x= 290, y= 330, width= 260,height=25)

        
        
        chose_Email_button = Button(self.master, text="E-Mail auswaehlen",border= "3", bg= "lightgreen" , command=lambda: self.select3(listbox_email))
        chose_Email_button.place(x=290, y=330, width=110,height=25)
        
        add_Email_button = Button(self.master, text="Add E-Mail",border= "3", bg= "lightgreen" , command=lambda: self.insert_email(self.email_eingabe, listbox_email))
        add_Email_button.place(x= 290, y= 360, width= 110,height=25)
        
        delete_email_button = Button(self.master, text= "Remove E-Mail", bg= "lightgreen" , command= lambda: self.clear_email(listbox_email))
        delete_email_button.place(x= 290, y = 385, width=110, height=25)
        
        clear_email_liste_button = Button(self.master, text="Clear List",bg= "lightgreen", command= lambda: self.clear_all_emails(listbox_email))
        clear_email_liste_button.place(x= 290, y = 410, width=110, height= 25)
        
        select_all_email_button = Button(self.master, text= "Select all", bg= "lightgreen", command= lambda : self.select_all_email(listbox_email))
        select_all_email_button.place(x= 290, y= 435, width=110, height= 25)
        
        liste_speichern = Button(self.master, text= "Save List", bg= "lightgreen",command= lambda: self.save_changed(listbox_email))
        liste_speichern.place(x= 290, y= 460, width=110, height=25)
        
        vergleich_button = Button(self.master, text="vergleichen",border= "3" , bg = "blue", fg = "yellow", command=lambda: self.setAuswahl_XML())
        vergleich_button.place(x= 290,y=530,width=180,height=50)
        
        listbox_email = self.email_to_listbox(self.datei_email_adressen)
        listbox_email.place(x=30,y=330,width=240,height=100)
        
        scrollbar = Scrollbar(listbox_email, orient="vertical") # Zuordnung
        scrollbar.config(command=listbox_email.yview) # Ausführung
        scrollbar.pack(side="right", fill="y") # Position
        
        
        self.master.mainloop()

    def verzeichnis(self):
        dateien = os.listdir(self.path)
        return dateien
  

    def dateien_to_listbox(self, dateien):
        listbox = Listbox(self.master, bg="lightgrey")

        for i in dateien:
            listbox.insert("end", i)

        #listbox.bind('<<ListboxSelect>>', self.onSelect)
        return listbox

    def email_to_listbox(self, datei_email_adressen):
        listbox = Listbox(self.master, selectmode= "extended", bg="lightgrey")
        
        with open(self.datei_email_adressen, "r") as f:
            liste_email = f.read()
            liste_email = liste_email.split(", ")
        for i in liste_email:
            listbox.insert("end", i)
        
        return listbox
    
   

    def select1(self, listbox1, button):
        if button.cget("text") == "Alte XML auswaehlen":
            self.auswahl_1 = listbox1.get(ANCHOR)
            self.choosed_1.configure(text=self.auswahl_1)
            self.choosed_1.place(x= 420,y=60)
            button.configure(text= "Neue XML auswaehlen")
            print(self.choosed_1.cget("text"))
        elif button.cget("text")== "Neue XML auswaehlen":
            self.auswahl_2 = listbox1.get(ANCHOR)
            self.choosed_2.configure(text=self.auswahl_2)
            self.choosed_2.place(x= 420,y=85) 
            print(self.choosed_2.cget("text"))
    def select2():
        pass
        
    def select3(self, listbox_email):
        #self.auswahl_3 = listbox_email.get(ANCHOR)
        self.auswahl_3 = []
        self.auswahl_4 = listbox_email.curselection()
        for index in self.auswahl_4:
            self.auswahl_3.append(listbox_email.get(index))
        #print("Ausgewählter Eintrag:", self.auswahl_3)
        
        self.e_mail_choosed.configure(text=self.auswahl_3)
        self.e_mail_choosed.place(x=410, y=330,  height=25) 
        print(self.e_mail_choosed.cget("text"))
    
    def select_all_email(self, listbox_email):
        self.auswahl_3 = ""
        self.auswahl_3 = (listbox_email.get(0, "end"))
        self.e_mail_choosed.configure(text=self.auswahl_3)
        ausgewaehlt = Label(self.master, text= "All selected")
        ausgewaehlt.place(x= 410, y= 435, width=110, height= 25)
        print(type(self.auswahl_3))
        
    def clear_all_emails(self, listbox_email):
        listbox_email.delete(0,"end")
        
    def clear_email(self, listbox_email):
        listbox_email.delete(ANCHOR)
        
        
    def insert_email(self, email_eingabe, listbox_email):
        eingabe = email_eingabe.get()
        listbox_email.insert("end",eingabe)
        email_eingabe.delete(0, "end")
    
    
    def save_changed (self, listbox_email):
        inhalt = listbox_email.get(0,"end")
        print("Inhalt:  " + str(inhalt))
        with open(self.datei_email_adressen, "w") as f:
            for i in inhalt:
                f.write(str(i)+ ", ")
        
    def getAuswahl_1(self):
        return self.choosed_1
    
    def getAuswahl_2 (self):
        return self.choosed_2
    
    def setAuswahl_XML (self):
        t = threading.Thread(target=self.setAuswahl_XML, daemon=True)
        t.start() # setzt eine Flagge für den Thread
        
        
        if self.auswahl_1 and self.auswahl_2:
            self.beenden()
        
        
        return [self.auswahl_1, self.auswahl_2]
    
    
    def setAuswahl_E_Mail (self): # Übergabe der email-Liste
        # t = threading.Thread(target=self.setAuswahl_E_Mail, daemon=True)
        # t.start() # setzt eine Flagge für den Thread
        
        return self.auswahl_3 
    
    
    def beenden(self):
        time.sleep(1)
        self.master.quit()


