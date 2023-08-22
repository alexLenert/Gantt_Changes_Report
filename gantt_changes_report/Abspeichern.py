# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 02:30:43 2023

@author: Student
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:38:30 2023

@author: Alexander Lenert
"""

"""
Die Datei  <- Datei_Namen.txt -> darf nicht gelöscht werden!
Falls doch, bitte ein txt-File mit diesem Namen wieder erstellen und Ausgabe_1 direkt in das File schreiben.



"""

import re
from Pfade import Path
import datetime as dt
import pandas as pd
import os
import sys
from Drop_not_Relevant import Drop_not_Relevant
from Format_DF_toHtml import Format_to_html
from GUI_Check import Check
import time
import threading



class save():
    
    def __init__(self):
        self.txt_folder = os.path.join(os.path.dirname(os.path.abspath(__name__)), os.pardir,'Data')# Ordner-Ebene ist zur Laufzeit eine Ebene tiefer, daher mit os.pardir einen Ordner höher
        self.Datei_Name_r = os.path.join(self.txt_folder, 'Datei_Name.txt')# Auslesen wird in übergelagerten Ordner "Data" ausgeführt
        self.Datei_Name = ""
        self.ausgabe_ordner = os.path.join(self.txt_folder, 'ausgabe_ordner.txt')
        self.Drop = Drop_not_Relevant()
        self.df_x = self.Drop.df_actual_d_show
        self.df = Format_to_html.Format_html(self.df_x)
        self.ad = self.Drop.added
        self.dell = self.Drop.deleted
        self.zusatz = self.Drop.zusatz
        self.ausgabe = self.Drop.ausgeben
        self.email = self.Drop.email
        self.gespeichert = False
        self.gesendet = False
        self.gespeichert = self.to_html(self.df, self.ad, self.dell, self.zusatz)[1]
        self.Check = Check()
        self.meldung(Check)
        
    def to_html(self, df, ad, dell, zusatz):
        neuer_string = ""
        
        self.Datei_Name = open(self.Datei_Name_r).read() # Holt aktuellen Datei-Namen aus Datei
        
        html_list =[] 
        print("--Speichern--")
        
        #html_list.append(df.to_html(index=False))
        html_list.append(self.df)# geändert weil Farb-formatierung nur mit .render() funktioniert. Diese Methode foiert schon in html 
        html_list.append("<<< Hinzugefügte Aufträge >>>: ")
        html_list.append(self.ad.to_html(index=False))
        html_list.append("<<< Gelöschte Aufträge >>>: ")
        html_list.append(self.dell.to_html(index=False))
        html_list.append(self.zusatz)
        
        html_all = "\n".join(html_list) # 
        
        # HTML-Datei speichern
        with open(self.ausgabe + self.Datei_Name + '.html'  , 'w') as f: # speichert mit aktuellem >Datei_Namen
            f.write(html_all)
        print(f' Pfad :  {self.ausgabe}  {self.Datei_Name} .html'  )
        
        """
        Datei_Name für nächste Abfrage vorbereiten -> wird um 1 hochgezählt, damit das nächste File geschrieben werden kann 
        """
        string = self.Datei_Name # speichert verwendeten Datei-Namen
        match = re.search(r'\d+', string)  # Sucht nach einer oder mehr Ziffern im String
        if match:
            zahl = int(match.group())  # Extrahiert die Zahl als Integer
            zahl += 1  # Erhöhe die Zahl um 1
            neue_zahl = str(zahl)  # Wandelt die neue Zahl wieder in einen String um
            neuer_string = re.sub(r'\d+', neue_zahl, string)  # Ersetzt die alte Zahl im String mit der neuen Zahl
            print(neuer_string)
        
        with open(self.Datei_Name_r,mode= "w" ) as g: #speichert neuen Datei-Namen in Datei ab
            g.write(neuer_string) 
        
        self.gespeichert = True
        
        return self.Datei_Name, self.gespeichert
        
    def show_window(self):
        self.check.root.mainloop()
        
    def meldung(self, Check):
        if self.gespeichert:
            print("gespeichert")
            #self.Check = Check()
            self.Check.gespeichert()
            
            #windowThread = threading.Thread(target= show_window)
            #windowThread.start()
            
            self.Check.root.mainloop()
            time.sleep(10)
            self.Check.Frame.quit()
            self.Check.root.destroy()
            
    
Save = save()
# df_x = Save.df_x
# ad =Save.ad
# dell = Save.dell
#gespeichert = Save.to_html(Save.df, Save.ad, Save.dell, Save.zusatz)[1]

#gespeichert = Save.gespeichert
