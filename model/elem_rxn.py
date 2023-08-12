import 

class ElementaryReaction:
    def __init__(self, label=None:str):
        self.label = label
    
    @property
    def reaction_equation(self):
        raise NotImplementedError
    
    @property
    def potential_energy_reaction(self):
        raise NotImplementedError
    
    @property
    def potential_energy_activation_forward(self):
        raise NotImplementedError

    @property
    def potential_energy_activation_reverse(self):
        raise NotImplementedError

    @property
    def free_energy_activation_forward(self):
        raise NotImplementedError

    @property
    def free_energy_activation_reverse(self):
        raise NotImplementedError

    @property
    def rate_constant_forward(self):
        raise NotImplementedError

    @property
    def rate_constant_reverse(self):
        raise NotImplementedError

    @property
    def equilibrium_constant(self):
        raise NotImplementedError