# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:45:15 2023

@author: eh
"""
from tkinter import Tk
from tkinter import Frame
from tkinter import Label




class Check:

    def __init__(self):
        self.root = Tk()
        self.Frame= Frame(self.root)
        self.Frame.place(x=0,y=0, width = 350, height= 100)
        
        
        #self.root.mainloop()
        
    def gespeichert(self):
        self.Label_1 = Label(self.Frame, text= "Ihr Dokument wurde erstellt. ")
        self.Label_1.place(x=20, y= 10, width= 200, height= 30)
        
        
    def gesendet(self):
        self.Label_2 = Label(self.Frame, text= "Ihr Dokument wurde versendet. ")
        self.Label_2.place(x=20, y= 50, width= 200, height= 30)
        
        


#test = check()

#test.gespeichert()
#test.gesendet()
#test.root.mainloop()