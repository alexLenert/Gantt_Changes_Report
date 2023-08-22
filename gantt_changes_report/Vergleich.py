# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:33:05 2023

@author: Student
"""

import pandas as pd

from Tags_einsortieren import Einsortieren
from Labels_adjust import Label_sync

class Vergleichen():
    
    def __init__(self):
        Sort = Einsortieren()
        self.properties_1 = Sort.getProperties()[0]
        self.properties_2 = Sort.getProperties()[1]
        self.tasks_1 = Sort.getTasks()[0]
        self.tasks_2 = Sort.getTasks()[1]
        self.datei_1 = Sort.getDatei()[0]
        self.datei_2 = Sort.getDatei()[1]
        self.anzahl_tasks_Datei_1 = Sort.getTasks()[0]
        self.anzahl_tasks_Datei_2 = Sort.getTasks()[1]
        self.df_1_x = Sort.xml_einlesen(self.tasks_1, self.properties_1, self.datei_1)
        self.df_2_x = Sort.xml_einlesen(self.tasks_2, self.properties_2, self.datei_2)
        self.Label_adjust = Label_sync.use_sync( self.df_1_x, self.df_2_x)
        self.df_1_a = self.Label_adjust[0] # Datenpool für OLD
        self.df_2_a = self.Label_adjust[1] # Datenbpool für NEW
        self.df_1 = self.use_drop_1() # Datenpool ohne IGNOR
        self.df_2 = self.use_drop_2() # Datenpool ohne IGNOR
        self.Anzahl_aller_tasks_1 = Sort.getAnzahlTasks()[0]
        self.Anzahl_aller_tasks_2 = Sort.getAnzahlTasks()[1]
        self.Lise_resources = Sort.list_resources
        self.ausgeben = Sort.ausgeben
        self.email = Sort.email
        
        
        print(f' {self.Anzahl_aller_tasks_1} :  {self.df_1.shape}') # Anzahl der Series im df, Anzahl der Rows im df
        print(f' {self.Anzahl_aller_tasks_2} :  {self.df_2.shape}') # Anzahl der Series im df, Anzahl der Rows im df
        
        if self.df_1.shape[0] == self.Anzahl_aller_tasks_1:
            print("Alle Eintraege gefunden") # Nur wenn die Anzahl der Tasks mit den Rows in Shape übereinstimmt
        if self.df_2.shape[0] == self.Anzahl_aller_tasks_2:
            print("Alle Eintraege gefunden")

        
    
    def mycompare(self,old1, new2):
    
    # gelöschte und neue Vorgänge erfassen
        output = {} # leeres dict für Sammlung (geänderte, gelöschte und hinzugefügte Vorgänge)
        old = old1
        new = new2
          
        list1 = list(old1.index)
        list2 = list(new2.index)
        
        
        deleted = [i for i in list1 if i not in list2] # Liste der IDs old die nicht in new sind
        added =   [i for i in list2 if i not in list1] # Liste der IDs new die nicht in old sind
        
        print(f'Länge Added: {len(added)}')
        print(f'Länge Deleted: {len(deleted)}')

        if len(added) or len(deleted) > 0: # wenn die IDs zwischen old und new unterschiedlich sind -> erzeugt für beide befüllte Listen: 
            print("IF")
    
            output["deleted"] = old1.loc[deleted]
            
            output["added"] = new2.loc[added]
         
            # old und new vergleichen
            # abweichende Zeilen aus old, new löschen (df.compare kann nur identically-labeled
            old1 = old1.drop(deleted)
            new2 = new2.drop(added)
                    
            old1 = old1.drop(["name"], axis=1) # Namensänderungen werden nicht aufgenommen (z.B. Metrology -> Metrology MX203)
            new2 = new2.drop(["name"], axis=1)
            
            old1 = old1.sort_index() 
            new2 = new2.sort_index()
            comp = new2.compare(old1, keep_equal= True) # Zusatz keep_equal= True erspart die Methoden getStart und getDuration
            output["delta"] = []
           
            output["delta"] = comp
            output["old"] = old
            output["new"] = new
            output["OLD"] = self.df_1_a
            output["NEW"] = self.df_2_a
            
            
        else :    
        #elif len(added) and len(deleted) == 0: # wenn die IDs von old und new identisch sind  -> erzeugt für beide leere Listen:
            print("ELSE")
            #=============================================
            
            
            #=============================================
            old1 = old1.drop(["name"], axis=1) # Namensänderungen werden nicht aufgenommen (z.B. Metrology -> Metrology MX203)
            new2 = new2.drop(["name"], axis=1)
            
            old1 = old1.sort_index() 
            new2 = new2.sort_index()
            
            comp = old1.compare(new2, keep_equal= True) # Zusatz keep_equal= True erspart die Methoden getStart und getDuration
            output["old"] = old
            output["new"] = new
            output["OLD"] = self.df_1_a
            output["NEW"] = self.df_2_a
            output["delta"] = []
            output["delta"] = comp
           
            
            output["added"] = pd.DataFrame(columns={"name":"0", "Kunde":"0", "SN":"0","LT":"0","parent":"0"})# parents!
            output["deleted"] = pd.DataFrame(columns={"name":"0", "Kunde":"0", "SN":"0","LT":"0","parent":"0"})
            
            
        # print("DELTA: " + str(len(output["delta"])))
        # print("------------output:---------------- ")
        # print(output)
        return output
    
    def drop_notrelevant_1(self, df_1_a):

        not_relevant_list1 = []
        not_relevant_list1_index = []
        if "IGNORE" in self.df_1_a.columns:
            print("IGNORE in df_1_a")
            for index, row in self.df_1_a["IGNORE"].items():
                if row == "true":
                    print("true gefunden")
                    not_relevant_list1.append(row)
                    not_relevant_list1_index.append(index)
                    print(not_relevant_list1_index)

        # Gesammelte, nicht relevanten Daten
        nichtrelevate_Daten = pd.DataFrame(not_relevant_list1, not_relevant_list1_index)
        return nichtrelevate_Daten
        
    def drop_notrelevant_2(self, df_2_a):

        not_relevant_list2 = []
        not_relevant_list2_index = []
        if "IGNORE" in self.df_2_a.columns:
            print("IGNORE in df_2")
            for index, row in self.df_2_a["IGNORE"].items():
                if row == "true":
                    print("true gefunden")
                    not_relevant_list2.append(row)
                    not_relevant_list2_index.append(index)
                    print(not_relevant_list2_index)

        # Gesammelte, nicht relevanten Daten
        nichtrelevate_Daten = pd.DataFrame(not_relevant_list2, not_relevant_list2_index)
        return nichtrelevate_Daten

    def use_drop_1(self):

        nichtrelevate_Daten_df_1 = Vergleichen.drop_notrelevant_1(self, self.df_1_a)

        """
        Löschen einer Row vor dem Vergleichen darf nicht den DatenPool einschränken!!
        """
        # Sollte diese Funktion zum Einsatz kommen, muss df_1_test in -> df_1 bzw. df_2_test in -> df_2 geändert werden
        # aus df_concated werden alle Rows mit den IDs aus den nichtrelevanten Daten gelöscht
        self.df_actual_d_1 = self.df_1_a.drop(nichtrelevate_Daten_df_1.index)
        return self.df_actual_d_1
        
    def use_drop_2(self):

        nichtrelevate_Daten_df_2 = Vergleichen.drop_notrelevant_2(self, self.df_2_a)
        

        """
        Löschen einer Row vor dem Vergleichen darf nicht den DatenPool einschränken!!
        """
        # Sollte diese Funktion zum Einsatz kommen, muss df_1_test in -> df_1 bzw. df_2_test in -> df_2 geändert werden
        # aus df_concated werden alle Rows mit den IDs aus den nichtrelevanten Daten gelöscht
        self.df_actual_d_2 = self.df_2_a.drop(nichtrelevate_Daten_df_2.index)
        return self.df_actual_d_2
    
    
    def getDF(self):
        return self.df_1, self.df_2
    def getDatei(self):
        return self.datei_1, self.datei_2





# Vergleich = Vergleichen()

# df_1_x = Vergleich.df_1_x
# df_2_x = Vergleich.df_2_x
# df_2 = Vergleich.df_2
# df_1 = Vergleich.df_1

# df_1_test = Vergleich.df_1
# df_2_test = Vergleich.df_2

# df_1_dropped = Vergleich.use_drop_1()
# df_2_dropped = Vergleich.use_drop_2()

# comp = Vergleich.mycompare(Vergleich.df_1, Vergleich.df_2)