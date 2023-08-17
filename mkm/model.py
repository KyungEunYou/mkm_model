from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import numpy as np
from mkm.utils import (
    _rxn_eqn_slicer,
    _free_site_regulator_for_mkm,
    _multipliers,
    _add_y_ind,
)

class MKM:
    """
    reaction_network: dict e.g. {"r1": ElementaryReactionStep, "r2": ElementaryReactionStep}

    y_list: list
            in the order of the y0, this is to safely map the matrix
    config: dict, example of yaml file is in example directory
    reactant_pressures: dict, e.g. {'H2_g': 10, 'hexane_g': 1, 1hexene_g: 0}; unit: bar
    temperature_interest: int or float, choose one of temperature that is in your bag_of_energies.json
    """
    def __init__(
            self,
            reaction_network:dict, 
            y_list:list,
            adsorption_sites:dict,
            reactant_pressures:dict,
            temperature_interest:int or float or str,
            ):            
        self.reaction_network = reaction_network
        self.ads_site = adsorption_sites
        self.pressures = reactant_pressures

        self.y_list = y_list
        self.temperature = str(temperature_interest)

        # save result
        self.result_coverages = None
        self.result_rates = {}
    
    def rates(self, y):
        reaction_map = self._reactions_map()

        point = 0
        while point < len(self.reaction_network):
            point += 1
            label = f"r{point}"
            k_for = self.reaction_network[label].k_for[self.temperature]
            k_rev = self.reaction_network[label].k_rev[self.temperature]
            map = reaction_map[label]
            params = (k_for, k_rev, map)

            rate_for, rate_rev, rate_total = self._rate(y, *params)
            self.result_rates[label] = {"r_for": rate_for, "r_rev":rate_rev, "rate": rate_total}
            yield rate_total

    def balances(self, *rates):
        reaction_map = self._reactions_map()

        for y in self.y_list:
            map = self._map_balance(y, reaction_map)
            total_balance = self._balance(map, *rates)
            yield total_balance

    def dydt(self, y, t):
        y = y
        rates = tuple(self.rates(y))
        return tuple(self.balances(*rates))

    def compute(self, y, t, **params):
        self.t = t
        self.result_coverages = odeint(self.dydt, y, t, mxstep=500, **params)

        return self.result_coverages, self.result_rates
    
    def plot_coverages(self, save=False, selected_labels:list=None):
        i = 0 
        while i < self.result_coverages.shape[1]:
            if (not selected_labels or 
                (selected_labels and self.y_list[i] in selected_labels)):
                plt.plot(self.t, self.result_coverages[:, i], label=self.y_list[i])
            i += 1
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel("Time(s)")
        plt.ylabel("Fractional Coverages")
        plt.grid()
        plt.show()
        if save==True:
            plt.savefig("coverages.png", dpi=1000)
   
    def _rate(self, y, *params):
        # params
        k_for, k_rev, map = params[0], params[1], params[2]

        # rate equation
        rate_for = k_for * _multipliers(y, map["consumption"]) 
        rate_rev = k_rev * _multipliers(y, map["formation"])

        return rate_for, rate_rev, rate_for - rate_rev
    
    def _reactions_map(self):

        reaction_map = {}
        # generate reaction map
        for label, er in self.reaction_network.items():
            left, right = _rxn_eqn_slicer(er.reaction_eqn)
            left, right = _free_site_regulator_for_mkm(left, right, self.ads_site)
            left, right = _add_y_ind(left, right, self.y_list, self.pressures)
            reaction_map[label] = {"consumption":left, "formation":right}
        
        return reaction_map 

    def _balance(self, map, *rates):
        
        total_balance = 0
        pointer = 0
        while pointer < len(rates):
            label = f"r{pointer+1}"
            if label in map:
                total_balance += map[label]*rates[pointer]
            pointer += 1
        return total_balance       
    
    def _map_balance(self, y, reaction_map):
        balance_map = {}
        for r_label, map in reaction_map.items():
            if y in map["consumption"]:
                balance_map[r_label] = -1 * map["consumption"][y][0]
            elif y in map["formation"]:
                balance_map[r_label] = 1 * map["formation"][y][0]
        return balance_map

if __name__=="__main__":
    import mkm
    import yaml
    import json
    from mkm.reaction_network import ReactionNetworkGenerator

    yaml_file = f"{mkm.EXAMPLE}/config.yml"
    with open(yaml_file) as f:
        config = yaml.safe_load(f)

    json_file = f"{mkm.EXAMPLE}/bag_of_energies.json"
    with open(json_file) as f:
        bag_of_energies = json.load(f)

    rn = ReactionNetworkGenerator(
        config.get("rxn_eqn", {}), 
        bag_of_energies,
        config["adsorption"],
        )
    rxn_network = rn.convert_all()


    t = np.linspace(0, 300, 500)
    # sol = odeint(dydt, y, t, mxstep=500)
    temperature = 573.15
    y_list = ["*","I000*","I001*","I002*","I003*","I004*","I006*","I008*","I010*", "I011*","I012*","I014*","I015*"]
    y = y = np.zeros(len(y_list))
    y[y_list.index("*")] = 1
    
    print(y)

    pressure = config.get("reaction_conditions", {}).get("pressure", {})
    ads_sites = config.get("int_ads_site", {})

    mkm = MKM(
        rxn_network, 
        y_list,
        ads_sites,
        pressure, 
        temperature)
    cov, result_rates = mkm.compute(y, t)
    mkm.plot_coverages()


    y = []
    for i in range(13):
        y.append((cov[:, i][-1]))

    y_sum = 0
    for elem in y:
        y_sum += elem
        print(elem)
    print(f"total_balance: {y_sum}")

    print(result_rates)