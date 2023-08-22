# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:06:29 2023

@author: Student
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:57:02 2023

@author: Alexander Lenert
"""

"""


"""
# in Strategy-Pattern ausführen




import pandas as pd
from abc import ABC, abstractmethod
from Vergleich import Vergleichen
class Entscheiden ():

    def __init__(self):
        Vergleich = Vergleichen()
        self.df_1 = Vergleich.getDF()[0]
        self.df_2 = Vergleich.getDF()[1]
        
        self.ergebnis = Vergleich.mycompare(self.df_1, self.df_2)
        self.datei_1 = Vergleich.getDatei()[0]
        self.datei_2 = Vergleich.getDatei()[1]
        self.list_resources = Vergleich.Lise_resources
        self.ausgeben = Vergleich.ausgeben
        self.zusatz = ""
        self.email = Vergleich.email

    def getErgebnis(self):
        return self.ergebnis

    # Bevor Daten verarbeitet werden können wird geprüft, welche Daten gefunden wurden:

    # Parameterliste-> comp aus mycompare,  datei_1 Dateinamen 1.Datei, datei_2 Dateinamen 2.Datei
    def fall_if(self, comp, datei_1, datei_2):
        # Leere Ausgaben werden initialisiert, und können -im Fall der Existens- überschrieben werden
        df_actual_d_show = pd.DataFrame()
        df_actual_d = pd.DataFrame()     # So wird ein Ausnahme-Fehler abgefangen
        verschieben = pd.Series(dtype=object)
        verlaengern = pd.Series(dtype=object)
        df_start_self = pd.Series(dtype=object)
        df_start_other = pd.Series(dtype=object)
        df_duration_self = pd.Series(dtype=object)
        df_duration_other = pd.Series(dtype=object)
        zusatz = ""

        df_sorted = comp["delta"]
        added = comp["added"].fillna("")
        deleted = comp["deleted"].fillna("")
        added = added.fillna("")
        deleted = deleted.fillna("")

        # Zustand:Gleicher Inhalt-> delta ist leer-> es wurden keine veränderten Daten gefunden
        if pd.DataFrame(comp["delta"]).empty:
            self.zusatz = "Es gibt keine Veränderung \n" + "Verglichene Dateien: " + \
                " < " + str(datei_1) + " > und < " + str(datei_2) + ">"
            print(zusatz)
            df_actual_d_show = comp["delta"]
            print("Leer")

        # Zustand:Ungleicher Inhalt-> delta ist nicht leer, aber es befinden sich keine veränderten Daten zu start und duration in delta
        elif ('duration', 'self') not in comp["delta"] and ('duration', 'other')not in comp["delta"] and ('start', 'self') not in comp["delta"] and ('start', 'other')not in comp["delta"] and ('IGNORE', 'self') in comp["delta"] and ('IGNORE', 'other') in comp["delta"]:

            self.zusatz = "Struktur wurde verändert \n" + "Verglichene Dateien: " + \
                " < " + str(datei_1) + " > und < " + str(datei_2) + ">"
            print(zusatz)
            # entnimmt aus newy alle Einträge nach dem Index von df_sorted
            new2 = comp["new"].loc[df_sorted.index]

            # enthält durch den Vergleich auch NaN!
            df_labeled = df_sorted.rename(
                columns={'start': 'start1', 'duration': 'duration1'})

            # axis von 0 auf 1 geändert --AL-- fügt die Vergleichsange
            df_concated = pd.concat([df_labeled, new2], axis=1)
            df_actual_d_show = df_concated.fillna(
                "")  # comp["delta"]# df_actual_d_show
            print("keine Zeiten")
		
        #elif ('IGNORE',  'self') and ('IGNORE', 'other') in comp["delta"]:

        #    self.zusatz = "Struktur wurde verändert \n" + "Verglichene Dateien: " + \
        #        " < " + str(datei_1) + " > und < " + str(datei_2) + ">"
        #    print(zusatz)
            # entnimmt aus newy alle Einträge nach dem Index von df_sorted
        #    new2 = comp["new"].loc[df_sorted.index]

            # enthält durch den Vergleich auch NaN!
        #    df_labeled = df_sorted.rename(
        #        columns={'start': 'start1', 'duration': 'duration1'})

            # axis von 0 auf 1 geändert --AL-- fügt die Vergleichsange
        #    df_concated = pd.concat([df_labeled, new2], axis=1)
        #    df_actual_d_show = df_concated.fillna(
        #       "")  # comp["delta"]# df_actual_d_show
        #    print("IGNORE ")
        else:
            # Zustand:Ungleicher Inhalt ->  Es befinden sich veränderte Daten von start und duration in delta
            self.zusatz = "Verglichene Dateien: " + " < " + \
                str(datei_1) + " > und < " + str(datei_2) + ">"
            print(zusatz)
            print("Full ")
            # entnimmt aus new alle Einträge nach dem Index von df_sorted
            new2 = comp["new"].loc[df_sorted.index]

            # enthält durch den Vergleich auch NaN!
            df_labeled = df_sorted.rename(
                columns={'start': 'start1', 'duration': 'duration1'})

            # axis von 0 auf 1 geändert --AL-- fügt die Vergleichsangeben von Start und Duration mit new2 zusammen
            df_concated = pd.concat([df_labeled, new2], axis=1)

            # Parents herausfiltern
            # parents = df_concated["parent"].dropna()
            # parents = parents.values

            # parents = df_concated.index.drop(parents, errors = "ignore")# es gibt task-ids die gedropt werden sollen, aber nicht in df_concated vorhanden sind, daher errors = ignore
            # df_concated = df_concated.reindex(index= parents)# df_concated enthält jetzt keine task-ids mehr, die in der Column "parents" verzeichnet sind

            df_actual_d = df_concated

            def startAufbereiten(df, df_old, df_new):
                # Spalte in dateTime konvertieren
                df_start_self = pd.to_datetime(df[('start1', 'self')])
                # Spalte in dateTime konvertieren
                df_start_other = pd.to_datetime(df[('start1', 'other')])

                # fügt Spalte Verschiebung mit Zeitdifferenz aus start_self und start_other in den aktuellen DataFrame
                df_actual_d1 = df_concated.assign(
                    Verschiebung= df_start_other - df_start_self)

                df_actual_d = df_actual_d1
                return [df_actual_d, df_start_self, df_start_other]

            if ('start1', 'self') and ('start1', 'other') in df_concated:
                print("start!!")

                liste_start = startAufbereiten(
                    df_concated, comp["old"], comp["new"])

                df_actual_d = liste_start[0]
                df_start_self = liste_start[1]
                df_start_other = liste_start[2]

                df_actual_d["Verschiebung"] = df_actual_d["Verschiebung"].dt.days.astype(
                    int)
                verschieben = df_actual_d["Verschiebung"]

            def durationAufbereiten(df, comp, df_start):
                # fügt der Zahl den String days hinzu, wodurch --datetime-- jetzt erkennen kann um welche Einheitz es sich bei der Zahl handelt
                df_duration_self_d = ((df[('duration1', 'self')]) + "days")
                df_duration_other_d = ((df[('duration1', 'other')]) + "days")

                # formatiert die Zahl und den String in ein datetime-Format
                df_duration_self = pd.to_timedelta(df_duration_self_d)
                df_duration_other = pd.to_timedelta(df_duration_other_d)

                # fügt Spalte Verlängerung mit Zeitdiferenz aus duration_self und duration_other hinzu
                df_actual_d = df_start.assign(
                    Verlaengerung= df_duration_other - df_duration_self)

                return [df_actual_d, df_duration_self, df_duration_other]

            if ('duration1', 'self') and ('duration1', 'other') in df_concated:
                print("duration!!")
                liste_duration = durationAufbereiten(
                    df_concated, comp, df_actual_d)
                df_actual_d = liste_duration[0]
                df_duration_self = liste_duration[1]
                df_duration_other = liste_duration[2]

                df_actual_d["Verlaengerung"] = df_actual_d["Verlaengerung"].dt.days.astype(
                    int)
                verlaengern = df_actual_d["Verlaengerung"]
        return [df_actual_d, df_actual_d_show, verschieben, verlaengern, df_start_self, df_start_other, df_duration_self, df_duration_other, zusatz, added, deleted]

#Entscheidung = Entscheiden()
#ausgeben = Entscheidung.ausgeben
#Ausgabe = Entscheidung.fall_if(Entscheidung.ergebnis, Entscheidung.datei_1, Entscheidung.datei_2)
#Ausgabe_1 = Entscheidung.ergebnis
