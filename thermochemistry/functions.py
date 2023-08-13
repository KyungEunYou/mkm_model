from pymatgen.io.vasp.outputs import (
    Oszicar, Outcar
)
from pathlib import Path
import numpy as np
import math


class Thermochemistry:
    """
    functions to calculate thermochemistry from Vasp output files  
    """    
    def __init__(self):
        ##parameters
        self.h = 4.135667662e-15       #plank's constant in eV/s
        self.kb = 8.6173303e-5         #bolzmann's constant in eV/K
        self.c =  2.99792458e10        # speed of light in cm/s

    def energy_scf(self, file_path:str):
        file = Path(file_path).stem
        try: 
            if file == "OSZICAR":
                return Oszicar(file_path).final_energy
            elif file == "OUTCAR":
                return Outcar(file_path).final_energy
            else:
                print(f"Unsupported file: {file}")
                return None
        except FileNotFoundError:
            print(f"OSZICAR and OUTCAR do not exist.")
    
    def zero_point_correction(
            self, 
            file_path:str, 
            cutoff=50, 
            is_transition_state:bool=False
            ):
        """
        file_path: path of freq.dat file
        cutoff: 50 cm^{-1} as default
        is_transition_state: True if freq.dat is for transition state
        """
        # make list of tubples including frequencies of 3N+1 (N=relaxed atoms)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        vibfreqs = []
        for line in lines:
            vib_freq = line.split(" cm^{-1} ... ") # unit: cm^-1
            vibfreqs.append((vib_freq[0].strip(), vib_freq[1].strip()))
 
        # calculation zpe 
        # for transition state, imaginary frequency appears at the first row
        if is_transition_state:
            freq_list = vibfreqs[1:]
        else:
            freq_list = vibfreqs[:] 

        freq_sum = 0
        for i in freq_list: 
            if i[1] == "1":
                freq_sum += cutoff
            else:
                if float(i[0]) < cutoff:
                    freq_sum += cutoff
                else:
                    freq_sum += float(i[0])
 
        return 0.5 * self.h * freq_sum * self.c 

    def vibrational_partition_function(
            self,
            file_path:str,
            temperature:float,
            cutoff=50, 
            is_transition_state:bool=False
            ):
        """
        file_path: path of freq.dat file
        temperature: in unit K
        cutoff: 50 cm^{-1} as default
        is_transition_state: True if freq.dat is for transition state
        """
        # make list of tubples including frequencies of 3N+1 (N=relaxed atoms)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        vibfreqs = []
        for line in lines:
            vib_freq = line.split(" cm^{-1} ... ") # unit: cm^-1
            vibfreqs.append((vib_freq[0].strip(), vib_freq[1].strip()))   

        #calculation vibrational partition function (q)    
        if is_transition_state:
            freq_list = vibfreqs[1:]
        else:
            freq_list = vibfreqs[:] 
        
        total_qvib = 1
        for i in freq_list: 
            if i[1] == "1":
                normal_mode = cutoff
            else:
                if float(i[0]) < cutoff:
                    normal_mode = cutoff
                else:
                    normal_mode = float(i[0])
            qvib = 1/(1 - math.exp( -(self.h * normal_mode * self.c) / (self.kb * temperature)))        
            total_qvib *= qvib
        return total_qvib

    def get_potential_energy(
            self,
            energy_file:str,
            frequency_file:str,
            cutoff:float=50,
            is_transition_state:bool=False,
    ):
        """
        energy_file: path to OSZICAR or OUTCAR
        frequency_file: path to freq.dat
        cutoff: cutoff of vibrational frequency
        is_transition_state: True if freq.dat is for transition state
        """
        e = self.energy_scf(energy_file)
        zpe = self.zero_point_correction(
            frequency_file, cutoff=cutoff, is_transition_state=is_transition_state)
        return e + zpe

    def get_free_energy(
            self,
            energy_file:str,
            frequency_file:str,
            temperature:float,
            cutoff:float=50,
            is_transition_state:bool=False,
    ):
        """
        energy_file: path to OSZICAR or OUTCAR
        frequency_file: path to freq.dat
        temperature: reaction temperature
        cutoff: cutoff of vibrational frequency
        is_transition_state: True if freq.dat is for transition state
        """
        e = self.energy_scf(energy_file)
        zpe = self.zero_point_correction(
            frequency_file, cutoff=cutoff, is_transition_state=is_transition_state)
        qvib = self.vibrational_partition_function(
            frequency_file, temperature=temperature, cutoff=cutoff, 
            is_transition_state=is_transition_state)

        return e + zpe - self.kb * temperature * math.log(qvib)

