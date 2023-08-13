import numpy as np

class AdsorptionTheories:
    def __init__(
            self,
            adsorption_theory:str="collision_theory", 
            params:dict=None, 
            temperature_range:list=[273.15]):
        
        self.adsorption_theory = adsorption_theory
        self.params = params
        self.trange = temperature_range
        self.rate_constants = self._theory_identifier()
    
    def _theory_identifier(self):
        if any(item is None for item in [self.adsorption_theory, self.params, self.trange]):
            raise ValueError("One or more required variables are None.")
        if self.adsorption_theory == "collision_theory":
            return self._collision_theory(self.params, self.trange)

    def _collision_theory(self, params:dict=None, temperature_range:list=[273.15]):
        kb_si = 1.39064852e-23    #bolzmann's constant in (m^2)*(kg)*(s^-2)*(K^-1)
        conv1 = 100000            #1bar=100000pa
        conv2 = 1e-3              #1kg=1e-3g
        na = 6.02e23              #Avogadro 6.02*10e23/mol

        try:
            s0 = params["s0"]
            n0 = params["n0"]
            ma = params["ma"] * conv2 / na
            rate_constants = {}
            for t in temperature_range:
                rate_constants[t] = conv1 * s0 / n0 / np.sqrt(2 * np.pi * ma * kb_si * float(t))

        except:
            rate_constants = None 
        return rate_constants   
    
    def calculate(self):
        return self.rate_constants
