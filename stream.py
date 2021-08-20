class Stream():

    def __init__(self, name = "stream_000", Temperature = None,  Pressure = None, molarFlow = 0.0, mComposition = None, Enthalpy = None):
        self.name =  name
        self.Temperature = Temperature
        self.Pressure = Pressure
        self.molarFlow = molarFlow
        self.mComposition = mComposition
        self.Enthalpy = Enthalpy

    def setName(self, name):
       self.name = name

    def setT(self, T):
        self.Temperature = T

    def setP(self, P):
        self.Pressure = P

    def setmF(self, mF):
        self.molarFlow = mF

    def setmC(self, mC, key = None):
        if key != None:
            self.mComposition[key] = mC
        else:
            if mC == None:
                self.mComposition = {}
            else:
                self.mComposition = mC

    def setH(self, H):
        self.Enthalpy = H

    def getName(self):
        return self.name

    def getT(self):
        return self.Temperature

    def getP(self):
        return self.Pressure

    def getmF(self):
        return self.molarFlow

    def getmC(self, key = None):
        if key != None:
            return self.mComposition[key] 
        else:
            return self.mComposition

    def getH(self):
        return self.Enthalpy

    def normalize(self):
        
        Z = sum([zi for zi in self.mComposition.values()])

        if not ((Z == 1.0) or (Z == 1)):

            for key in self.mComposition.keys():

                self.mComposition[key] = self.mComposition[key] / Z

