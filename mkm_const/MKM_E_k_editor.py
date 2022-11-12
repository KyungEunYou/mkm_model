# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:06:20 2018

This code can be used when new input file for k_K_calculation based on E 
for specific rxn step which show Ea<Erxn should be generated
procedure:
    1.search specific rxn step which Ea<Erxn
    2.make new input file

inputfile form should be "[OUTPUT]@@@_E_k_@@@.xlsx"

@author: kyou
"""

import os
import math
import pandas as pd
import shutil


######### variable section ####################################################
#Temp_input=[i for i in range(275,425,25)]
#Temp_input=[473.15,573.15,673.15]
Temp_input=[350]

#CM
system = "CM-13PD"
path_recipe_start_with="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\[OUTPUT]MKM-"+system+"_all_E_k_1bar_"
path_output="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"
trash_path="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\old\\"

#ZrO2
# system = "ZrO2-butane"
# path_data="F:\\MKM-pretest\\DFT-data\\"+system+"\\"
# path_recipe_start_with="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"_simpleMKM\\"+system+"-output\\[OUTPUT]MKM-"+system+"_E_k_1bar_"
# path_output="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"_simpleMKM\\"+system+"-output\\"
# trash_path="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"_simpleMKM\\"+system+"-output\\old\\"
###############################################################################

h=4.135667662e-15       #plank's constant in eVs
kb=8.6173303e-5         #bolzmann's constant in eV/K

for temp in Temp_input:
#############################variable section##################################
    path_recipe=path_recipe_start_with+str(temp)+"K.xlsx"
###############################################################################
    import_tb_recipe=pd.ExcelFile(path_recipe)
    tb1 = import_tb_recipe.parse("Sheet1",dtype={"k_for":float,"k_rev":float,"Keq":float})
    tb2=import_tb_recipe.parse("Sheet2",dtype={"species":str,"ads_sites":str,"matlab":str})
    tb3=pd.DataFrame(columns=["revised_rxn"])
    print("Temperature: "+str(temp))
    num=1
    for idx, row in tb1.iterrows():
        Ga_for=-kb*temp*math.log(h/(kb*temp)*row["k_for"])
        Ga_rev=-kb*temp*math.log(h/(kb*temp)*row["k_rev"])
        Keq=row["Keq"]
        Grxn=-kb*temp*math.log(Keq)
        if Ga_for<0:
            print(row["r_step"]+" Ga_for")
            kfor = kb*temp/h
            krev = kfor/Keq
            tb1.loc[idx,"k_for"] = kfor
            tb1.loc[idx,"k_rev"] = krev
            tb1.loc[idx,"Ga"] = 0
            revised_rxn=row["r_step"]
            tb3.loc[num]=revised_rxn
            num+=1
        if Ga_rev<0:
            print(row["r_step"]+" Ga_rev")
            krev = kb*temp/h
            kfor = krev*Keq
            tb1.loc[idx,"k_for"]=kfor
            tb1.loc[idx,"k_rev"]=krev
            tb1.loc[idx,"Ga"] = Grxn
            revised_rxn=row["r_step"]
            tb3.loc[num]=revised_rxn
            num+=1
    os.chdir(path_output)
    file_name=path_recipe_start_with.split("\\")[-1]+str(temp)+"K.xlsx"
    shutil.move(path_output+file_name,trash_path+file_name[:-5]+"-old.xlsx")
    writer=pd.ExcelWriter(path_recipe)
    tb1 = tb1.loc[:, tb1.columns[1:]]
    tb2 = tb2.loc[:, tb2.columns[1:]]
    tb1.to_excel(writer,"Sheet1")
    tb2.to_excel(writer,"Sheet2")
    tb3.to_excel(writer,"Sheet3")
    output=writer.save()


