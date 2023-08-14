from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from mkm.utils import (
    _rxn_eqn_slicer,
    _free_site_regulator_for_mkm,
    _multipliers,
)

class MKM:
    """
    config: dict, example of yaml file is in example directory
    reaction_network: dict e.g. {"r1": ElementaryReactionStep, "r2": ElementaryReactionStep}
    """
    def __init__(self, config:dict, reaction_network:dict):
        self.rxn_eqn = config.get("rxn_eqn", {})
        self.ads_site = config.get("int_ads_site", {})
        self.pressures = config.get("reaction_conditions", {}).get("pressure", {})
        self.reaction_network = reaction_network
        # initialize coverage
        coverage = self.ads_site.copy()
        self.coverage = {k:0 for k,_ in coverage.items()}
        self.coverage.update({"*":1})
    
    def rate(self, label):
        k_for = self.reaction_network[label].k_for
        k_rev = self.reaction_network[label].k_rev

        # count free sites
        reaction_eqn = self.reaction_network[label].reaction_eqn
        left_terms, right_terms = _rxn_eqn_slicer(reaction_eqn)        
        left, right = _free_site_regulator_for_mkm(left_terms, right_terms, self.ads_site)

        rate_for = k_for * _multipliers(left, self.ads_site, self.pressures) 
        rate_rev = k_rev * _multipliers(right, self.ads_site, self.pressures)

        return rate_for, rate_rev
    
    # def generator(self):
    #     for _, rxn in self.reaction_network:



if __name__=="__main__":
    import mkm
    import yaml
    import json
    from mkm.reaction_network import ReactionNetworkGenerator

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

    model = MKM(config, rxn_network)
    model.rate("r1")
    print