# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:45:48 2023

@author: Alexander Lenert
"""

import pandas as pd
from workalendar.europe import Germany
import datetime



 
class zeiten ():
    
    def zeitenBerechnen (comp, start_xml1, dauer_xml1, df_actual_d, verschieben, verlaengern):
        
        #Quell-Daten um lokal testen zu können:
        #dauer_xml1 = liste[7]#.dt.days # nur zum testen !!!
        #start_xml1 = liste[5]#.dt.date # nur zum testen !!!
        #df_actual_d = df_actual_d# nur zum testen !!!
        #verlaengern = liste[3]   # nur zum testen !!!
        #verschieben = liste[2]   # nur zum testen !!!
        #=====================================================
        #start und dauer müssen abhägig von einander jeweils einen default-Wert mit 0 days bzw. die daten von comp["old"]log[dauer_xml1.index] bekommen
        """
        Wenn zwei XML-Dateien verglichen werden, bei denen NUR start oder NUR duration geändert wurde, 
        wird kein Wert für das jeweils unveränderte Tag-Element erstellt.
        Damit das Programm nicht in einen Ausnahme-Fehler fällt, werden hier die Werte extra berechnet.
        Dazu werden zuerst default-Series erstellt, falls ein benötigter Wert leer bleibt
        """
        if start_xml1.empty:
            start_x = comp["old"].loc[dauer_xml1.index]
            start_xml1 = start_x["start"]
            start_xml1 = pd.to_datetime(start_xml1)
        if dauer_xml1.empty:
            dauer_x = comp["old"].loc[start_xml1.index]
            dauer_xml1 = dauer_x["duration"]
            dauer_xml1 = pd.to_timedelta(dauer_xml1)
        if verschieben.empty:
            verschieben = start_xml1 - pd.to_datetime(comp["new"].loc[start_xml1.index]["start"])
            verschieben = verschieben.dt.days
        if verlaengern.empty:
            verlaengern = dauer_xml1 - pd.to_timedelta(comp["new"].loc[dauer_xml1.index]["duration"])
            verlaengern = verlaengern.dt.days            
        dauer = dauer_xml1.dt.days
        start = start_xml1.dt.date
       
        
        dauer_liste = []
        dauer_liste_index =[]
        verschiebung_liste = []
        verschiebung_liste_index = [] 
        verlaengerung_liste =[]
        verlaengerung_liste_index = []
        s_datum = pd.Series(dtype=object)
        s_verschieben = pd.Series(dtype=object)
        s_verlaengern = pd.Series(dtype=object)
        # In listen die berechnete Zeit eintragen: Wenn (+)Wert -> add_working_days , wenn (-)Wert -> sub_working_days
        """
        Hier werden start, dauer, verlängern und verschieben mit add_working-days bzw. sub_working_days aufgerechnet
        """
        for index, value in dauer.items():
            
            if value >= 0:#                  plus                   datum          dauer
                dauer_liste.append(Germany().add_working_days(start.loc[index], dauer.loc[index]))
                dauer_liste_index.append(index)
            if value < 0:#                  minus                   datum          dauer
                dauer_liste.append(Germany().sub_working_days(start.loc[index], dauer.loc[index]))
                dauer_liste_index.append(index)
        s_datum = pd.Series(dauer_liste, dauer_liste_index) # Series mit richtigen Indizes erstellen -> End-Datum vor Veränderung
        
        # Veränderungen einrechnen:
        for index, value in verschieben.items():
            
            if value >= 0:#                                         
                verschiebung_liste.append(Germany().add_working_days(s_datum.loc[index], verschieben.loc[index]))#  auf die Series Verschiebung anrechnen
                verschiebung_liste_index.append(index)
            if value < 0:
                verschiebung_liste.append(Germany().sub_working_days(s_datum.loc[index], verschieben.loc[index]))#  auf die Series Verschiebung anrechnen
                verschiebung_liste_index.append(index)
        s_verschieben = pd.Series(verschiebung_liste, verschiebung_liste_index) #neue Series mit Korrektur der Verschiebung   
        
        for index, value in verlaengern.items():

            if value >= 0:
                verlaengerung_liste.append(Germany().add_working_days(s_verschieben.loc[index], verlaengern.loc[index])) #  auf die Series Verlängerung anrechnen
                verlaengerung_liste_index.append(index)
            if value < 0:
                verlaengerung_liste.append(Germany().sub_working_days(s_verschieben.loc[index], verlaengern.loc[index])) #  auf die Series Verlängerung anrechnen
                verlaengerung_liste_index.append(index)
        s_verlaengern = pd.Series(verlaengerung_liste, verlaengerung_liste_index) # neue Series mit Korrektur der Verlängerung 
        
        return [s_verlaengern, s_datum]
    
    
    def datumVergleichen(df, datum_w, datum_s):
        df_lt = df["LT"]
        liste = []
        liste_index= []
        meldung = pd.Series#(dtype=object) muss auskommentiert bleiben, sonst Fehlermeldung Series ist not callable
        
        counter = 0
        for index, value in df_lt.items():
           
            index1 = index
            if str(datum_w[counter]).split(" ")[0] > str(datum_s[counter]).split(" ")[0]:# start+duration mit start+duration+verlaengern+verschieben vergleichen
                late = "late"
                liste.insert(int(index1),late)
                liste_index.insert(int(index1), index1)
                counter = counter +1
            else:
                liste.insert(int(index1), "early")
                liste_index.insert(int(index1), index1)     
                counter = counter +1  
               
        meldung = meldung(liste, index = liste_index) 
        df_actual_d = df.assign(Ende = meldung) #Geändert von LT_verschoben auf LT_P_verschoben
        
        return df_actual_d
    
    
    def LT_Vergleichen(df, datum_w, parent_datum):
        df_lt = df["LT"]
        liste = []
        liste_index= []
        meldung = pd.Series
        
        counter = 0
        for index, value in df_lt.items():
           
            index1 = index
            if str(datum_w[counter]).split(" ")[0] > str(df["LT"][counter]).split(" ")[0]:#df_lt #parent_datum
                ja = True
                liste.insert(int(index1),ja)
                liste_index.insert(int(index1), index1)
                counter = counter +1
            else:
                liste.insert(int(index1), "")
                liste_index.insert(int(index1), index1)     
                counter = counter +1  
               
        meldung = meldung(liste, index = liste_index) 
        df_actual_d = df.assign(LT_verschoben = meldung)
        
        return df_actual_d
    
    def LT_one(df):  # Führt Series Ende und LT_verschoben zusammen, wobei LT_verschoben (True) Series Ende überdeckt
        s_ende = df["Ende"]
        s_LT_verschoben = df["LT_verschoben"]  
        LT_neu = s_LT_verschoben.mask(s_LT_verschoben == "", s_ende)
        df = df.assign(LT_verschoben = LT_neu)
        return df
        