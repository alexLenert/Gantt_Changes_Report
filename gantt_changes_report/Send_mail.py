# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 23:57:22 2023

@author: Student
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 13:31:27 2023

@author: Alexander lenert
"""


import smtplib # Postausgang
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os




from Crypt_contacts import kontakt



class send():
     
    # pw = kontakt().pw  # Erzeugt Passwort nur zum testen
    # email = kontakt().nm
                
    def send_email(to, subject, body, attachment_path):# email und Passwort aus wird nur in der Methode aufgerufen
        sender_email = kontakt().nm                    # In Methode aufgerufen, erzeugt keine Klassen-Variablen!!
        sender_password = kontakt().pw
    
        # Create message container
        message = MIMEMultipart() # Art des Email-Containers
        message['From'] = sender_email
        message['To'] = ','.join(to) # für mehrere E-Mail-Adressen
        message['Subject'] = subject # Betreffzeile
    
        # Add body to message
        message.attach(MIMEText(body, 'plain'))
    
        # Add attachment to message
        with open(attachment_path, 'rb') as file:
            attach = MIMEApplication(file.read(),_subtype="html")
            attach.add_header('Content-Disposition', 'attachment', filename=str(attachment_path))
    
        message.attach(attach)
    
        # Create SMTP session
        #session = smtplib.SMTP_SSL(host='smtp.web.de', port=587)
        session = smtplib.SMTP_SSL(host='smtp.web.de', port=465)
        
        #session.starttls()#keyfile / certfile notwendig?
        session.login(sender_email, sender_password)
    
        # Send mail
        text = message.as_string()
        session.sendmail(sender_email, to, text)
        session.quit()
    
        print('Mail Sent')

    