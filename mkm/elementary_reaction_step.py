from mkm.utils import (
    _rxn_eqn_slicer,
    _is_adsorption_step,
    _free_site_regulator,
    _delta_energy,
)
from mkm.adsorption import AdsorptionTheories
import numpy as np

class ElementaryReactionStep:
    def __init__(self, label:str=None, reaction_eqn:str=None, 
                 adsorption:dict=None, bag_of_energies:dict=None):
        self.label = label
        self.reaction_eqn = reaction_eqn
        if self.reaction_eqn is not None:
            self._left_terms, self._right_terms = _rxn_eqn_slicer(reaction_eqn)
        self.adsorption = adsorption
        self.bag_of_energies = bag_of_energies
        self._erxn = None
        self._ea_for = None
        self._ea_rev = None
        self._grxn = None
        self._ga_for = None
        self._ga_rev = None
        self._k_for = None
        self._k_rev = None
        self._equil_const = None

        # parameteres
        self.h = 4.135667662e-15       #plank's constant in eVs
        self.kb = 8.6173303e-5         #bolzmann's constant in eV/K

    @property
    def erxn(self):
        if self.bag_of_energies:
            left, right = _free_site_regulator(self._left_terms, self._right_terms)

            try:
                self._erxn = _delta_energy(
                    self.bag_of_energies,left, right, energy_type="potential_energy")
            except:
                print(f"One or more species not found in bag_of_energies for {self.label}: {self.reaction_eqn}")      
        return self._erxn
    
    @erxn.setter
    def erxn(self, erxn):
        self._erxn = erxn
    
    @property
    def ea_for(self):
        if self.bag_of_energies:
            # activation energy is for elementary surface reaction
            # the rate constant of adsorption step is calculated by collision theory without activation energy
            if not _is_adsorption_step(self.reaction_eqn):
                # arbitrary set transition state list. it is because ts is commonly described by one state in elementary reaction.
                # There is room to be upgraded to general circumstances.
                right = ["ts*"]
                left, right = _free_site_regulator(self._left_terms, right)
                right[0] = self.label
                try:
                    self._ea_for = _delta_energy(
                        self.bag_of_energies, left, right, energy_type="potential_energy")
                except:
                    print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}") 
        
        return self._ea_for
    
    @ea_for.setter
    def ea_for(self, ea_for):
        self._ea_for = ea_for

    @property
    def ea_rev(self):
        if self.bag_of_energies:
            if not _is_adsorption_step(self.reaction_eqn):
                right = ["ts*"]
                left, right = _free_site_regulator(self._right_terms, right)
                right[0] = self.label
                try:
                    self._ea_rev = _delta_energy(
                        self.bag_of_energies, left, right, energy_type="potential_energy")
                except:
                    print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}")

        return self._ea_rev
    
    @property
    def grxn(self):
        if self.bag_of_energies:
            left, right = _free_site_regulator(self._left_terms, self._right_terms)

            try:
                self._grxn = _delta_energy(
                    self.bag_of_energies, left, right, energy_type="free_energy")
            except:
                print(f"One or more species not found in bag_of_energies for {self.label}: {self.reaction_eqn}")      
        return self._grxn
    
    @grxn.setter
    def grxn(self, grxn):
        self._grxn = grxn    
    
    @property
    def ga_for(self):
        if self.bag_of_energies:
            # activation energy is for elementary surface reaction
            # the rate constant of adsorption step is calculated by collision theory without activation energy
            if not _is_adsorption_step(self.reaction_eqn):
                # arbitrary set transition state list. it is because ts is commonly described by one state in elementary reaction.
                # There is room to be upgraded to general circumstances.
                right = ["ts*"]
                left, right = _free_site_regulator(self._left_terms, right)
                right[0] = self.label
                try:
                    self._ga_for = _delta_energy(
                        self.bag_of_energies, left, right, energy_type="free_energy")
                except:
                    print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}") 
        
        return self._ga_for  

    @ga_for.setter
    def ga_for(self, ga_for):
        self._ga_for = ga_for       

    @property
    def ga_rev(self):
        if self.bag_of_energies:
            if not _is_adsorption_step(self.reaction_eqn):
                right = ["ts*"]
                left, right = _free_site_regulator(self._right_terms, right)
                right[0] = self.label
                try:
                    self._ga_rev = _delta_energy(
                        self.bag_of_energies, left, right, energy_type="free_energy")
                except:
                    print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}")

        return self._ga_rev

    @property
    def k_for(self):
        if self.bag_of_energies:
            t_range = list(self.grxn.keys())
            if _is_adsorption_step(self.reaction_eqn):
                adsorption_theory = list(self.adsorption.keys())[0]            
                at = AdsorptionTheories(
                    adsorption_theory, 
                    self.adsorption[adsorption_theory][self.label],
                    t_range,
                )
                self._k_for = at.calculate()                    

            else:
                ga_for = self.ga_for
                for t in t_range:
                    self._k_for = (self.kb * float(t) / self.h) * np.exp(-ga_for[t] / self.kb / float(t))
        return self._k_for
    
    @k_for.setter
    def k_for(self, k_for):
        self._k_for = k_for    

    @property
    def k_rev(self):
        if self.bag_of_energies:
            t_range = list(self.grxn.keys())
            if _is_adsorption_step(self.reaction_eqn):
                equil_const = self.equilibrium_const
                k_for = self.k_for
                for t in t_range:
                    self._k_rev = k_for[t] / equil_const                  

            else:
                ga_rev = self.ga_rev
                for t in t_range:
                    self._k_rev = (self.kb * float(t) / self.h) * np.exp(-ga_rev[t] / self.kb / float(t))
        return self._k_rev

    @k_rev.setter
    def k_rev(self, k_rev):
        self._k_rev = k_rev   

    @property
    def equilibrium_const(self):
        if self.bag_of_energies:
            grxn = self.grxn
            t_range = list(grxn.keys())
            for t in t_range:
                self._equil_const = np.exp(- grxn[t] / self.kb / float(t))
        return self._equil_const
    
    @equilibrium_const.setter
    def equilibrium_const(self, equil_const):
        self._equil_const = equil_const

if __name__=="__main__":
    import mkm
    import yaml
    import json

    yaml_file = f"{mkm.EXAMPLE}/config.yml"
    with open(yaml_file) as f:
        config = yaml.safe_load(f)
    
    json_file = f"{mkm.EXAMPLE}/info_bag.json"
    with open(json_file) as f:
        bag_of_energies = json.load(f)
    
    # bag_of_energies["species"].pop("*")
        
    ers = ElementaryReactionStep(
        "r1", 
        config.get("rxn_eqn", {}).get("r1", None),
        adsorption = config["adsorption"],
        bag_of_energies=bag_of_energies)
    # ers = ElementaryReactionStep()
    # ers.erxn = -0.1
    print(ers.k_for)
    print