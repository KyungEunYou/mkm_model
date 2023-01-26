# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:53:39 2019

for RC, ads rxn does not need to be considered. (not included in RC test)

@author: kyou
"""
import math
import pandas as pd

######## Input rxn list here###################################################
system = "CM-13PD"

path_recipe_dir="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"
path_output="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\RC\\"
file_starts_with="[OUTPUT]MKM-"+system+"_E_k_1bar_"
#  file_starts_with should be whole phrase just before temperature
#  file name should be 'file_starts_with_'400K.xlsx

#path_recipe_dir="F:\\Simulation\\MKM_package\\input_output_v4\\output\\Cu111_gly\\"
#path_output="F:\\Simulation\\MKM_package\\input_output_v4\\output\\Cu111_gly\\RC\\"
#file_starts_with="[OUTPUT]MKM_Cu111_gly_E_k_1bar_"
#  file_starts_with should be whole phrase just before temperature
#  file name should be 'file_starts_with_'400K.xlsx

#Temp_input=[i for i in range(275,575,25)]
Temp_input=[350]
rxn_list=["r1","r3","r7","r9","r15","r17","r19","r42","r47","r48","r68","r78"]
#rxn_list=["r1","r2","r3","r7","r9","r15","r17","r18","r19","r20","r22","r30","r42","r44","r47","r48","r68","r78"]

###############################################################################

#parameters
kb=8.6173303e-5         #bolzmann's constant in eV/K
h=4.135667662e-15       #plank's constant in eVs


def two_table_generator_RC(tb1,tb2,rxn,temp):
    mul_plus=math.exp(-0.01/kb/temp)
    mul_minus=math.exp(0.01/kb/temp)    
    for idx,row in tb1.iterrows():
        if row["r_step"]==rxn:
            k_for_real=row["k_for"]
            k_rev_real=row["k_rev"]
            k_for=k_for_real*mul_plus
            k_rev=k_rev_real*mul_plus
            tb1.loc[tb1.r_step==rxn,"Ea_for"]=""
            tb1.loc[tb1.r_step==rxn,"k_for"]=k_for
            tb1.loc[tb1.r_step==rxn,"k_rev"]=k_rev
        else:
            pass
       
    for idx,row in tb2.iterrows():
        if row["r_step"]==rxn:
            k_for_real=row["k_for"]
            k_rev_real=row["k_rev"]
            k_for=k_for_real*mul_minus
            k_rev=k_rev_real*mul_minus
            tb2.loc[tb2.r_step==rxn,"Ea_for"]=""
            tb2.loc[tb2.r_step==rxn,"k_for"]=k_for
            tb2.loc[tb2.r_step==rxn,"k_rev"]=k_rev
        else:
            pass      
    return tb1,tb2    

for temp in Temp_input:
    import_tb_recipe=pd.ExcelFile(path_recipe_dir+file_starts_with+str(temp)+"K.xlsx")
    table_cov=import_tb_recipe.parse("Sheet2",dtype={"species":str,"ads_sites":str,"matlab":str})
    for item in rxn_list:
        tb1=import_tb_recipe.parse("Sheet1",dtype={"k_for":float,"k_rev":float}).copy()
        tb2=import_tb_recipe.parse("Sheet1",dtype={"k_for":float,"k_rev":float}).copy()
        two_table_generator_RC(tb1,tb2,item,temp)
        generated_file1=path_output+file_starts_with+str(temp)+"K_"+item+"_1.xlsx"
        generated_file2=path_output+file_starts_with+str(temp)+"K_"+item+"_2.xlsx"
        writer1=pd.ExcelWriter(generated_file1)
        writer2=pd.ExcelWriter(generated_file2)
        tb1.to_excel(writer1,"Sheet1")
        tb2.to_excel(writer2,"Sheet1")
        table_cov.to_excel(writer1,"Sheet2")
        table_cov.to_excel(writer2,"Sheet2")
        writer1.save()
        writer2.save()

            