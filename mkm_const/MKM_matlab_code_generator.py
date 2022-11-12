# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 12:01:21 2018

@author: kyou
"""
import pandas as pd
from collections import Counter

############# input #################################################
file = "MKM_CM_13PD_E_k.xlsx"
#####################################################################

def RxnDictMake(int1,int2,pd_SiteBal):
    rxns = {}
    rxns[int1] = 0
    rxns[int2] = 0
    tot_site = 0
    for i in int1,int2:
        rxns[i] += 1
        if i == "*":
            int_site = 0
        else:
            int_site = pd_SiteBal.loc[pd_SiteBal.species == i].ads_sites.item()
            tot_site += int_site
    return rxns, tot_site

def net_stoich(for_stoich,rev_stoich):
    C_rfor_stoich = Counter(for_stoich)
    C_rrev_stoich = Counter(rev_stoich)
    C_rrev_stoich.subtract(C_rfor_stoich)
    net_stoich = dict(C_rrev_stoich)
    return net_stoich

# import and read files
import_xl=pd.ExcelFile("./"+file)
pd_rxn=import_xl.parse("Sheet1",dtype={"r_step":str,"React_1":str,"React_2":str,"Prod_1":str,"Prod_2":str})
pd_cov=import_xl.parse("Sheet2",dtype={"species":str,"ads_sites":int,"matlab":str})

# read matlab variable for free sites coverage 
free_mat=str("y("+pd_cov.loc[pd_cov.species=="*"].matlab.item()+")")

eqn_list = []
stoich = {row["species"]:str(0) for idx,row in pd_cov.iterrows()}
for idx, row in pd_rxn.iterrows():
    if row["React_1"].endswith("_g"):
        for_stoich = {}
        rev_stoich = {}
        rlabel = row["r_step"]
        prod1 = row["Prod_1"]
        p = "P_" + row["React_1"][:-2]        
        kfor = rlabel.replace("r","k")+"f"
        krev = rlabel.replace("r","k")+"r"
        
        free_num = pd_cov.loc[pd_cov.species==prod1].ads_sites.item()
        free_term = "power(" + free_mat + "," + str(free_num) + ")"
        ads_term = "y(" + pd_cov.loc[pd_cov.species==prod1].matlab.item() + ")"
        
        rfor_eqn = rlabel+"f=" + kfor + "*" + p + "*" + free_term + " ;"
        rrev_eqn = rlabel+"r=" + krev + "*" + ads_term + " ;"
        eqn_list.append(rfor_eqn)
        eqn_list.append(rrev_eqn)
        for_stoich["*"] = free_num
        rev_stoich[prod1] = 1
        elem_stoich = net_stoich(for_stoich,rev_stoich)
        for nk, nm in elem_stoich.items():
            stoich[nk] += "+"+str(nm)+"*"+rlabel
        
    else:
        rlabel = row["r_step"]
        react1 = row["React_1"]
        react2 = row["React_2"]
        prod1 = row["Prod_1"]
        prod2 = row["Prod_2"]
        kfor = row["r_step"].replace("r","k")+"f"
        krev = row["r_step"].replace("r","k")+"r"
        
        react_rxns, react_sites = RxnDictMake(react1,react2,pd_cov)
        prod_rxns, prod_sites = RxnDictMake(prod1,prod2,pd_cov)        
        free_sites = prod_sites - react_sites
        if free_sites > 0:
            prod_rxns.pop("*",None)
            react_rxns["*"] = abs(free_sites)
        elif free_sites < 0:
            react_rxns.pop("*",None)
            prod_rxns["*"] = abs(free_sites)
        else:
            react_rxns.pop("*",None)
            prod_rxns.pop("*",None)
        rfor_eqn = rlabel+"f=" + kfor
        for k,v in react_rxns.items():
            mat_term = "y(" + pd_cov.loc[pd_cov.species==k].matlab.item() + ")"
            add_st = "*power(" + mat_term + "," + str(v) + ")"
            rfor_eqn += add_st
        rfor_eqn += " ;"
        rrev_eqn = rlabel+"r=" + krev
        for k,v in prod_rxns.items():
            mat_term = "y(" + pd_cov.loc[pd_cov.species==k].matlab.item() + ")"
            add_st = "*power(" + mat_term + "," + str(v) + ")"
            rrev_eqn += add_st  
        rrev_eqn += " ;" 
        eqn_list.append(rfor_eqn)
        eqn_list.append(rrev_eqn)
        
        elem_stoich = net_stoich(react_rxns,prod_rxns)
        for nk, nm in elem_stoich.items():
            if nm < 0:
                stoich[nk] += str(nm)+"*"+rlabel
            else:
                stoich[nk] += "+"+str(nm)+"*"+rlabel
               
for idx, row in pd_rxn.iterrows():
    rlabel=str(pd_rxn.loc[idx,"r_step"])
    rxn_eqn=rlabel+"="+rlabel+"f-"+rlabel+"r ;"
    eqn_list.append(rxn_eqn)

for key,value in stoich.items(): 

    if value.startswith("0+"):
        value = value[2:]
    elif value.startswith("0-"):
        value = value[1:]
    else:
        pass
    value += " ;"
    stoich[key] = value

y_num = str(len(stoich))

print("M = zeros("+y_num+","+y_num+") ;")
print("M("+y_num+","+y_num+") = 1 ;")
print("optode = odeset('NonNegative',1:"+y_num+",'Abstol',1E-15,'RelTol',1E-15) ;")
y0_list = ["x/"+str(row["ads_sites"]) if row["species"]!="*" else "1-"+str(int(y_num)-1)+"*x" for idx,row in pd_cov.iterrows()]
y0_st = "y0 = ["
for item in y0_list:
    item = item + ","
    y0_st += item
y0_st = y0_st[:-1]+"] ;"
print(y0_st)
plot_list = [",t, y(:,"+str(i)+"),'r'" for i in range(2,int(y_num)+1)]
plot_spec = "loglog(t, y(:,1),'b'"
for i in plot_list:
    plot_spec += i
print(plot_spec+") ;")
plot_legend = "l = legend('y1'"
for i in range(2,int(y_num)+1):
    plot_legend += ",'y"+str(i)+"'"
print(plot_legend+") ;")
sb_list = []
for i in range(1,int(y_num)+1):
    sb = pd_cov.loc[pd_cov.matlab==str(i)].ads_sites.item()
    sb_list.append(sb)
print("y_site_balance = y.* "+str(sb_list)+" ;")

# for i in eqn_list:
#     print(i)

# print("F = [ ;")    
# for i in range(1,int(y_num)+1):
#     species = pd_cov.loc[pd_cov.matlab==str(i)].species.item()
#     res = stoich[species]    
#     print(res)
# print("] ;")

# rxn_num = len(pd_rxn.r_step)
# r_1st = "r = ["
# for_1st = "for_r = ["
# rev_1st = "rev_r = ["
# for i in range(1,rxn_num+1):
#     r_elem = " r"+str(i)
#     for_elem = " r"+str(i)+"f"
#     rev_elem = " r"+str(i)+"r"
#     r_1st += r_elem
#     for_1st += for_elem
#     rev_1st += rev_elem
# print(r_1st+"] ;") 
# print(for_1st+"] ;") 
# print(rev_1st+"] ;")     