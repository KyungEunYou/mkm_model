# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

###################### input ##################################################
system = "CM-13PD"

direc="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"
file_start="[OUTPUT]MKM-"+system+"_all_E_k_1bar_"
new_file="S3-"+system+"_rivised.xlsx"

temp_list=[350,400,450,500,550]
###############################################################################

new_tb = pd.DataFrame(columns = ["ID","Constants"] + temp_list)
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

sample_T = temp_list[0]
import_tb_sample = pd.ExcelFile(direc+file_start+str(sample_T)+"K.xlsx")
table_sample = import_tb_sample.parse("Sheet1",dtype={"r_step":str,"k_for":float,"Keq":float})

count = 0
empty_T_column = [np.zeros_like(a) for a in temp_list]
for idx1, row1 in table_sample.iterrows():
    rstep1 = row1["r_step"].translate(SUB)
    Klabel1 = "K" + rstep1[1:]
    klabel1 = "k" + rstep1[1:] + ",for"
    new_tb.loc[count] = [rstep1, Klabel1] + empty_T_column
    new_tb.loc[count+1] = ["", klabel1] + empty_T_column
    count += 2

for temp in temp_list:
    import_tb = pd.ExcelFile(direc+file_start+str(temp)+"K.xlsx")
    table = import_tb.parse("Sheet1",dtype={"r_step":str,"k_for":float,"Keq":float})
    for idx, row in table.iterrows():
        idx_num = idx
        r_step = row["r_step"].translate(SUB)
        K_label = "K" + r_step[1:]
        k_label = "k" + r_step[1:] + ",for"
        Keq = str(format(row["Keq"],".2E")).split("E")
        Keq_fac = str(int(Keq[1]))
        if Keq_fac == "0":
            Keq = Keq[0]
        else:
            Keq_fac = Keq_fac.translate(SUP)
            Keq = Keq[0]+"×10"+Keq_fac
        k_for = str(format(row["k_for"],".2E")).split("E")
        k_for_fac = str(int(k_for[1]))
        if k_for_fac == "0":
            k_for = k_for[0]
        else:
            k_for_fac = k_for_fac.translate(SUP)
            k_for = k_for[0]+"×10"+k_for_fac
        new_tb.loc[new_tb.Constants == K_label,temp] = Keq
        new_tb.loc[new_tb.Constants == k_label,temp] = k_for

writer=pd.ExcelWriter(direc+new_file)
new_tb.to_excel(writer,"Sheet1")    
writer.save() 
