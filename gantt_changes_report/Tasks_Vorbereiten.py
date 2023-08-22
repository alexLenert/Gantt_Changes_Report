# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 23:00:13 2023

@author: Student
"""

import pandas as pd
from GetFromGui import GetFromGUI as GT

import re


class TagsAuswaehlen ():# Klasse tagsAuswaehlen bezieht XML-Auswahl aus Klasse ablaufen

    def __init__(self):
        geber = GT()# Komposition
        geber.createData()
        geber.text()
        self.text_1 = geber.getText()[0]
        self.text_2 = geber.getText()[1]
        self.dict_1 = geber.getDict()[0]
        self.dict_2 = geber.getDict()[1]
        self.datei_1 = geber.getDatei()[0]
        self.datei_2 = geber.getDatei()[1]
        self.List_resources = self.only_if_Resources(self.text_1)
        self.ausgabe = geber.ausgeben
        self.email = geber.getEmail()
        
        
    def task_zahl (self): # verwendet die ausgegebene liste aus einlesen.text()
        text_1 = self.text_1
        text_2 = self.text_2
        
        Anzahl_aller_tasks_xml_1 = text_1.count("<task id=")# durchzählen der task-ids im Text
        Anzahl_aller_tasks_xml_2 = text_2.count("<task id=")
        return Anzahl_aller_tasks_xml_1, Anzahl_aller_tasks_xml_2
    
    def dict_auf_tasks_begrenzen(self):
        def task(dictionary):
            d = dictionary
            d = d["project"]["tasks"]
            d = d["task"]
            return d 
        task_XML_1 = task(self.dict_1)
        task_XML_2 = task(self.dict_2)
        return task_XML_1, task_XML_2
        
    def properties_x (self): # verwendet das erste Elemelt der ausgegebenen liste aus einlesen.text()
        
        def properties_erzeugen(dictionary): 
            d = dictionary["project"]["tasks"]            
            properties_original = pd.DataFrame(d["taskproperties"]["taskproperty"]) # ertstellt DataFrame der Columns -> type, priority,info, name, beginndate...
            properties = properties_original.rename(columns=lambda x: str.replace(x, "@", ""))   # "@" im Spaltennamen führt zu KeyError.
            properties = properties.loc[properties["type"] == "custom"]    
            return properties
        
        properties_XML_1 = properties_erzeugen(self.dict_1)
        properties_XML_2 = properties_erzeugen(self.dict_2)
        return properties_XML_1, properties_XML_2
    
    def only_if_Resources(self, text_1):
        

        text = self.text_1

        search = re.findall(
            """allocation task-id="(\d*)" resource-id="(\d*)" """, text)  # alle ids -> resource
        liste_resources = []
        try:
            for i in search:
                x = i[0]
                if x.isdigit():
                    # print("isDigit")
                    liste_resources.append(x)  # alle IDs in allocations
                else:
                    print("isNoDigit")
                    continue
        except ValueError:
            print("Anderer Fehler")
        return liste_resources
    
    
    def getDict(self):
        return self.dict_1, self.dict_1
    def getDatei(self):
        return self.datei_1, self.datei_2
    
#tagCheck = TagsAuswaehlen()
#email = tagCheck.email
#liste_Anzahl_aller_tags = tagCheck.task_zahl()
#liste_task = tagCheck.dict_auf_tasks_begrenzen()
#liste_properties = tagCheck.properties_x()

