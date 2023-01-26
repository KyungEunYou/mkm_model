# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:27:07 2020

@author: SEC
"""
import os
import pandas as pd
import numpy as np

############## input #########################################################
system = "mZrO2-hexane"
#system = "CM-12PD"
file_name_startswith = "MKM_"
#ref_file = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-input\\MKM-"+system+"_E_k.xlsx"
#path = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"+system+"-MATLAB\\"
#save_path = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\"+system+"-MATLAB\\arranged\\"
ref_file = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\MKM-"+system+"_E_k-final2.xlsx"
path = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\MATLAB-zro2-hexane\\"
save_path = "F:\\MKM-pretest\\MKM-data\\"+system+"\\"+system+"-output\\MATLAB-zro2-hexane\\arranged\\"

##############################################################################

ref_pd1 = pd.ExcelFile(ref_file).parse("Sheet1")
ref_pd1 = ref_pd1.loc[:, ref_pd1.columns[:6]]
ref_pd2 = pd.ExcelFile(ref_file).parse("Sheet2")
ref_pd2 = ref_pd2.loc[:, ref_pd2.columns[:3]]
file_list = os.listdir(path)
for f in file_list:
    if f.startswith(file_name_startswith):
        import_pd = pd.ExcelFile(path+f)
        pd1 = import_pd.parse("rate")
        pd2 = import_pd.parse("coverage")
        if f[:-5]+"_edit.xlsx" in os.listdir(save_path):
            pass
        else:
            pd1_num = 0
            for column in ref_pd1.columns:
                pd1.insert(pd1_num,column,ref_pd1[column])
                pd1_num += 1
            pd2_num = 0
            for column in ref_pd2.columns:
                pd2.insert(pd2_num,column,ref_pd2[column])
                pd2_num += 1
            pd1 = pd1.replace(np.nan, '', regex=True)
            newlist = []
            for idx,row in pd2.iterrows():
                new_elem = int(row["ads_sites"])*float(row["coverage"])
                newlist.append(new_elem)
            pd2["net_cov"] = newlist
            pd2.assign(newlist = newlist)
            pd2 = pd2.replace(np.nan, '', regex=True)
            pd3 = pd.DataFrame(data = {"File_name": [f]})
            
            new_f = save_path+f[:-5]+"_edit.xlsx"
            writer = pd.ExcelWriter(new_f)
            pd1.to_excel(writer,"Rate")
            pd2.to_excel(writer,"Coverage")
            pd3.to_excel(writer,"File_name")
            writer.save()