# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd

############## input

#rate_step_idx=[0,1,2,3,4,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118]
#rate_step_idx=[104,106,107,108,109]
#for TOF
rate_step_idx=[2,8,6,11]
#rate_step_idx=[104,105,106,107,108,110,112]
#rate_step_idx=[109]

#CuMo2C
file_starts_with="MKM_OUTPUT_CM_13PD_350K_tpd-simple-RC_"
#file_ends_with="RC_r64_2_edit.xlsx"
path="F:\\MKM-pretest\\MKM-data\\CM-13PD\\CM-13PD-output\\CM-13PD-MATLAB\\arranged\\"
#coverage_idx=[1,2,5,7,13,35,47,49,51]
#coverage_label={1:"H",2:"O",5:"I000",7:"*",13:"I009",35:"I071",47:"supp08",49:"supp22",51:"supp25"}

#Cu111
#file_starts_with="MKM_OUTPUT_Cu111_gly_"
#path="F:\\Simulation\\MKM_package\\input_output_v6_revised\\output\\Cu111_gly\\MATLAB\\T_PH2\\"
#coverage_idx=[1,2,7,8,9,35]
#coverage_label={1:"H",2:"O",7:"*",8:"I001",9:"I002",35:"I071"}

output_file_name="MKM_OUTPUT_CM_13PD_350K_TPD_RC.xlsx"
##############################


# for reading rates
def search_idx(search_i,list_idx):
    for item in list_idx:
        if item==search_i:
            return True
        else:
            pass
    return False


os.chdir(path)
file_list=os.listdir()

new_tb=pd.DataFrame(columns=["file","r_step","rate"])
idx_count=0

for file in file_list:
    if file.startswith(file_starts_with):
#    if file.endswith(file_ends_with):
        import_tb1=pd.ExcelFile(path+file)
        table=import_tb1.parse("Rate",dtype={"rate":float,"f_rate":float,"r_rate":float})
        
        for idx,row in table.iterrows():
            if search_idx(idx,rate_step_idx)==True:
#                new_tb.loc[idx_count]=[file[23:-4],"r"+str(idx+1),row["rate"]]
                new_tb.loc[idx_count]=[file[38:-10],"r"+str(idx+1),row["rate"]]
                idx_count+=1
            else:
                pass
    else:
        pass

writer=pd.ExcelWriter(path+output_file_name)
new_tb.to_excel(writer,"Sheet1")
writer.save()
    
#for reading coverages        
#def search_idx(search_i,list_idx):
#    for item in list_idx:
#        if item==search_i:
#            return True
#        else:
#            pass
#    return False
#
#os.chdir(path)
#file_list=os.listdir()
#
#new_tb2=pd.DataFrame(columns=["file","Adsorbate","Coverage"])
#idx_count=0
#
#for file in file_list:
##    if file.startswith(file_starts_with):
#    if file.endswith(file_ends_with):        
#        import_tb2=pd.ExcelFile(path+file)
#        tb2=import_tb2.parse("coverage",dtype={"coverage":float})
#        
#        for idx,row in tb2.iterrows():
#            if search_idx(idx,coverage_idx)==True:
#                new_tb2.loc[idx_count]=[file[23:26],coverage_label[idx],row["coverage"]]
##                new_tb2.loc[idx_count]=[file[18:21],coverage_label[idx],row["coverage"]]
#                idx_count+=1
#            else:
#                pass
#    else:
#        pass    
#    
#writer=pd.ExcelWriter(path+output_file_name)
#new_tb2.to_excel(writer,"Sheet1")
#writer.save()