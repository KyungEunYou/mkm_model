from collections import Counter

def _is_adsorption_step(reaction_eqn:str):
    left, right = _rxn_eqn_slicer(reaction_eqn=reaction_eqn)
    for i in (left + right):
        if i.endswith("_g"):
            return True
        else:
            return False

def _rxn_eqn_slicer(reaction_eqn:str):
    elem_list = reaction_eqn.split()
    elem_list = [item for item in elem_list if item != '+']
    arrow_pointer = 0
    for elem in elem_list:
        if elem == '->':
            break
        arrow_pointer += 1

    return elem_list[:arrow_pointer], elem_list[arrow_pointer+1:]

def _free_site_regulator(left, right):
    redundant_free_sites = (len([i for i in right if i == "*" or i.endswith("*")])
        - len([i for i in left if i == "*" or i.endswith("*")]))
    if redundant_free_sites < 0:
        right += ["*"]*abs(redundant_free_sites)
    elif redundant_free_sites > 0:
        left += ["*"]*abs(redundant_free_sites)
    while "*" in left and "*" in right:
        right.remove("*")
        left.remove("*")        
    return left, right

def _free_site_regulator_for_mkm(left, right, ads_info:dict):

    ads_info.update({"*":1})
    right_sites = sum(ads_info[i] for i in right if i.endswith("*"))
    lift_sites = sum(ads_info[i] for i in left if i.endswith("*"))

    redundant_free_sites = right_sites - lift_sites
    if redundant_free_sites < 0:
        right += ["*"]*abs(redundant_free_sites)
    elif redundant_free_sites > 0:
        left += ["*"]*abs(redundant_free_sites)
    while "*" in left and "*" in right:
        right.remove("*")
        left.remove("*")
    right = dict(Counter(right))
    left = dict(Counter(left))
    return left, right

def _multipliers(one_side:dict, coverage:dict, pressures_info:dict):
    multiplier = 1
    for ads, site in one_side.items():
        if ads.endswith("_g"):
            try:
                multiplier *= pressures_info[ads]
            except:
                print(f"{ads} is not in pressure information")
        else:
            multiplier *= coverage[ads]**site
    return multiplier

def _delta_energy(
        bag_of_energies,
        left, right, energy_type:str="potential_energy"):
    new_copy = {}
    for _, v in bag_of_energies.items():
        new_copy.update(v)
    if energy_type == "potential_energy":
        left_sum = sum([new_copy[i][energy_type] for i in left])
        right_sum = sum([new_copy[i][energy_type] for i in right])
        return right_sum - left_sum
    
    elif energy_type == "free_energy":
        delta_dict = {}
        trange = list(new_copy[list(new_copy.keys())[0]][energy_type].keys())
        for t in trange:
            left_sum = sum([new_copy[i][energy_type][t] for i in left])
            right_sum = sum([new_copy[i][energy_type][t] for i in right])
            delta_dict[t] = right_sum - left_sum 
        return delta_dict        
