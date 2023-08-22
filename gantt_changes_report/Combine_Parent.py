# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 01:48:59 2023

@author: Student
"""

from Parent_Data_Einfuegen import makeParData
import pandas as pd
        		

class Combine():

    def __init__(self):
        Data = makeParData()
        Data.checkValue()
        #Data.parents_in_df_actual_d_eingeben()
        Data.parents_in_added_eingeben()
        Data.parents_in_deleted_eingeben()
        self.df_actual_d = Data.df_actual_d
        self.df_actual_d_show = Data.df_actual_d_show
        self.added = Data.Ergebnis["added"]
        self.deleted = Data.Ergebnis["deleted"]
        self.SN = []
        self.index_l = []
        #self.df_SN = pd.DataFrame(dtype = object)
        #self.df_SN = self.df_actual_d["SN"]
        #self.df_SN_p = self.df_actual_d["SN_Parent"]
        #self.df_SN_p = pd.DataFrame(dtype = object)
        self.Kunde = []
        self.index_k = []
        #self.df_Kd = self.df_actual_d["Kunde"]
        #self.df_Kd = pd.DataFrame(dtype = object)
        #self.df_Kd_p = self.df_actual_d["Kunde_Parent"]
        #self.df_Kd_p = pd.DataFrame(dtype = object)
        #self.df_Kd_p = pd.DataFrame(dtype = object)
        self.list_resources = Data.list_resources
        self.zusatz = Data.zusatz
        self.ausgeben = Data.ausgeben
        self.email = Data.email

    def combine_parent(self, Series, liste, liste_index):
        #SN = []
       # index_l =  []
        for index, value in Series.items():
            if value != "":
                liste.append(value)
                liste_index.append(index)
        sn = pd.Series(liste, liste_index, dtype=object)
        return sn

    def use_combine(self):

        self.sn = Combine.combine_parent(
            self, self.df_SN, self.SN, self.index_l)

        self.sn_1 = Combine.combine_parent(
            self, self.df_SN_p, self.SN, self.index_l)

        self.kd = Combine.combine_parent(
            self, self.df_Kd, self.Kunde, self.index_k)

        self.kd_1 = Combine.combine_parent(
            self, self.df_Kd_p, self.Kunde, self.index_k)

        self.sn_1 = self.sn_1[~self.sn_1.index.duplicated(
            keep='first')]  # doppelte Einträge löschen

        self.df_actual_d = self.df_actual_d.assign(SN=self.sn_1).fillna(
            "")  # Nans durch leeren String ersetzen

        self.kd_1 = self.kd_1[~self.kd_1.index.duplicated(keep='first')]

        self.df_actual_d = self.df_actual_d.assign(Kunde=self.kd_1).fillna("")

        def get_added():
            return self.added

        def get_deleted():
            return self.deleted
		
    def checkValue(self):
        if not self.df_actual_d.empty:
            print("df_actual_d is not empty")
            self.df_SN = self.df_actual_d["SN"]
            self.df_SN_p = self.df_actual_d["SN_Parent"]
            self.df_Kd = self.df_actual_d["Kunde"]
            self.df_Kd_p = self.df_actual_d["Kunde_Parent"]
            self.use_combine()
        else:
            print("df_actual_d is empty")
            pass


# test = Combine()
# 	
# df = test.df_actual_d
# ausgeben = test.ausgeben
# zusatz = test.zusatz
# # ----  Unbedingt checkValue() ausführen, bevor use_combine ausgeführt wird ----
# test.checkValue()
# test.use_combine()

# test.checkValue()
# df_1 = test.df_actual_d


# resources = test.list_resources
