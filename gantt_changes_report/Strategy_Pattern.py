# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 14:12:32 2023

@author: Student
"""

import pandas as pd

from Fall_entscheidung import Entscheiden

from zeiten_aufrechnen import zeiten
from LT_anpassen import SetLT


class Comparsion():
    zeiten = zeiten()
    
    """
    die die Methode fall_if der Klasse Entscheiden liefert eine Liste aus folgenden Elementen:

        0: df_actual_d, 1: df_actual_d_show, 2: verschieben, 3: verlaengern, 4: df_start_self, 5: df_start_other, 6: df_duration_self, 7: df_duration_other , 8: zusatz, 9: added, 10: deleted 


    """
    
    def __init__(self):
        Entscheidung = Entscheiden()
        self.Ausgabe = Entscheidung.fall_if(Entscheidung.ergebnis, Entscheidung.datei_1, Entscheidung.datei_2)
        self.ergebnis = Entscheiden.getErgebnis(Entscheidung)
        self.df_actual_d_show = pd.DataFrame()# Leere Ausgaben werden initialisiert, und können -im Fall der Existens- überschrieben werden
        self.df_actual_d = pd.DataFrame()     # So wird ein Ausnahme-Fehler abgefangen
        self.verschieben = pd.Series(dtype = object)
        self.verlaengern = pd.Series(dtype = object)
        self.df_start_self = pd.Series(dtype = object)
        self.df_start_other = pd.Series(dtype = object)
        self.df_duration_self = pd.Series(dtype = object)
        self.df_duration_other = pd.Series(dtype = object)
        self.zusatz = Entscheidung.zusatz
        self.list_resources = Entscheidung.list_resources
        self.ausgeben = Entscheidung.ausgeben
        self.email = Entscheidung.email
    
    def switch(self,liste):
        if liste[0].empty and not liste[1].empty: # not
            print("show")
            self.df_actual_d_show = liste[1]
            self.added = liste[9]
            self.deleted = liste[10]
             
            #Datei_Name = save.to_html(df_actual_d_show, added, deleted, liste[8])
            print("ohne Added und Deleted") 
            
            # datum_w = zeiten.zeitenBerechnen(comp, liste[4], liste[0], liste[2], liste[3])
            # parent_datum = zeiten.datumParent(liste[0], comp)
            
            
        elif liste[0].empty and liste[1].empty:
            print("nichts drin")
            self.df_actual_d_show = liste[1]
            self.added = liste[9]
            self.deleted = liste[10]
              
            #Datei_Name = save.to_html(df_actual_d_show, added, deleted, liste[8])
            print("Keine Veränderung") 
            
        elif not liste[0].empty and liste[1].empty:
            print("Full")
            datum_w_liste = zeiten.zeitenBerechnen(self.ergebnis, liste[5], liste[7], liste[0], liste[2], liste[3]) # Aggregation!!
            datum_w = datum_w_liste[0]
            datum_s = datum_w_liste[1]
           # parent_datum = zeiten.datumParent(liste[0], comp, liste[2],liste[3])
            self.df_actual_d = zeiten.datumVergleichen(liste[0], datum_w, datum_s)
            self.df_actual_d = self.df_actual_d.rename(columns = {"name":"Vorgang" }) # ändert Spalten-Name von "name auf "Vorgang" - Gleiche Bezeichnung wie in GanttProjekt
            self.added = liste[9]
            self.deleted = liste[10]
            self.df_actual_d_LT = SetLT.getAll_LT(self.df_actual_d, self.ergebnis)
            self.df_actual_d_True = zeiten.LT_Vergleichen(self.df_actual_d_LT, datum_w, self.df_actual_d["LT"])# Vergleicht LT mit datum_w -> True 
            self.df_actual_d = zeiten.LT_one(self.df_actual_d_True) # Überdeckt alle early / late wo True existiert
#comp = Comparsion()
#comp.switch(comp.Ausgabe)
#ausgeben = comp.ausgeben
#zusatz = comp.zusatz
#df = comp.df_actual_d
#df_actual_d_show = comp.df_actual_d_show

#df_LT = comp.df_actual_d_LT

#df_True = comp.df_actual_d_True


