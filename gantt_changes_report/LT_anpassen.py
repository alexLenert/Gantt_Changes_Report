# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 08:23:14 2023

@author: Student
"""
import pandas as pd


class SetLT():


    """
    Dieser Abschnitt setzt in die Spalte LT für jede Row den Liefertermin ein, 
    wenn er in der Row des DataFrames nicht verfügbar ist, werden übergeordnete
    Rows außerhalb der dedizierten Daten nach dem Liefertemin durchsucht und eingesetzt 
    """
    def getAll_LT(df_actual_d,comp):
    
        df_actuald_d_2dn = df_actual_d
        
        index_parent = df_actuald_d_2dn["parent"] # Series parent aus df 
        index_parent = index_parent.dropna() # alle tasks die tatsächlichen parents haben
        
        datenPool = pd.concat([comp["old"],comp["new"]])# Gesamte Ursprungsdaten 
        
        datenPool_aufgeräumt = datenPool[~datenPool.index.duplicated(keep='first')] # doppelte Einträge aus ursprungdaten löschen
        datenPool_LT_parent = datenPool_aufgeräumt[["LT", "parent"]]# DataFrame mit Series LT und parent aus Ursprungsdaten -> alle Liefertermine die existiere
        
        datenPool_LT_parent_intern = datenPool_LT_parent.fillna("Intern") # alle nans haben keinen Liefertermin
        
        liefertermin =  datenPool_LT_parent_intern.loc[index_parent] # alle Liefertermine der parents begrenzt auf die IDs der Series parent von df_actual_d 
        #liefertermin = liefertermin[~liefertermin.index.duplicated(keep='first')] # Series Liefertermine mit Datum, Untervorgänge mit String "Untervorgang"
         
         
        if (liefertermin["LT"] == "Intern").all() and (liefertermin["parent"] == "Intern").all():# Prüft ob alle Rows "Intern" sind -> keine Möglichkeit weiter auszuwerten 
            print("All")
            pass
        else:
            print("else")
        
        
            liste_termin= []
            liste_termin_1 = []  
            for index, row in liefertermin.iterrows():  # Iterieren über DataFrame, bestehend aus LT ind parent, begrenzt auf IDs von df_actual_d
                if row["LT"] == "Intern" and row["parent"] != "Intern":
                    vorgaenger =  int(row["parent"]) # Fügt parent-ID der Liste hinzu, wenn kein Liefertemin vorhanden ist
                    liste_termin.append(vorgaenger)
                elif type((row["LT"]) is pd.Timedelta):
                    liste_termin.append(row["LT"])  # Fügt Liefertermin der Liste hinzu
                 
            liefertermin_1 = liefertermin.assign(LT_1 = liste_termin)# Neue erzeugte Liste aus IDs und Lieferterminen hinzufügen 
            
            # Liste mit Lieferteminen und IDs durchlaufen, und von allen IDs die Liefertermine aufrufen  
            for index, row in liefertermin_1.iterrows(): # Iterrieren über eine Series eines DataFrames mit der Liste aus LTs und parents
                lt_1_value = row["LT_1"]
                if type(row["LT_1"]) is int: # Wenn ID-Nr gefunden wird, dann soll Liefertermin eingesetzt werden
                
                    lt_1_value = str(lt_1_value)
                    if lt_1_value in datenPool_aufgeräumt.index: # Sucht IDs aus den Rohdaten, außerhalb df_actual_d
                        
                        parent_row = datenPool_aufgeräumt.loc[lt_1_value] # Wählt die Rows der IDs aus
                        parent_lieferttermin = parent_row["LT"] # Entnimmt die Series aus den Rows
                        liste_termin_1.append(parent_lieferttermin) 
                        
                elif type((row["LT_1"]) is pd.Timedelta):
                     liste_termin_1.append(row["LT_1"])
             
            liefertermin_2 = liefertermin_1.assign(LF_2 = liste_termin_1)
            liefertermin_2 = liefertermin_2.fillna("Intern")
            
            df_actual_d_LT = df_actuald_d_2dn.merge(liefertermin_2, left_on='parent', right_index=True) # Fügt die beiden DataFrames <df_actuald_d_2dn> und <liefertermin_2> anhand der Values aus Liefertermin_2["parent"] zusammen
            
            lf_2 = df_actual_d_LT["LF_2"]
            lf_2 = lf_2.mask(lf_2 == "Intern", "") # ersetzt alle Intern-Einträge durch leere Strings, da sonst das Umwandeln in DateTime nicht funktioniert
            lf_2 = pd.to_datetime(lf_2) # Format in DateTime umwandeln
            lf_2 = lf_2.dt.date # Umwandel in date
            lf_2 = lf_2[~lf_2.index.duplicated(keep='first')] # alle doppelten IDs löschen
            LT = df_actual_d["LT"]
            
            df_actual_d = df_actual_d.drop(["LT"], axis = 1) # Series LT aus df_actual_d löschen, um danach korrigierte Daten wieder als LT eintragen zu können
            
            lf_2 = lf_2.combine_first(LT) # alle Liefertemine aus LT in lf_2 übertragen, falls der Eintrag aus einem leeren String besteht
            
            df_actual_d = df_actual_d.assign(LT = lf_2) # lf_2 als neue 
            return df_actual_d
        
            