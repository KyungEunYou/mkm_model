# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 11:15:53 2018

@author: kyou
"""

import pandas as pd
import math

############## input #########################################################
Pset = 1

system = "CM-12PD"
file_name="[OUTPUT]MKM-"+system+"_E_k_1bar_500K.xlsx"
path = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"

#system = "mZrO2-hexane"
#file_name="MKM-mZrO2-hexane_E_k-final2.xlsx"
#path = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"
##############################################################################

# unit = bar
P_table=pd.DataFrame(columns=["P_set","P_I000","P_h2"])
#product=0
P_table.loc[1]="Pset1", 4*1.33322E-11, 5*1.33322E-13
P_table.loc[2]="Pset2", 4*1.33322E-11, 5*1.33322E-12
P_table.loc[3]="Pset3", 4*1.33322E-11, 5*1.33322E-11  #reaction condition
P_table.loc[4]="Pset4", 4*1.33322E-11, 5*1.33322E-10
P_table.loc[5]="Pset5", 4*1.33322E-11, 5*1.33322E-9

P_table.loc[6]="Pset6", 0.008, 0.01   #high pressure
P_table.loc[7]="Pset7", 0.008, 0.1   # reactor condition in reference
P_table.loc[8]="Pset8", 0.008, 0.05
P_table.loc[9]="Pset9", 0.008, 0.005
P_table.loc[10]="Pset10", 0.008, 0.001

P_table.loc[11]="Pset11", 0.008, 0

#zro2

###highP
# P_table.loc[11]="Pset11",5e-2*0.00133322,5e-3*0.00133322
# P_table.loc[12]="Pset12",5e-2*0.00133322,5e-2*0.00133322
# P_table.loc[13]="Pset13",5e-2*0.00133322,5e-1*0.00133322
# P_table.loc[14]="Pset14",5e-2*0.00133322,5*0.00133322
# P_table.loc[15]="Pset15",5e-2*0.00133322,5e1*0.00133322


# P_table.loc[16]="Pset16",5*0.00133322,1e-4*0.00133322
# P_table.loc[17]="Pset17",5*0.00133322,1e-3*0.00133322
# P_table.loc[18]="Pset18",5*0.00133322,1e-2*0.00133322
# P_table.loc[19]="Pset19",5*0.00133322,1e-1*0.00133322
# P_table.loc[20]="Pset20",5*0.00133322,1*0.00133322

# P_table.loc[21]="Pset21",3.09e-2*0.00133322,0.1*0.00133322
# P_table.loc[22]="Pset22",3.09e-2*0.00133322,1*0.00133322
# P_table.loc[23]="Pset23",3.09e-2*0.00133322,10*0.00133322

# P_table.loc[24]="Pset24",6.80e-1*0.00133322,0.1*0.00133322
# P_table.loc[25]="Pset25",6.80e-1*0.00133322,1*0.00133322
# P_table.loc[26]="Pset26",6.80e-1*0.00133322,10*0.00133322

# P_table.loc[27]="Pset27",2.22e-4*0.00133322,1*0.00133322
# P_table.loc[28]="Pset28",3.09e-2*0.00133322,1*0.00133322
# P_table.loc[29]="Pset29",6.80e-1*0.00133322,1*0.00133322
# P_table.loc[30]="Pset30",4.91*0.00133322,1*0.00133322
# P_table.loc[31]="Pset31",1.87e1*0.00133322,1*0.00133322



#Pgly_rxn_order
#P_table.loc[1]="Pset1",math.exp(-0.5)*1e-5*0.00133322,0,0,1e-2*0.00133322
#P_table.loc[2]="Pset2",math.exp(-0.25)*1e-5*0.00133322,0,0,1e-2*0.00133322
#P_table.loc[3]="Pset3",1e-5*0.00133322,0,0,1e-2*0.00133322
#P_table.loc[4]="Pset4",math.exp(0.25)*1e-5*0.00133322,0,0,1e-2*0.00133322
#P_table.loc[5]="Pset5",math.exp(0.5)*1e-5*0.00133322,0,0,1e-2*0.00133322

#PH2_rxn_order
#P_table.loc[1]="Pset1",1e-5*0.00133322,0,0,math.exp(-0.1)*1e-2*0.00133322
#P_table.loc[2]="Pset2",1e-5*0.00133322,0,0,math.exp(-0.05)*1e-2*0.00133322
#P_table.loc[3]="Pset3",1e-5*0.00133322,0,0,1e-2*0.00133322
#P_table.loc[4]="Pset4",1e-5*0.00133322,0,0,math.exp(0.05)*1e-2*0.00133322
#P_table.loc[5]="Pset5",1e-5*0.00133322,0,0,math.exp(0.1)*1e-2*0.00133322

#P_table.loc[1]="Pset1",1e-5*0.00133322,0,0,math.exp(-0.05)*1e-2*0.00133322
#P_table.loc[2]="Pset2",1e-5*0.00133322,0,0,math.exp(-0.01)*1e-2*0.00133322
#P_table.loc[3]="Pset3",1e-5*0.00133322,0,0,1e-2*0.00133322
#P_table.loc[4]="Pset4",1e-5*0.00133322,0,0,math.exp(0.01)*1e-2*0.00133322
#P_table.loc[5]="Pset5",1e-5*0.00133322,0,0,math.exp(0.05)*1e-2*0.00133322




import_tb1=pd.ExcelFile(path+file_name)
table=import_tb1.parse("Sheet1",dtype={"r_step":str,"React_1":str,"React_2":str,"TS":str,"Prod_1":str,"Prod_2":str})

Pstrs=list()
for idx,row in table.iterrows():
    if row["React_1"].endswith("_g"):
        elem = "P_"+row["React_1"][:-2]
        if elem in P_table.columns:
            line = elem + " = " + str(P_table.loc[Pset,elem]) + " ;"
        else:
            line = elem + " = 0 ;"
        Pstrs.append(line)
    else:
        pass
        
kstrs=list()
for idx, row in table.iterrows():
    klabel_for="k"+str(idx+1)+"f"
    klabel_rev="k"+str(idx+1)+"r"
    kfor=table.loc[idx,"k_for"]
    krev=table.loc[idx,"k_rev"]
    string1=klabel_for+" = "+str(kfor)+" ;"
    string2=klabel_rev+" = "+str(krev)+" ;"
    kstrs.append(string1)
    kstrs.append(string2)

for i in kstrs:
    Pstrs.append(i)

for i in Pstrs:
    print(i)
    
    
    



