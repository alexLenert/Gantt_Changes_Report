# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:34:19 2023

"""

# emailSpeicher= "C:/dev/Spyder_Workspace/xml_Python_panda/XML_Ausgabe/"
"""
Die Klasse path liest aus den Textdateien xml_ordner.txt und ausgebe_ordner.txt die Pfade aus,
 und weist sie den Klassenvariablen eilesen und ausgeben zu
"""




import os
import sys
class Path ():

    def __init__(self):
        # positionierung mit Sys: findet nach Kopie hoffentlich den aktuellen Standort
        self.exe_pfad = os.path.abspath(sys.argv[0])
        self.txt_folder = os.path.join(os.path.dirname(
            self.exe_pfad), os.pardir, 'Data')  # Nur für den normlen Ablauf
        # self.txt_folder = os.path.join(os.path.dirname(self.exe_pfad), 'Data') #Nur zum localen testen

        self.xml_ordner = os.path.join(self.txt_folder, 'xml_ordner.txt')
        self.ausgabe_ordner = os.path.join(
            self.txt_folder, 'ausgabe_ordner.txt')

        self.einlesen = open(self.xml_ordner, encoding="utf-8").read()
        self.ausgeben = open(self.ausgabe_ordner, encoding="utf-8").read()

    def get_einlesen(self):
        return self.einlesen

    def get_ausgeben(self):
        return self.ausgeben


# test = Path()

# einlesen = test.einlesen

# abspeichern = test.ausgeben
