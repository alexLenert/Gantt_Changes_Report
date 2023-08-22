# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 22:53:55 2023

@author: Student
"""


class Label_sync:
    """
    Sollten zu den Taskproperties weitere hinzugekommen sein, aber eine Datei hat noch die alte Version und die andere 
    Datei schon die neue Version mit zusätzlicher Taskproperty, können die DataFrames nicht mehr verglichen werden, da 
    sie dadurch ungleiche Anzahl an Labels bekommen. Daher wird im folgenden Abschnitt die fehlende Taskproperty 
    der betreffenden Datei hizugefügt und Labels neu sortiert, so dass beide die gleiche Struckr haben. 
    """
    def use_sync(df_1, df_2):

        if len(df_1.columns) != len(df_2.columns):
            print(
                f"Erste Datei: {df_1.columns} <<<hat nicht die gleiche Labels wie die zweite Datei>>>: {df_2.columns}")
            dataframes = [df_1, df_2]

            min_index = min(enumerate(dataframes),
                            key=lambda x: x[1].shape[1])[0]

            df_min = min(enumerate(dataframes), key=lambda x: x[1].shape[1])[
                1]  # alte Version -> ein Label fehlt
            df_min_ind = min(enumerate(dataframes), key=lambda x: x[1].shape[1])[
                0]  # alte Version -> ein Label fehlt

            df_max = max(enumerate(dataframes), key=lambda x: x[1].shape[1])[
                1]  # neue Version
            df_max_ind = max(enumerate(dataframes), key=lambda x: x[1].shape[1])[
                0]  # neue Version

            # Betreffendes Label wird gespeichert (noch als Set)
            column = set(df_max.columns)-set(df_min.columns)
            # Signatur von Set auf String ändern
            column = str(column)
            for i in ["{", "}", "'", "'"]:
                column = column.replace(i, "")

            # alte Version erhält fehlendes Label von neuer Version
            df_min = df_min.assign(**{column: df_max[column]})

			# Hinzugefügte Column darf kein "true" enthalten, da es sonst beim Vergleichen wegfällt
			
            if "IGNORE" in df_min.columns:
                df_min["IGNORE"] = df_min["IGNORE"].map({"true": ""})
			
            # Zuordnen:
			
			
            if df_min_ind == 0:
                df_1 = df_min
            elif df_min_ind == 1:
                df_1 = df_max

            if df_max_ind == 0:
                df_2 = df_min
            if df_max_ind == 1:
               df_2 = df_max

            # df_1 = df_min # Columns müssen noch sortiert werden
            # df_2 = df_max # Columns müssen noch sortiert werden
            # columns sortieren - notwendig, da komplette Struktur gleich zu df_2 sein muss um vergleichen zu können
            df_1 = df_1.reindex(sorted(df_1.columns), axis=1)
            # columns sortieren - notwendig, da komplette Struktur gleich zu df_1 sein muss um vergleichen zu können
            df_2 = df_2.reindex(sorted(df_2.columns), axis=1)
			
			
			
        else:
            print("Keine unterschiedlichen Labels")
            pass
        return df_1, df_2
