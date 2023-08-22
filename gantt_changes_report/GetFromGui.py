# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 13:33:41 2023

@author: Student


Fuktioniert als Übergeber
"""
import xmltodict
from GUI_Manager_2 import App_1
from Pfade import Path

class GetFromGUI:
    
        
    def __init__(self):
        
        self.XML_1 = ""
        self.XML_2 = ""
        self.Email = ""
        self.dict_1 = ""
        self.dict_2 = ""
        self.text_1 = ""
        self.text_2 = ""
        self.ausgeben = Path().get_ausgeben()
        return     
    
    def createData(self):
        app = App_1()
        self.XML_1 = App_1.setAuswahl_XML(app)[0]
        self.XML_2 = App_1.setAuswahl_XML(app)[1] 
        self.Email = App_1.setAuswahl_E_Mail(app)
        app.master.destroy()
        #return self.XML, self.Email
    
    def text (self):
        pfad = Path().einlesen
        datei_1 = self.XML_1
        datei_2 = self.XML_2
        
        def xml_todict(datei):
            ganzer_Pfad= pfad+ "/" +datei 
            text = ""
            try:
                with open(ganzer_Pfad) as f:
                    text = f.read()
            except IOError as e:
                print("Fehler beim Öffen: " ,e)
            
            # text = open(pfad+ "/" +datei).read() #geändert auf try - except  
            
            d = xmltodict.parse(text)
            return d, text
        self.text_1 = xml_todict(datei_1)[1]
        self.text_2 = xml_todict(datei_2)[1]
        self.dict_1 = xml_todict(datei_1)[0]
        self.dict_2 = xml_todict(datei_2)[0]
        
        
    def getText(self):
        return self.text_1, self.text_2
    def getDict(self):
        return self.dict_1, self.dict_2
    def getEmail(self):
        return self.Email
    def getDatei(self):
        return self.XML_1, self.XML_2
   
   

# geber = GetFromGUI()
# ausgeben = geber.ausgeben
# geber.createData()
# #xml = geber.XML
# email = geber.Email
# #print(GetFromGUI().XML)
# #print(GetFromGUI().Email)
# geber.text()
# liste_Text = geber.getText()
# liste_Dict = geber.getDict()
# liste_Email = geber.getEmail()
# dictionary = liste_Dict[0]
# dictionary["project"]["tasks"] 
# test = geber.getDict()[0]
# test["project"]["tasks"] 

