from thermochemistry import Thermochemistry

class BagofEnergiesGen:
    def __init__(self,species_src:str, transitionstate_src:str, temperature:list=[285]):

        # initiate bag of information
        self.bag_energy = {"species": {}, "transition_states": {}}

        # load species & transition states
        self.subdirs_interm = [x for x in species_src.iterdir() if x.is_dir()]
        self.subdirs_ts = [x for x in transitionstate_src.iterdir() if x.is_dir()]

        # temperatures to consider
        self.temperature = temperature
    
    def explorer(self):
        thermo = Thermochemistry()
        for path in self.subdirs_interm:
            
            label = path.name
            self.bag_energy["species"][label] = {"potential_energy": None, "free_energy": {}}
            
            energy_file = path.joinpath("OUTCAR")
            freq_file = path.joinpath("freq/freq.dat")
            
            pe = thermo.get_potential_energy(energy_file=energy_file, frequency_file=freq_file, cutoff=50, is_transition_state=False)
            self.bag_energy["species"][label]["potential_energy"] = pe
            
            for t in self.temperature:
                ge = thermo.get_free_energy(energy_file=energy_file, frequency_file=freq_file, temperature=t, cutoff=50, is_transition_state=False)
                self.bag_energy["species"][label]["free_energy"][t] = ge


        for path in self.subdirs_ts:
            
            label = path.name
            self.bag_energy["transition_states"][label] = {"potential_energy": None, "free_energy": {}}
            
            energy_file = path.joinpath("OUTCAR")
            freq_file = path.joinpath("freq/freq.dat")
            
            pe = thermo.get_potential_energy(energy_file=energy_file, frequency_file=freq_file, cutoff=50, is_transition_state=True)
            self.bag_energy["transition_states"][label]["potential_energy"] = pe
            
            for t in self.temperature:
                ge = thermo.get_free_energy(energy_file=energy_file, frequency_file=freq_file, temperature=t, cutoff=50, is_transition_state=True)
                self.bag_energy["transition_states"][label]["free_energy"][t] = ge
                
        return self.bag_energy    

 