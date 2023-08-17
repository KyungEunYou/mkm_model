from mkm.utils import (
    _is_adsorption_step,
    _rxn_eqn_slicer,
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
        self._adsorption_params = adsorption
        self._bag_of_energies = bag_of_energies

        self._adsorption_theory = None
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
        self._h = 4.135667662e-15       #plank's constant in eVs
        self._kb = 8.6173303e-5         #bolzmann's constant in eV/K
    
    def __dir__(self):
        attributes = super().__dir__()
        selected_attr = [attr for attr in attributes if not attr.startswith("__") and not attr.startswith("_")]
        return selected_attr
    
    @property
    def temperature_range(self):
        return list(self.grxn.keys())
    
    @property
    def bag_of_energies(self):
        bag = {}
        bag.update({k:self._bag_of_energies['species'][k] for k in self._left_terms+self._right_terms})
        if self.is_adsorption:
            bag.update({"transition_states":None})
        else:
            bag.update({"transition_states":self._bag_of_energies['transition_states'][self.label]})
        return bag    

    @property
    def is_adsorption(self):
        return _is_adsorption_step(self.reaction_eqn)
    
    @property
    def adsorption_params(self):
        ads_theory = self.adsorption_theory
        return self._adsorption_params[ads_theory][self.label]
    
    @property
    def adsorption_theory(self):
        if _is_adsorption_step(self.reaction_eqn):
            self._adsorption_theory = list(self._adsorption_params.keys())[0]
            return self._adsorption_theory

    @property
    def erxn(self):
        if self._erxn:
            return self._erxn
        else:
            if self._bag_of_energies:
                left, right = _free_site_regulator(self._left_terms, self._right_terms)

                try:
                    self._erxn = _delta_energy(
                        self._bag_of_energies,left, right, energy_type="potential_energy")
                    return self._erxn
                except:
                    print(f"One or more species not found in bag_of_energies for {self.label}: {self.reaction_eqn}")      
    
    @erxn.setter
    def erxn(self, erxn):
        self._erxn = erxn
    
    @property
    def ea_for(self):
        if self._ea_for:
            return self._ea_for
        else:
            if self._bag_of_energies:
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
                            self._bag_of_energies, left, right, energy_type="potential_energy")
                        return self._ea_for
                    except:
                        print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}") 
            
    @ea_for.setter
    def ea_for(self, ea_for):
        self._ea_for = ea_for

    @property
    def ea_rev(self):
        if self._ea_rev:
            return self._ea_rev
        else:        
            if self._bag_of_energies:
                if not _is_adsorption_step(self.reaction_eqn):
                    right = ["ts*"]
                    left, right = _free_site_regulator(self._right_terms, right)
                    right[0] = self.label
                    try:
                        self._ea_rev = _delta_energy(
                            self._bag_of_energies, left, right, energy_type="potential_energy")
                        return self._ea_rev
                    except:
                        print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}")
    
    @property
    def grxn(self):
        if self._grxn:
            return self._grxn
        else:
            if self._bag_of_energies:
                left, right = _free_site_regulator(self._left_terms, self._right_terms)

                try:
                    self._grxn = _delta_energy(
                        self._bag_of_energies, left, right, energy_type="free_energy")
                    return self._grxn
                except:
                    print(f"One or more species not found in bag_of_energies for {self.label}: {self.reaction_eqn}")      
    
    @grxn.setter
    def grxn(self, grxn):
        self._grxn = grxn    
    
    @property
    def ga_for(self):
        if self._ga_for:
            return self._ga_for
        else:        
            if self._bag_of_energies:
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
                            self._bag_of_energies, left, right, energy_type="free_energy")
                        return self._ga_for
                    except:
                        print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}") 

    @ga_for.setter
    def ga_for(self, ga_for):
        self._ga_for = ga_for       

    @property
    def ga_rev(self):
        if self._ga_rev:
            return self._ga_rev
        else:          
            if self._bag_of_energies:
                if not _is_adsorption_step(self.reaction_eqn):
                    right = ["ts*"]
                    left, right = _free_site_regulator(self._right_terms, right)
                    right[0] = self.label
                    try:
                        self._ga_rev = _delta_energy(
                            self._bag_of_energies, left, right, energy_type="free_energy")
                        return self._ga_rev
                    except:
                        print(f"One or more species/transition state not found in bag_of_energies for {self.label}: {self.reaction_eqn}")

    @property
    def k_for(self):
        if self._k_for:
            return self._k_for
        else:     
            if self._bag_of_energies:
                t_range = self.temperature_range
                if _is_adsorption_step(self.reaction_eqn):
                    adsorption_theory = list(self._adsorption_params.keys())[0]            
                    at = AdsorptionTheories(
                        adsorption_theory, 
                        self._adsorption_params[adsorption_theory][self.label],
                        t_range,
                    )
                    self._k_for = at.calculate()                    

                else:
                    ga_for = self.ga_for
                    rate_constants = {}
                    for t in t_range:
                        rate_constants[t] = (self._kb * float(t) / self._h) * np.exp(-ga_for[t] / self._kb / float(t))
                        self._k_for = rate_constants
                return self._k_for
            else:
                raise ValueError("Plase provide params to clculated k_for in bag_of_energies or set manually")
    
    @k_for.setter
    def k_for(self, k_for):
        self._k_for = k_for    

    @property
    def k_rev(self):
        if self._k_rev:
            return self._k_rev
        else:  
            if self._bag_of_energies:
                t_range = self.temperature_range
                rate_constants = {}
                if _is_adsorption_step(self.reaction_eqn):
                    equil_const = self.equilibrium_const
                    k_for = self.k_for
                    for t in t_range:
                        rate_constants[t] = k_for[t] / equil_const[t]
                        self._k_rev = rate_constants             

                else:
                    ga_rev = self.ga_rev
                    for t in t_range:
                        rate_constants[t] = (self._kb * float(t) / self._h) * np.exp(-ga_rev[t] / self._kb / float(t))
                        self._k_rev = rate_constants
                return self._k_rev
            else:
                raise ValueError("Plase provide params to clculated k_rev in bag_of_energies or set manually")

    @k_rev.setter
    def k_rev(self, k_rev):
        self._k_rev = k_rev   

    @property
    def equilibrium_const(self):
        if self._equil_const:
            return self._equil_const
        else:       
            if self._bag_of_energies:
                grxn = self.grxn
                t_range = list(grxn.keys())
                eq_constants = {}
                for t in t_range:
                    eq_constants[t] = np.exp(- grxn[t] / self._kb / float(t))
                    self._equil_const = eq_constants
                return self._equil_const
            else:
                raise ValueError("Plase provide params to clculated equilibrium_const in bag_of_energies or set manually")
    
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
    
    json_file = f"{mkm.EXAMPLE}/bag_of_energies.json"
    with open(json_file) as f:
        bag_of_energies = json.load(f)
    
    # bag_of_energies["species"].pop("*")
    from ase.atoms import Atoms
    d = 1.1
    co = Atoms('CO', positions=[(0, 0, 0), (0, 0, d)])
    co.pbc = [True, True, True]
    print(co.pbc)

        
    ers = ElementaryReactionStep(
        "r1", 
        config.get("rxn_eqn", {}).get("r1", None),
        adsorption = config["adsorption"],
        bag_of_energies=bag_of_energies)
    print(ers.erxn)
    ers.erxn = -0.1
    print(ers.erxn)
    print