
class ElementaryReactionStep:
    def __init__(self, label:str=None, ):
        self.label = label

    @property
    def reaction_equation(self):
        raise NotImplementedError
    
    @property
    def erxn(self):
        raise NotImplementedError
    
    @property
    def ea_for(self):
        raise NotImplementedError

    @property
    def ea_rev(self):
        raise NotImplementedError

    @property
    def ga_for(self):
        raise NotImplementedError

    @property
    def ga_rev(self):
        raise NotImplementedError

    @property
    def ka_for(self):
        raise NotImplementedError

    @property
    def ka_rev(self):
        raise NotImplementedError

    @property
    def equilibrium_const(self):
        raise NotImplementedError
    
    def _left_terms(self):
        raise NotImplementedError
    
    def _right_terms(self):
        raise NotImplementedError
    
    def _num_free_sites(self):
        raise NotImplementedError

if __name__=="__main__":
    import mkm
    import yaml

    yaml_file = f"{mkm.EXAMPLE}/config.yml"
    with open(yaml_file) as f:
        config = yaml.safe_load(f)
    
    

    print