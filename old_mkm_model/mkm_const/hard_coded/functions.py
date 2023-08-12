# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 22:48:01 2018

@author: SEC
"""

def Escf(file):
    text=file.read()
    #find last entropy= line
    E_list={}
    iter=1
    E_loc=text.find("entropy=")        
    while E_loc != -1:
        #E_list[iter]=text[E_loc+51:E_loc+64] #CM system
        E_list[iter]=text[E_loc+50:E_loc+64] #zro2 system
        iter+=1
        E_loc=text.find("entropy=",E_loc+1)        
    E_scf=float(E_list[iter-1])
    return E_scf



def ZPE_int(file):
    #make dictionary of frequencies of 3N+1 (N=relaxed atoms)
    freq_list=[]
    freq_line=file.readline().strip()    
    while freq_line:
        temp=freq_line.split(" cm^{-1} ... ")
        freq_dic={}
        freq_dic[temp[0]]=temp[1]
        freq_list.append(freq_dic)
        freq_line=file.readline().strip()    
    #calculation zpe of intermediate strucuture
    import numpy as np
    freq_array=np.array(freq_list)
    cal_freq_array=freq_array[:] #int
    sum_freq=0   
    for item in cal_freq_array: 
        for freq_num in item.keys():
            if item[freq_num]=="1":
                sum_freq+=50
            else:
                if float(freq_num)<50:
                    sum_freq+=50
                else:
                    sum_freq+=float(freq_num)    
    ZPE_int=sum_freq*(3*(10**10))*0.5*(4.14*(10**-15))
    return ZPE_int


def ZPE_TS(file):
    #make dictionary of frequencies of 3N+1 (N=relaxed atoms)
    freq_list=[]
    freq_line=file.readline().strip()    
    while freq_line:
        temp=freq_line.split(" cm^{-1} ... ")
        freq_dic={}
        freq_dic[temp[0]]=temp[1]
        freq_list.append(freq_dic)
        freq_line=file.readline().strip()    
    #calculation zpe of TS strucuture
    import numpy as np
    freq_array=np.array(freq_list)
    cal_freq_array=freq_array[1:] #TS
    sum_freq=0    
    for item in cal_freq_array: 
        for freq_num in item.keys():
            if item[freq_num]=="1":
                sum_freq+=50
            else:
                if float(freq_num)<50:
                    sum_freq+=50
                else:
                    sum_freq+=float(freq_num)    
    ZPE_TS=sum_freq*(3*(10**10))*0.5*(4.14*(10**-15))
    return ZPE_TS



def qvib_int(file,Temp):
    #make dictionary of frequencies of 3N+1 (N=relaxed atoms)
    freq_list=[]
    freq_line=file.readline().strip()    
    while freq_line:
        temp=freq_line.split(" cm^{-1} ... ")
        freq_dic={}
        freq_dic[temp[0]]=temp[1]
        freq_list.append(freq_dic)
        freq_line=file.readline().strip()    
    #calculation vibrational partition function (q) of intermediate
    import numpy as np
    import math    
    freq_array=np.array(freq_list)
    cal_freq_array=freq_array[:] #int
    #parameters
    h=4.135667662e-15   #plank's constant in eVs
    kb=8.6173303e-5     #bolzmann's constant in eV/K
    c=3e10              #velocity of light in cm/s
    # q calculation
    Q_vib=1   
    for item in cal_freq_array: 
        for freq_num in item.keys():
            if item[freq_num]=="1":
                qvib=1/(1-math.exp(-(h*50*c)/(kb*Temp)))
                Q_vib*=qvib
            else:
                if float(freq_num)<50:
                    qvib=1/(1-math.exp(-(h*50*c)/(kb*Temp)))
                    Q_vib*=qvib
                else:
                    qvib=1/(1-math.exp(-(h*float(freq_num)*c)/(kb*Temp)))
                    Q_vib*=qvib
    return Q_vib



def qvib_TS(file,Temp):
    #make dictionary of frequencies of 3N+1 (N=relaxed atoms)
    freq_list=[]
    freq_line=file.readline().strip()    
    while freq_line:
        temp=freq_line.split(" cm^{-1} ... ")
        freq_dic={}
        freq_dic[temp[0]]=temp[1]
        freq_list.append(freq_dic)
        freq_line=file.readline().strip()    
    #calculation vibrational partition function (q) of TS
    import numpy as np
    import math    
    freq_array=np.array(freq_list)
    cal_freq_array=freq_array[1:] #TS
    #parameters
    h=4.135667662e-15     #plank's constant in eVs
    kb=8.6173303e-5       #bolzmann's constant in eV/K
    c=3e10                #velocity of light in cm/s
    # q calculation
    Q_vib=1   
    for item in cal_freq_array: 
        for freq_num in item.keys():
            if item[freq_num]=="1":
                qvib=1/(1-math.exp(-(h*50*c)/(kb*Temp)))
                Q_vib*=qvib
            else:
                if float(freq_num)<50:
                    qvib=1/(1-math.exp(-(h*50*c)/(kb*Temp)))
                    Q_vib*=qvib
                else:
                    qvib=1/(1-math.exp(-(h*float(freq_num)*c)/(kb*Temp)))
                    Q_vib*=qvib
    return Q_vib


def all_E_qvib(Temp):
    
    import os
    from functions import Escf, ZPE_int, ZPE_TS, qvib_int, qvib_TS
    import pandas as pd
    data=pd.DataFrame(columns=("Label","Escf","Escf+zpe","Q_vib"))
    title_num=1

    cwd=os.getcwd()
    os.chdir("int")
    int_dir=os.getcwd()
    for direc_int in os.listdir(int_dir):
        os.chdir(int_dir+"/"+direc_int)
        
        outcar= open("OUTCAR","r",encoding="utf-8")
        E_scf=Escf(outcar)
        outcar.close()
        
        freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
        ZPE=ZPE_int(freq_dat)
        freq_dat.close()
    
        freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
        Q_vib=qvib_int(freq_dat,Temp)
        freq_dat.close()
        
        E_ZPE=E_scf+ZPE
    
        data.loc[title_num]=direc_int,E_scf,E_ZPE,Q_vib
        title_num+=1
    
    os.chdir(cwd)
    os.chdir("TS")
    TS_dir=os.getcwd()
    for direc_TS in os.listdir(TS_dir):
        os.chdir(TS_dir+"/"+direc_TS)
        
        outcar= open("OUTCAR","r",encoding="utf-8")
        E_scf=Escf(outcar)
        outcar.close()
        
        freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
        ZPE=ZPE_TS(freq_dat)
        freq_dat.close()
    
        freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
        Q_vib=qvib_TS(freq_dat,Temp)
        freq_dat.close()
        
        E_ZPE=E_scf+ZPE
    
        data.loc[title_num]=direc_TS,E_scf,E_ZPE,Q_vib
        title_num+=1
    os.chdir(cwd)
    filename=input("Filename :")
    output=data.to_csv("./"+filename+".csv")
    return output        


## direc's patt: dir_loc
def search_dir(direc):
    import os
    for dirpath, dirnames, filenames in os.walk("."):
        for dirname in [dir_n for dir_n in dirnames if dir_n==direc]:
            dir_loc=os.path.join(dirpath, dirname)
            return dir_loc

def atom_composition(file):
    path_data=open(file,encoding="utf-8")
    lines=path_data.readlines()
    atom_list=lines[5].strip("\n").split(" ")
    while "" in atom_list:
        atom_list.remove("")
    num_list=lines[6].strip("\n").split(" ")
    while "" in num_list:
        num_list.remove("")
    composition={}
    for i in atom_list:
        index_i=atom_list.index(i)
        composition[i]=int(num_list[index_i])
    return composition

###############################################################################
###############################################################################
import os
import math
import numpy as np
from functions import Escf, ZPE_int, ZPE_TS, qvib_int, qvib_TS, atom_composition
import pandas as pd
from collections import Counter

def allrxn_E_G(temp,path_data,selected_rxn_step,ads_atom,cat_atom,reactant,tb1,tb2):
    ##functions
    def Escf_zpe_int(data_path,item):
        if item=="*":
            os.chdir(data_path+"catal")
            outcar= open("OUTCAR","r",encoding="utf-8")
            E_ZPE=Escf(outcar)
            outcar.close()
            if os.path.exists("freq") == True:
                freq_dat = open("./freq/freq.dat","r",encoding="utf-8")
                ZPE = ZPE_int(freq_dat)
                freq_dat.close()
                E_ZPE += ZPE
            else:
                pass
        else:
            os.chdir(data_path+"int\\"+item)
            outcar= open("OUTCAR","r",encoding="utf-8")
            E_scf=Escf(outcar)
            outcar.close()
            
            freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
            ZPE=ZPE_int(freq_dat)
            freq_dat.close()
            
            E_ZPE=E_scf+ZPE
        return E_ZPE
    
    def Escf_zpe_TS(data_path,item):
        os.chdir(data_path+"TS\\"+item)
        outcar= open("OUTCAR","r",encoding="utf-8")
        E_scf=Escf(outcar)
        outcar.close()
            
        freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
        ZPE=ZPE_TS(freq_dat)
        freq_dat.close()
            
        E_ZPE=E_scf+ZPE
        return E_ZPE
    
    def q_v_int(data_path,item,Temp):
        if item=="*":
            qv_int=1
        else:
            os.chdir(data_path+"int\\"+item)
            freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
            qv_int=qvib_int(freq_dat,Temp)
            freq_dat.close()
        return qv_int  
    
    def q_v_TS(data_path,item,Temp):
        os.chdir(data_path+"TS\\"+item)
        freq_dat= open("./freq/freq.dat","r",encoding="utf-8")
        qv_TS=qvib_TS(freq_dat,Temp)
        freq_dat.close()
        return qv_TS
    
    def atom_comp(data_path,state,item):
        os.chdir(data_path+state+"\\"+item)
        comp=atom_composition("CONTCAR")
        return comp
    
    def search_rxn(search_rxn,rxn_list):
        for rxn in rxn_list:
            if rxn==search_rxn:
                return True
            else:
                pass
        return False
        
    #parameters
    kb=8.6173303e-5         #bolzmann's constant in eV/K
    
    cat_atom=Counter(cat_atom)
    ads_atom=Counter(ads_atom)
    
    #dE and dG of catalyst and gas
    dE_catal=Escf_zpe_int(path_data,"*")
    dE_reactant=tb2.loc[reactant,"E"]
    dG_reactant=tb2.loc[reactant,"G"]
    dE_h2o=tb2.loc["h2o_g","E"]
    dG_h2o=tb2.loc["h2o_g","G"]
    dE_h2=tb2.loc["h2_g","E"]
    dG_h2=tb2.loc["h2_g","G"]
    
    
    for idx, row in tb1.iterrows():
        if row["React_1"].endswith("_g"):
            pass
        else:
            tb1.loc[idx,"TS"]=tb1.loc[idx,"React_1"]+"_"+tb1.loc[idx,"Prod_1"]
    for idx, row in tb1.iterrows():
        if search_rxn(row["r_step"],selected_rxn_step)==True:    
            # producted H2O and H2 count refernece form reactant        
            reac1_atom=Counter(atom_comp(path_data,"int",tb1.loc[idx,"React_1"]))
            TS_atom=Counter(atom_comp(path_data,"TS",tb1.loc[idx,"TS"]))
            prod1_atom=Counter(atom_comp(path_data,"int",tb1.loc[idx,"Prod_1"]))
            
            reac1_ads_atom=reac1_atom-cat_atom
            TS_ads_atom=TS_atom-cat_atom
            prod1_ads_atom=prod1_atom-cat_atom
            
            H2O_prod_reac1=(ads_atom-reac1_ads_atom)["O"]
            H2_prod_reac1=((ads_atom-reac1_ads_atom)["H"])/2-(ads_atom-reac1_ads_atom)["O"]
            H2O_prod_TS=(ads_atom-TS_ads_atom)["O"]
            H2_prod_TS=((ads_atom-TS_ads_atom)["H"])/2-(ads_atom-TS_ads_atom)["O"]
            H2O_prod_prod1=(ads_atom-prod1_ads_atom)["O"]
            H2_prod_prod1=((ads_atom-prod1_ads_atom)["H"])/2-(ads_atom-prod1_ads_atom)["O"]
            
            #dE
            dE_reac1=Escf_zpe_int(path_data,row["React_1"])
            dE_TS=Escf_zpe_TS(path_data,row["TS"])
            dE_prod1=Escf_zpe_int(path_data,row["Prod_1"])
            #dG
            qvb_reac1=q_v_int(path_data,row["React_1"],temp)
            dG_reac1=dE_reac1-kb*temp*math.log(qvb_reac1)
            qvb_TS=q_v_TS(path_data,row["TS"],temp)
            dG_TS=dE_TS-kb*temp*math.log(qvb_TS)
            qvb_prod1=q_v_int(path_data,row["Prod_1"],temp)
            dG_prod1=dE_prod1-kb*temp*math.log(qvb_prod1)
            
            #dE from ref(gly, cat, h20, h2)
            dE_reac1_ref=dE_reac1+H2O_prod_reac1*dE_h2o+H2_prod_reac1*dE_h2-dE_reactant-dE_catal
            dE_TS_ref=dE_TS+H2O_prod_TS*dE_h2o+H2_prod_TS*dE_h2-dE_reactant-dE_catal
            dE_prod1_ref=dE_prod1+H2O_prod_prod1*dE_h2o+H2_prod_prod1*dE_h2-dE_reactant-dE_catal
            #dG from ref(gly, cat, h20, h2)
            dG_reac1_ref=dG_reac1+H2O_prod_reac1*dG_h2o+H2_prod_reac1*dG_h2-dG_reactant-dE_catal
            dG_TS_ref=dG_TS+H2O_prod_TS*dG_h2o+H2_prod_TS*dG_h2-dG_reactant-dE_catal
            dG_prod1_ref=dG_prod1+H2O_prod_prod1*dG_h2o+H2_prod_prod1*dG_h2-dG_reactant-dE_catal
            
            #Erxn ref(h2o,h2)
            Erxn=dE_prod1_ref-dE_reac1_ref
            #Grxn ref(h2o,h2)
            Grxn=dG_prod1_ref-dG_reac1_ref
            
            #Ea ref(h2o,h2)
            Ea=dE_TS_ref-dE_reac1_ref
            #Ga ref(h2o,h2)
            Ga=dG_TS_ref-dG_reac1_ref
            
            #record values
            tb1.loc[idx,"dE_React1"]=dE_reac1_ref
            tb1.loc[idx,"dE_TS"]=dE_TS_ref
            tb1.loc[idx,"dE_Prod1"]=dE_prod1_ref
            tb1.loc[idx,"dG_React1"]=dG_reac1_ref
            tb1.loc[idx,"dG_TS"]=dG_TS_ref
            tb1.loc[idx,"dG_Prod1"]=dG_prod1_ref
            tb1.loc[idx,"ΔErxn"]=Erxn
            tb1.loc[idx,"ΔGrxn"]=Grxn
            tb1.loc[idx,"Ea"]=Ea
            tb1.loc[idx,"Ga"]=Ga
    return tb1

def allrxn_E_k(temp,path_data,tb_rxn,tb_gas):

    def Escf_zpe_int(data_path,item):
        if item == "*":
            os.chdir(data_path+"catal")
            outcar = open("OUTCAR","r",encoding="utf-8")
            E_ZPE = Escf(outcar)
            outcar.close()
            if os.path.exists("freq") == True:
                freq_dat = open("./freq/freq.dat","r",encoding="utf-8")
                ZPE = ZPE_int(freq_dat)
                freq_dat.close()
                E_ZPE += ZPE
            else:
                pass
        else:
            os.chdir(data_path+"int\\"+item)
            outcar = open("OUTCAR","r",encoding="utf-8")
            E_scf = Escf(outcar)
            outcar.close()
            
            freq_dat = open("./freq/freq.dat","r",encoding="utf-8")
            ZPE = ZPE_int(freq_dat)
            freq_dat.close()
            
            E_ZPE = E_scf+ZPE
        return E_ZPE
    
    def Escf_zpe_TS(data_path,item):
        os.chdir(data_path+"TS\\"+item)
        outcar = open("OUTCAR","r",encoding="utf-8")
        E_scf = Escf(outcar)
        outcar.close()
            
        freq_dat = open("./freq/freq.dat","r",encoding="utf-8")
        ZPE = ZPE_TS(freq_dat)
        freq_dat.close()
            
        E_ZPE = E_scf+ZPE
        return E_ZPE
    
    def Escf_gas(data_path,item):
        os.chdir(data_path+"molecule\\"+item)
        outcar = open("OUTCAR","r",encoding="utf-8")
        E_scf = Escf(outcar)
        outcar.close()
        return E_scf
    
    def q_v_TS(data_path,item,Temp):
        os.chdir(data_path+"TS\\"+item)
        freq_dat = open("./freq/freq.dat","r",encoding="utf-8")
        qv_TS = qvib_TS(freq_dat,Temp)
        freq_dat.close()
        return qv_TS
    
    def q_v_int(data_path,item,Temp):
        if item == "*":
            os.chdir(data_path+"catal\\")
            if os.path.exists("freq") == True:
                freq_dat = open("./freq/freq.dat","r",encoding="utf-8")
                qv_int = qvib_int(freq_dat,Temp)
                freq_dat.close()
            else:
                qv_int = 1
        else:
            os.chdir(data_path+"int\\"+item)
            freq_dat = open("./freq/freq.dat","r",encoding="utf-8")
            qv_int = qvib_int(freq_dat,Temp)
            freq_dat.close()
        return qv_int    
            
    ##parameters
    h = 4.135667662e-15       #plank's constant in eVs
    kb = 8.6173303e-5         #bolzmann's constant in eV/K
    kb_SI = 1.39064852e-23    #bolzmann's constant in (m^2)*(kg)*(s^-2)*(K^-1)
    conv1 = 0.010364          #1kJ=0.010364 eV
    conv2 = 1e-3              #1kg=1e-3g
    conv3 = 100000            #1bar=100000pa
    NA = 6.02e23              #Avogadro 6.02*10e23/mol 
    
    ##calculation and filling up table
    for idx, row in tb_rxn.iterrows():
        if row["React_1"].endswith("_g"):
            pass
        elif row["TS"] == "diff":
            pass
        else:
            tb_rxn.loc[idx,"TS"] = tb_rxn.loc[idx,"React_1"]+"_"+tb_rxn.loc[idx,"Prod_1"]
        
    for idx, row in tb_rxn.iterrows():
        if row["React_1"].endswith("_g"):
            pass
            ads_step = row["r_step"]
            #kads,for
            S0 = 1
            N0 = tb_gas.loc[tb_gas.r_step==ads_step,"N0"]
            ma = tb_gas.loc[tb_gas.r_step==ads_step,"m"]*conv2/NA
            kads_for = float(conv3*S0/N0/math.sqrt(2*math.pi*ma*kb_SI*temp))
            
            #Kads,eq
            Efreesite = Escf_zpe_int(path_data,"*")
            Egasads = Escf_zpe_int(path_data,row["Prod_1"])            
            Escfgas = Escf_gas(path_data,row["React_1"])
            zpe_gas = tb_gas.loc[tb_gas.r_step==ads_step,"zpe"]*conv1
            Egas = Escfgas + zpe_gas
            
            Eads = float(Egasads - Egas - Efreesite)
            
            qv_freesite = q_v_int(path_data, "*",temp)
            qv_gasads = q_v_int(path_data,row["Prod_1"],temp)
            ln_qt_gas = tb_gas.loc[tb_gas.r_step==ads_step,"ln(qtrans)"]
            ln_qr_gas = tb_gas.loc[tb_gas.r_step==ads_step,"ln(qrot)"]
            ln_qv_gas = tb_gas.loc[tb_gas.r_step==ads_step,"ln(qvib)"]
            ln_qtotgas = ln_qt_gas + ln_qr_gas + ln_qv_gas

            Gfreesite = Efreesite - kb*temp*np.log(qv_freesite)
            Ggasads = Egasads - kb*temp*np.log(qv_gasads)
            Ggas = Egas - kb*temp*ln_qtotgas
           
            Gads = float(Ggasads - Ggas - Gfreesite)
            
            Keq_ads = np.exp(- Gads/kb/temp)
    
            #kads,rev
            kads_rev = kads_for / Keq_ads
            
            # #record values
            tb_rxn.loc[idx,"Ea_for"] = ""
            tb_rxn.loc[idx,"E_rxn"] = Eads
            tb_rxn.loc[idx,"k_for"] = kads_for
            tb_rxn.loc[idx,"k_rev"] = kads_rev
            tb_rxn.loc[idx,"Keq"] = Keq_ads
            tb_rxn.loc[idx,"Ga"] = ""
            tb_rxn.loc[idx,"Grxn"] = Gads
    
        else:
            #Erxn
            reac1 = Escf_zpe_int(path_data,row["React_1"])
            reac2 = Escf_zpe_int(path_data,row["React_2"])
            free = Escf_zpe_int(path_data,"*")
            prod1 = Escf_zpe_int(path_data,row["Prod_1"])
            prod2 = Escf_zpe_int(path_data,row["Prod_2"])
            
            Erxn_for = prod1 + prod2 - reac1 - reac2
            
            #Grxn
            qv_free = q_v_int(path_data, "*",temp)
            qv_reac1 = q_v_int(path_data,row["React_1"],temp)
            qv_reac2 = q_v_int(path_data,row["React_2"],temp)
            qv_prod1 = q_v_int(path_data,row["Prod_1"],temp)
            qv_prod2 = q_v_int(path_data,row["Prod_2"],temp)
            Gfree = free - kb*temp*np.log(qv_free)          
            Greac1 = reac1 - kb*temp*np.log(qv_reac1)
            Greac2 = reac2 - kb*temp*np.log(qv_reac2)
            Gprod1 = prod1 - kb*temp*np.log(qv_prod1)
            Gprod2 = prod2 - kb*temp*np.log(qv_prod2)
            
            Grxn_for = Gprod1 + Gprod2 - Greac1 -Greac2
            
            #Ea, Ga
            if row["TS"] == "diff":
                if Erxn_for > 0:
                    Ea_for = Erxn_for
                    Ea_rev = 0
                else:
                    Ea_for = 0
                    Ea_rev = -Erxn_for
                if Grxn_for > 0:
                    Ga_for = Grxn_for
                    Ga_rev = 0
                else:
                    Ga_for = 0
                    Ga_rev = -Grxn_for                    
            else:
                TS = Escf_zpe_TS(path_data,row["TS"])

                Ea_for = TS + free - reac1 - reac2
                Ea_rev = TS + free - prod1 - prod2
                
                qv_TS = q_v_TS(path_data,row["TS"],temp)
                GTS = TS - kb*temp*np.log(qv_TS)
                
                Ga_for = GTS + Gfree - Greac1 - Greac2                
                Ga_rev = GTS + Gfree - Gprod1 - Gprod2                          

            k_for = (kb*temp/h)*math.exp(-Ga_for/kb/temp)
            k_rev = (kb*temp/h)*math.exp(-Ga_rev/kb/temp)
            K_eq_for = k_for/k_rev
            
            #record values
            tb_rxn.loc[idx,"Ea_for"] = Ea_for
            tb_rxn.loc[idx,"E_rxn"] = Erxn_for
            tb_rxn.loc[idx,"k_for"] = k_for
            tb_rxn.loc[idx,"k_rev"] = k_rev
            tb_rxn.loc[idx,"Keq"] = K_eq_for
            tb_rxn.loc[idx,"Ga"] = Ga_for
            tb_rxn.loc[idx,"Grxn"] = Grxn_for   
            
    return tb_rxn