from typing import Any
from mkm.elementary_reaction_step import ElementaryReactionStep

class ReactionNetworkGenerator:
    """
    reaction_equnations: dict e.g. {"r1": "h2_g + * -> h2*, "r2": h2* + * -> h* + h*}
    bag_of_energies: dict ; format generated by mkm.bag_of_energies.BagofEnergiesGen
    """
    def __init__(
            self, 
            reaction_equations:dict=None, 
            bag_of_energies:dict=None,
            adsorption_params:dict=None,
            ):

        self.rxn_eqn = reaction_equations
        self.bag_of_energies = bag_of_energies
        self.adsorption_params = adsorption_params
        self.reaction_network = {}
        
    def __len__(self):
        return len(self.rxn_eqn)
    
    def num_ads_site(self):
        return self.ads_site
    
    def reaction_condition(self):
        return self.reaction_conditions
    
    def reactor_model(self):
        return self.reactor
    
    def convert_all(self):
        for label, rxn in self.rxn_eqn.items():
            ers = ElementaryReactionStep(
                label, 
                rxn,
                self.adsorption_params,
                self.bag_of_energies)
            
            self.reaction_network[label] = ers
        
        return  self.reaction_network

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
    
    rn = ReactionNetworkGenerator(
        config.get("rxn_eqn", {}), 
        bag_of_energies,
        config["adsorption"],
        )
    rxn_network = rn.convert_all()

    print