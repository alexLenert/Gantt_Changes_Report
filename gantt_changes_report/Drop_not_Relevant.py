# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 02:39:38 2023

@author: Student

"""
"""
Ignorieren von nicht relevanten Daten, z.B. Projekte ON HOLD / ohne Terminierung
Sebastian hat vorgheschlagen, eine weitere Custompropery< Name= IGNORE Type= bool > in die XML-Dateien einzufügen, um damit
nichtrelevante Daten zu markieren. In diesem Fall müssen die Columns nach diesem Name abgesucht werden, und im Fall <True> gedropt werden


"""




from Combine_Parent import Combine
import pandas as pd
class Drop_not_Relevant:

    def __init__(self):
        Combining = Combine()# Objekt aus letzter Klasse
        Combining.checkValue()# Series nur auslesen, wenn DataFrame nicht leer ist ->SN,SN_Parent,Kunde,Kunde_Parent ->Objektvariablen
        self.df_x = Combining.df_actual_d # durchschleusen //
        self.df_actual_d_show = Combining.df_actual_d_show
        #self.df = self.sort_Columns(self.df_x)
        self.df = self.checkValue() # columns anpassen
        self.added = Combining.added # durchschleusen //
        self.deleted = Combining.deleted # durchschleusen //
        self.liste_resources = Combining.list_resources # durchschleusen //
        self.df_actual_d_show = self.df[self.df.index.isin(self.liste_resources)]# Nur noch Vorgänge die auch in Resources verbucht sind
        self.zusatz = Combining.zusatz # durchschleusen //
        self.ausgeben = Combining.ausgeben # durchschleusen //
        self.email = Combining.email # durchschleusen //

    #def drop_notrelevant(self, df):

    #    not_relevant_list = []
    #    not_relevant_list_index = []
    #    if "IGNORE" in self.df_x.columns:
    #        print("IGNORE in df_x")
    #        for index, row in df_x["IGNORE"].items():
    #            if row == "true":
    #                print("true gefunden")
    #                not_relevant_list.append(row)
    #                not_relevant_list_index.append(index)

        # Gesammelte, nicht relevanten Daten
    #    nichtrelevate_Daten = pd.DataFrame(
    #        not_relevant_list, not_relevant_list_index)
    #    return nichtrelevate_Daten

    #def use_drop(self):

    #    nichtrelevate_Daten_df_1 = Drop_not_Relevant.drop_notrelevant(
    #        self, self.df)

        """
        Löschen einer Row vor dem Vergleichen darf nicht den DatenPool einschränken!!
        """
        # Sollte diese Funktion zum Einsatz kommen, muss df_1_test in -> df_1 bzw. df_2_test in -> df_2 geändert werden
        # aus df_concated werden alle Rows mit den IDs aus den nichtrelevanten Daten gelöscht
    #    self.df_actual_d = self.df.drop(nichtrelevate_Daten_df_1.index)

    def sort_Columns(self, df):

        if "Verlaengerung" not in df.columns:
            print("Datentypen-Version:")
            df = df[["NR_Parent", "Vorgang", "Vorgang_Parent", "SN",
                     "Kunde", "LT", "LT_verschoben", "Verschiebung"]]

        elif "Verschiebung" not in df.columns:
            print("Datentypen-Version:")
            df = df[["NR_Parent", "Vorgang", "Vorgang_Parent", "SN",
                     "Kunde", "LT", "LT_verschoben", "Verlaengerung"]]

        elif "Verschiebung" and "Verlaengerung" in df.columns:
            print("Datentypen-Version:")
            df = df[["NR_Parent", "Vorgang", "Vorgang_Parent", "SN", "Kunde",
                     "LT", "LT_verschoben", "Verschiebung", "Verlaengerung"]]
        return df

    def checkValue(self):
        if not self.df_x.empty:
            self.df = self.sort_Columns(self.df_x)
        elif not self.df_actual_d_show.empty:
            self.df = self.df_actual_d_show
        else:
            self.df = self.df_x
        return self.df
	
# Drop = Drop_not_Relevant()
# ausgeben = Drop.ausgeben
# zusatz = Drop.zusatz
# df_x = Drop.df_x
# #Drop.use_drop()
# df = Drop.df_x

# df = Drop.df
# Drop.use_drop()
# df_actual_d = Drop.df_actual_d
# liste_resources = Drop.liste_resources

# df_actual_d_show = df[df.index.isin(Drop.liste_resources)]

# df_label_sorted = Drop.sort_Columns(df)
