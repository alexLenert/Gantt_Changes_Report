# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 23:21:53 2023

@author: Student
"""

"""
Die Klasse makeParData wurde entwickelt, um die Inhalte aus den parents (Übergeodnete Vorgänge) auszulesen und den Untervorgängen als Series 
hinzuzufügen. 
parNames wird für die Vorgänge aus comp genutzt. parNamesAdd wird 
"""
import pandas as pd

from Strategy_Pattern import Comparsion

class makeParData ():
    
    def __init__(self):
        comp = Comparsion()
        comp.switch(comp.Ausgabe)
        self.Ausgabe = comp.Ausgabe
        self.Ergebnis = comp.ergebnis
        self.df_actual_d_show = comp.df_actual_d_show
        self.df_actual_d = comp.df_actual_d
        self.verschieben = comp.verschieben
        self.verlaengern = comp.verlaengern
        self.df_start_self = comp.df_start_self
        self.df_start_other = comp.df_start_other
        self.df_duration_self = comp.df_duration_self
        self.df_duration_other = comp.df_duration_other
        self.zusatz = comp.zusatz
        self.list_resources = comp.list_resources
        self.ausgeben = comp.ausgeben
        self.email = comp.email
   
    #Einfügen von Parent-Values aus den Columns Name, SN und Nr.
    def parNames(self, series, df, string):
 
        par_nam=df[string].loc[series] #Wählt alle Namen der tasks mit den festgelegten IDs
        
        
        nam_val_list = list(par_nam.values)# Liste aus den Values von par_nam
    
        par_ind_list = list(series.index) # Liste aus dem Index von par_index
        val_parent  = pd.Series(nam_val_list,par_ind_list)
           
        return val_parent
	#Einfügen von Parent-Values
    def parNamesAdd(self, series, df, string):
        
        seriesOrg = series
        seriesD = series.dropna()
        
        par_nam1=df[string].loc[seriesD] #Wählt alle Namen der tasks mit den festgelegten IDs
        par_nam = par_nam1[~par_nam1.index.duplicated(keep='first')] # löscht doppelte IDs
        
        nam_val_list = list(par_nam.values)# Liste aus den Values von par_nam
        par_ind_list = list(series.index) # Liste aus dem Index von par_index
        if(len(nam_val_list) != len(par_ind_list)): # Wenn gleiche Parent-IDs in unterschiedlichen IDs gefunden werden           
        		test_namen = par_nam.loc[seriesD]
        		nam_val_list = list(test_namen.values)
        		print("---Mehrere gleiche Parents!---")
        val_parent  = pd.Series(nam_val_list,par_ind_list, dtype = object)
           
        return val_parent
    
    def parNamesDel(self, series, df, string):
        
        seriesOrg = series
        seriesD = series.dropna()
        
        par_nam1=df[string].loc[seriesD] #Wählt alle Namen der tasks mit den festgelegten IDs
        par_nam = par_nam1[~par_nam1.index.duplicated(keep='first')] # löscht doppelte IDs
        
        nam_val_list = list(par_nam.values)# Liste aus den Values von par_nam
        par_ind_list = list(series.index) # Liste aus dem Index von par_index
        if(len(nam_val_list) != len(par_ind_list)):            
        		test_namen = par_nam.loc[seriesD]
        		nam_val_list = list(test_namen.values)
        		print("---Mehrere gleiche Parents!---")
        val_parent  = pd.Series(nam_val_list,par_ind_list, dtype = object)
           
        return val_parent
    
    def einfuegen(self, Series, DataFrame, String, df_x):# assign kann nur mit orginal-String betitelt werden, daher wird diese Methode nicht benutzt
        
        parentX = makeParData.parNamesAdd(Series, DataFrame, String)
        einsetzen = str(String.capitalize()) + "_Parent"
        df_x = df_x.assign(einsetzen = parentX) # setzt die Gerätenamen der Übergeordneten Tags in einer neuen Series ein
        return df_x
    
    
    
    def parents_in_df_actual_d_eingeben(self):
        self.ind_par = self.Ergebnis["OLD"]["parent"].dropna() # Datensatz aus mycompare()
        self.old3 = self.Ergebnis["OLD"]
        
    #========================Name=================
        
        name_parent = makeParData.parNames(self, self.ind_par, self.old3, "name")
        
        self.df_actual_d = self.df_actual_d.assign(Vorgang_Parent = name_parent) # setzt die Gerätenamen der Übergeordneten Tags in einer neuen Series ein
    
    #========================SN=================
    
        sn_parent = makeParData.parNames(self, self.ind_par, self.old3, "SN")
        
        self.df_actual_d = self.df_actual_d.assign(SN_Parent = sn_parent)
    
    #===============================NR==============
    
        nr_parent = makeParData.parNames(self, self.ind_par, self.old3, "Nr.")
        
        self.df_actual_d = self.df_actual_d.assign(NR_Parent = nr_parent)
    #================================Kunde============
    
        kunde_parent = makeParData.parNames(self, self.ind_par, self.old3, "Kunde")
        
        self.df_actual_d = self.df_actual_d.assign(Kunde_Parent = kunde_parent)
        self.df_actual_d = self.df_actual_d.fillna("")
        
        
    #===============================LT===================
    
        lt_parent = makeParData.parNames(self, self.ind_par, self.old3, "LT")
        
        lt_parent = pd.to_datetime(lt_parent)
        lt_parent = lt_parent.dt.date
        
        self.df_actual_d = self.df_actual_d.assign(LT_Parent = lt_parent)
    
        
        self.df_actual_d["Vorgang_Parent"] = self.df_actual_d["Vorgang_Parent"].fillna(" ") 
        
        self.df_actual_d["SN_Parent"] = self.df_actual_d["SN_Parent"].fillna(" ")
        
        self.df_actual_d["NR_Parent"] = self.df_actual_d["NR_Parent"].fillna(" ")
    
        self.df_actual_d["Kunde_Parent"] = self.df_actual_d["Kunde_Parent"].fillna(" ")
        
        self.df_actual_d["LT_Parent"] = self.df_actual_d["LT_Parent"].fillna(" ")
        
    def parents_in_added_eingeben(self):
        # added parent-Werte einfügen
        self.ind_par_add = self.Ergebnis["added"]["parent"].dropna() # Datensatz aus mycompare()
        self.old3 = pd.concat([self.Ergebnis["added"],self.Ergebnis["new"]])
    
        
        
    #========================Name=================
        
        name_parent_add = makeParData.parNamesAdd(self, self.ind_par_add,self. old3, "name")
        
        self.Ergebnis["added"] = self.Ergebnis["added"].assign(Vorgang_Parent = name_parent_add) # setzt die Gerätenamen der Übergeordneten Tags in einer neuen Series ein
    
    #========================SN=================
    
        sn_parent_add = makeParData.parNamesAdd(self, self.ind_par_add, self.old3, "SN")
        
        self.Ergebnis["added"] = self.Ergebnis["added"].assign(SN_Parent = sn_parent_add)
    
    #===============================NR==============
    
        nr_parent_add = makeParData.parNamesAdd(self, self.ind_par_add, self.old3, "Nr.")
        
        self.Ergebnis["added"] = self.Ergebnis["added"].assign(NR_Parent = nr_parent_add)
        
    #=============================Kunde============
    
        kunde_parent_add = makeParData.parNamesAdd(self, self.ind_par_add, self.old3, "Kunde")
        
        self.Ergebnis["added"] = self.Ergebnis["added"].assign(Kunde_Parent = kunde_parent_add)
        
        self.Ergebnis["added"] = self.Ergebnis["added"].rename(columns={"name": "Vorgang"})
        self.Ergebnis["added"] = self.Ergebnis["added"][["Kunde","SN","LT","Vorgang", "Vorgang_Parent", "SN_Parent", "NR_Parent", "Kunde_Parent"]]
        self.Ergebnis["added"] = self.Ergebnis["added"].fillna("")
        
    def parents_in_deleted_eingeben(self):
        self.ind_par_del = self.Ergebnis["deleted"]["parent"].dropna() # Datensatz aus mycompare()
        self.old3 = pd.concat([self.Ergebnis["old"],self.Ergebnis["new"]])

    #========================Name=================
        
        name_parent_del = makeParData.parNamesDel(self, self.ind_par_del, self.old3, "name")
        
        self.Ergebnis["deleted"] = self.Ergebnis["deleted"].assign(Vorgang_Parent = name_parent_del) # setzt die Gerätenamen der Übergeordneten Tags in einer neuen Series ein

    #========================SN=================

        sn_parent_del = makeParData.parNamesDel(self, self.ind_par_del, self.old3, "SN")
        
        self.Ergebnis["deleted"] = self.Ergebnis["deleted"].assign(SN_Parent = sn_parent_del)

    #===============================NR==============

        nr_parent_del = makeParData.parNamesDel(self, self.ind_par_del, self.old3, "Nr.")
        
        self.Ergebnis["deleted"] = self.Ergebnis["deleted"].assign(NR_Parent = nr_parent_del)
        
    #=============================Kunde============

        kunde_parent_del = makeParData.parNamesDel(self, self.ind_par_del, self.old3, "Kunde")
        
        self.Ergebnis["deleted"] = self.Ergebnis["deleted"].assign(Kunde_Parent = kunde_parent_del)
        self.Ergebnis["deleted"] = self.Ergebnis["deleted"].rename(columns={"name": "Vorgang"})
        
        self.Ergebnis["deleted"] = self.Ergebnis["deleted"][["Kunde","SN","LT", "Vorgang", "Vorgang_Parent", "SN_Parent", "NR_Parent", "Kunde_Parent"]]
        self.Ergebnis["deleted"] = self.Ergebnis["deleted"].fillna("")
    
    
    def checkValue(self):
        df_actual_d = self.df_actual_d 
        if not pd.DataFrame(df_actual_d).empty:
            self.parents_in_df_actual_d_eingeben()
            if ('IGNORE', 'self') and ('IGNORE', 'other') in self.df_actual_d:
                self.df_actual_d[('IGNORE', 'self')] = self.df_actual_d[('IGNORE', 'self')].fillna("") 
                self.df_actual_d[('IGNORE', 'other')] = self.df_actual_d[('IGNORE', 'other')].fillna("")
                print("IGNORE!!")
                if pd.Series(self.df_actual_d[('IGNORE', 'self')].str.len()==0).all():
                    print("self")
                    self.df_actual_d['IGNORE'] = self.df_actual_d[('IGNORE', 'other')]
                elif pd.Series(self.df_actual_d[('IGNORE', 'other')].str.len()==0).all():
                    print("other")
                    self.df_actual_d['IGNORE'] = self.df_actual_d[('IGNORE', 'self')]
            
        #else:
		#    self.df_actual_d = pd.DataFrame(columns = ["SN", "Kunde","SN_Parent","Kunde_Parent"])
			
	
#Data = makeParData()

#ausgeben = Data.ausgeben
#zusatz = Data.zusatz

#df_actual_d = Data.df_actual_d
#df_actual_d_show = Data.df_actual_d_show
#Data.checkValue()
#Data.parents_in_df_actual_d_eingeben()
#Data.parents_in_added_eingeben()
#Data.parents_in_deleted_eingeben()

#df_actual_d_1 = Data.df_actual_d
#df_actual_d_show_1 = Data.df_actual_d_show
#added = Data.Ausgabe[9]
#deleted = Data.Ausgabe[10]
#Ergebnis = Data.Ergebnis



