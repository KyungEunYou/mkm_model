# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:06:20 2018
#### Notice1 ##################################################################
input files:
    1.recipe file
    2.gas phase info file
    3.output files of VASP calculation (refer Notice2)
#### Notice2 ##################################################################
Data strucure:
    put "catal" "int" "molecule" "TS" in same level
direcory tree and necessary files
    catal/{OUTCAR}
    int/__int_directories__(same with inter label in inputfile)/{OUTCAR}
    int/__int_directories__(same with inter label in inputfile)/freq/{freq.dat}
    molecule/{molecules.xlsx}
    TS/__TS_directories__(same with TS label)/{OUTCAR}
    TS/__TS_directories__(same with TS label)/freq/{freq.dat}
**Otherwise, modify the code regarding to the path



@author: kyou
"""

import os
from functions import allrxn_E_k #Escf, ZPE_int, ZPE_TS, qvib_int, qvib_TS,
import pandas as pd

############## Input VARIABLE SECTION ###############################################
#Temp_input=[473.15,573.15,673.15]
#Temp_input=[i for i in range(275,425,25)]
Temp_input=[350]

system = "CM-13PD"
path_data="F:\\MKM-pretest\\DFT-data\\"+system+"\\"
path_recipe="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-input\\MKM-"+system+"_all_E_k.xlsx"
path_gas_info="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-input\\MKM-"+system+"_ads_alltemp.xlsx"
path_output="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"

# system = "ZrO2-butane"
# path_data="F:\\MKM-pretest\\DFT-data\\"+system+"\\"
# path_recipe="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"_simpleMKM\\"+system+"-input\\MKM-"+system+"_E_k.xlsx"
# path_gas_info="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"_simpleMKM\\"+system+"-input\\MKM-"+system+"_ads_alltemp.xlsx"
# path_output="F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"_simpleMKM\\"+system+"-output\\"
###############################################################################

##import recipe file
import_tb1=pd.ExcelFile(path_recipe)
tb_rxn=import_tb1.parse("Sheet1",dtype={"r_step":str,"React_1":str,"React_2":str,"TS":str,"Prod_1":str,"Prod_2":str})
tb_cov=import_tb1.parse("Sheet2",dtype={"species":str,"ads_sites":str,"matlab":str})
import_tb_gas=pd.ExcelFile(path_gas_info)
tb_2=import_tb_gas.parse("Sheet1",dtype={"Pressure":float,"Temperature":float,"r_step":str,"React":str,"N0":float,"m":float,"zpe":float,"ln(qtrans)":float,"ln(qrot)":float,"ln(qvib)":float})

for temp in Temp_input:
    tb_gas=tb_2.loc[tb_2["Temperature"]==temp].set_index("React")
    allrxn_E_k(temp,path_data,tb_rxn,tb_gas)
        
    os.chdir(path_output)
    filename="[OUTPUT]"+path_recipe.split("\\")[-1][:-5]+"_1bar_"+str(temp)+"K.xlsx"
    writer=pd.ExcelWriter(filename)
    tb_rxn.to_excel(writer,"Sheet1")
    tb_cov.to_excel(writer,"Sheet2")
    writer.save()    



