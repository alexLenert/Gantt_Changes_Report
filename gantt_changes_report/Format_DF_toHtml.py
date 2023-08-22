# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 03:02:55 2023

@author: Student
"""
import numpy as np

class Format_to_html:
    
   
    
    def Format_html(df):
        


        def highlight_value(x, value, color):
            print("--Highlighting wird durchgeführt--")
            return np.where(x == value, f"background-color: {color};", None)
    
    
        def highlight_Kunde(x, value, color):
            return np.where(x == value, f"background-color: {color};", None)
    
    
        if "LT_verschoben" in df:
            print("IF-Zweig")
            """
            df.style.apply ist depricated, habe aber keinen Ersatz dafür gefunden
            """
            styled_df = df.style.hide()
    
            styled_df = styled_df.apply(
                highlight_value, value=True, color='red', subset=['LT_verschoben'])
    
            styled_df = styled_df.apply(
                highlight_value, value='late', color='yellow', subset=['LT_verschoben'])
    
            styled_df = styled_df.apply(
                highlight_value, value='early', color='green', subset=['LT_verschoben']).render()
    
    
        elif df.empty:
            print("elif-Zweig")
            styled_df = "DataFrame ist leer"  # Da k
    
        else:
            styled_df = df.style.apply(highlight_value, value=str, color='green', subset=[
                                       ('parent', "self")]).render()
            print("else-Zweig")
        return styled_df