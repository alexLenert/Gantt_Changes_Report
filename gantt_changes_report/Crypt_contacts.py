# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 23:55:52 2023

@author: Student
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May  8 11:49:18 2023

@author: Student
"""
"""
06.08.2023 Sende-E-Mail-Konto geändert
"""

 
class kontakt:
    
    
    def __init__(self):
        self.passwort = "" # Passwort in ord-Zahlen -1 mit _ als Trenner verwenden
        self.pw = ""
        
        self.name = "" # email-adresse in ord-Zahlen -1 mit _ als Trenner verwenden
        self.nm = ""
    
        for i in self.passwort.split("_"):
            i = int(i)+1
            self.pw +=(chr(int(i)))
        
        for i in self.name.split("_"):
            i = int(i)+1
            self.nm +=(chr(int(i)))
  
# x = kontakt().pw  # Erzeugt Passwort nur zum testen
# y = kontakt().nm  # Erzeugt E-Mail-Adresse nur zum testen
