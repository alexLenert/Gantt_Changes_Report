# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:44:11 2023

@author: Student
"""
from Tasks_Vorbereiten import TagsAuswaehlen
import pandas as pd
import re

class Einsortieren():
    
    def __init__(self):
        TagCheck = TagsAuswaehlen()# Komposition
        self.Anzahl_aller_tags_XML_1 = TagCheck.task_zahl()[0]
        self.Anzahl_aller_tags_XML_2 = TagCheck.task_zahl()[1]
        self.task_XML_1 = TagCheck.dict_auf_tasks_begrenzen()[0] # nur tasks
        self.task_XML_2 = TagCheck.dict_auf_tasks_begrenzen()[1] # nur tasks
        self.properties_XML_1 = TagCheck.properties_x()[0]
        self.properties_XML_2 = TagCheck.properties_x()[1]
        self.dict_1 = TagCheck.getDict()[0]
        self.dict_2 = TagCheck.getDict()[1]
        self.datei_1 = TagCheck.getDatei()[0]
        self.datei_2 = TagCheck.getDatei()[1]
        self.list_resources = TagCheck.List_resources
        self.ausgeben = TagCheck.ausgabe
        self.email = TagCheck.email
        
  
        
        
        
        
    def taskdict_to_df (self, d, properties):     # braucht eine list of ordered dicts. Diese entsteht auch aus Subvorgängen
        
        # properties ist ein df mit eingelesenen customproperties    
        tasks = pd.DataFrame(d) # alle Muttervorgänge in Dataframe umwandeln  
     
        tasks = tasks.rename(columns=lambda x: str.replace(x, "@", ""))   # "@" im Spaltennamen führt zu KeyError.        
        # properties (SN, Kunde, usw.) aller tasks in Spalten übersetzen
        # nicht bei allen Subtasks nötig, da nicht alle überhaupt customproperties besitzen
        if "customproperty" in tasks.columns:
            
            df = pd.DataFrame(columns=properties["id"]) # leerer DataFrame erzeugt, # der mit for-Schleife gefüllt wird. Spalte "id" wird mit Inhalt aus der Spalte properties gefüllt        
            for i in tasks["customproperty"]:   # zeilenweise
                
                if type(i) == float:    # leere Zellen == nan abfangen -> "sollte ausgewähltes Element ein float sein"
                    i = pd.DataFrame(float("nan"), columns=properties["id"], index=[0])    # eine df Zeile mit nans erstellen -> Datentyp Float wird durch NaN ersetzt
                    df = pd.concat([df, i]) # 16.2.2023 hinzugefügt, repariert Bug der ID/Customproperty-Verschiebung
                    
                else:    
                    try:
                        i = pd.DataFrame(i)   
                       
                    except ValueError:
                        i = pd.DataFrame(i, index=[0]) # notwendig, wenn nur eine Eigenschaft eingetragen ist
                        
                    i = i.rename(columns=lambda x: str.replace(x, "@", "")) # "@" im Spaltennamen führt zu KeyError.
                    i = i.set_index("taskproperty-id") # falls 
                    
                    i = i.transpose()
                    
                    df = pd.concat([df, i]) #geändert von append (depricated) zu pd.concat --AL-- # 
                    
                    dfx = df
            df.index = range(len(df))# Index mit 0 bis n bezeichnen, sonst unambiguous indices, pd.concat funktioniert nicht
            df.columns = [properties.loc[properties["id"]==i, "name"].iloc[0] for i in df.columns]  # macht aus ids ("tpc0") unsere Bezeichnungen ("Nr."). iloc[0] ist leider nötig um aus einem Series Objekt einen String zu ziehen.      
            dfK = df
            
            tasks = pd.concat([df, tasks], axis=1)
        
        #DataFrame aufräumen (nicht benötigte Spalten löschen...)
        droplist = "meeting, complete, expand, thirdDate, thirdDate-constraint, cost-manual-value, cost-calculated, color, notes"
        droplist = droplist.split(", ")
        try:    # nicht alle aus der Liste sind in Subtasks vorhanden
            tasks = tasks.drop(droplist, axis=1)
        except KeyError as err: # err enthält Auflistung, z.B. "['cost-manual-value' 'cost-calculated'] not found in axis"
            err = re.search("\[.*\]", str(err)).group(0)
            
            err = err[1:-2].replace("'", "").split(" ") # enthält nur noch eine Liste der beiden Keys
            
            #for i in err:
            #    droplist.remove(i)
            #tasks = tasks.drop(droplist, axis=1)
        
        tasks = tasks.set_index("id")# setzt die Spalte "id" als index ein
     
        return tasks
    
             # von E+H definierte auswählen, alle anderen sind "default" begrenzt Einträge auf alle mit dem type von Wert "custom"
    
    #%%
    
    def make_one_df(self,df, properties, meldung):
        counter = 0
            
        for index, row in df.iterrows():
                            
            try:           
                task1 = row["task"]
                
                if type(task1) == dict:
                    task1=[task1]                                           
                if type(task1) == list : # Liste vorhanden => Subtasks vorhanden                                            
                                                                   
                    task2 = Einsortieren.taskdict_to_df(self,task1, properties) # 
                    
                    task2["parent"] = index # fügt den ausgelesenen Index aus der for-Schleife ->  in die Spalte "parent" ein
                    
                    #====================================================
                    df.loc[index, "task"] = meldung # Meldung hinzugefügt
                    #====================================================
                    df = pd.concat([df, task2], axis=0) # fügt mit jedem Durchlauf weitere rows hinzu
                    global dfX                            
                    dfX = df
                    
            except KeyError:
                pass
       # df = df.drop(["task"], axis=1) 
        
        # if "depend" in df.columns:
        #     df = df.drop(["depend"], axis=1)
        counter +=1
        return df
    
    def xml_einlesen (self,d, properties, datei):
        droplist = "meeting", "complete", "expand", "thirdDate", "thirdDate-constraint", "cost-manual-value", "cost-calculated", "color", "notes", "depend"
    
        df = Einsortieren.taskdict_to_df(self,d, properties) # 1. Ebene
        df = Einsortieren.make_one_df(self,df,properties, meldung="Tasks eingelesen 1")# 1. + 2. Ebene
        df = Einsortieren.make_one_df(self,df,properties, meldung="Tasks eingelesen 2") # 1.Ebene, 2.Ebene + 3. Ebene
    
        thisFilter = df.filter(droplist)
        df.drop(thisFilter, inplace=True, axis=1)
    
        print(f' {datei} :  {df.shape} einlesen') # Anzahl aller Tasks aus dem erstllten DataFrame
       
        df = df.sort_index() # Index sortieren
        df = df.reindex(sorted(df.columns), axis=1) # columns sortieren
        df = df.drop(["task","customproperty"], axis=1)
        return df
    def getProperties(self):
        return self.properties_XML_1, self.properties_XML_2
    def getDatei(self):
        return self.datei_1, self.datei_2
    def getTasks(self):
        return self.task_XML_1,self.task_XML_2
    def getAnzahlTasks(self):
        return self.Anzahl_aller_tags_XML_1, self.Anzahl_aller_tags_XML_2
    
    
    
# Sort = Einsortieren()

# df_1 = Sort.xml_einlesen(Sort.task_XML_1, Sort.properties_XML_1, Sort.datei_1)
# df_2 = Sort.xml_einlesen(Sort.task_XML_2, Sort.properties_XML_2, Sort.datei_2)

