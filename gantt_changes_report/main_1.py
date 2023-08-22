# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 00:06:04 2023

@author: Student
"""

"""
Achtung, E-Mail-Sende-Konto ändern!!! Nicht mehr über die Adresse von E + H senden!!



"""

from Abspeichern import Save
from Send_mail import send

class main():
    
    def __init__(self):
        self.Save = Save
        self.to = self.Save.email
        self.subject = "Diese Daten wurden gefunden: "
        self.body = "GanttProjekt Statusvergleich"
        self.path = self.Save.ausgabe
        self.filename = self.Save.Datei_Name
        self.attachment_path = self.path + self.filename + ".html" 
        
        if len(self.to) > 0:
            send.send_email(self.to, self.subject, self.body, self.attachment_path)
        
main()
