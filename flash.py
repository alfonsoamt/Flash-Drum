from gekko import GEKKO
import numpy as np
from stream import Stream
from math import sinh, cosh
from scipy.integrate import quad
import csv

m = GEKKO()

def Antoine(T, C1, C2, C3, C4, C5):


    P = m.exp(C1 + (C2 / T) + (C3 * m.log(T)) + (C4 * (T ** C5)))

    return (P / 1000) # kPa

def Antoinenp(T, C1, C2, C3, C4, C5):

    
    P = np.exp(C1 + (C2 / T) + (C3 * np.log(T)) + (C4 * (T ** C5)))

    return (P / 1000) # kPa

def AntoineInv(P, C1, C2, C3, C4, C5):
    
    m = GEKKO()
    T = m.Var(value = 298.15, lb = 100, ub = 800)
    m.Equation([(m.exp(C1 + (C2 / T) + (C3 * m.log(T)) + (C4 * (T ** C5))) / 1000) - P == 0])
    m.solve(disp=False)
    return float(T.value[0]) # K

def HeatVap(T, Tc, C1, C2, C3, C4):

    Tr = T / Tc
    Hvap = C1 * (1 - Tr) ** (C2 + C3 * Tr + C4 * Tr * Tr)
    return Hvap/1e6 # kJ / mol

def CP_L(T, C1, C2, C3, C4, C5):

    CPL = C1 +( C2 * T) +( C3 * (T ** 2)) +( C4 * (T ** 3)) + (C5 * (T ** 4))
    return CPL/1e6 # kJ / mol K

def CP_ig(T, C1, C2, C3, C4, C5):

    CPIG = C1 + C2 * pow((C3 / T) / (sinh(C3 / T)), 2) + C4 * pow((C5 / T) / (cosh(C5 / T)), 2)
    return CPIG/1e6 # kJ / mol K

def meanCP(f, T1, T2, ar):

    mcp, err = quad(f, T1, T2, args = ar, limit=1100)
    mcp = mcp / (T2 - T1)
    return mcp # kJ / mol K

def parameters(compounds):

    p = {'Antoine': {compound: compound_data[compound]['Antoine'] for compound in compounds},
         'AntoineInv' : {compound: compound_data[compound]['Antoine'] for compound in compounds}, 
         'Hvap' : {compound: compound_data[compound]['Hvap'] for compound in compounds},
         'CPL': {compound: compound_data[compound]['CPL'] for compound in compounds},
         'CPig': {compound: compound_data[compound]['CPIG'] for compound in compounds}}

    return p


with open('compound_data.csv', mode = 'r') as csv_f:
    reader = csv.reader(csv_f)
    compound_data = {row[0]: {'Antoine': {'C1': float(row[7]), 'C2': float(row[8]), 'C3': float(row[9]), 'C4': float(row[10]), 'C5': float(row[11])},
                                'Hvap': {'Tc': float(row[1]), 'C1': float(row[12]), 'C2': float(row[13]), 'C3': float(row[14]), 'C4': float(row[15])},
                                'CPL': {'C1': float(row[2]), 'C2': float(row[3]), 'C3': float(row[4]), 'C4': float(row[5]), 'C5': float(row[6])},
                                'CPIG': {'C1': float(row[16]), 'C2': float(row[17]), 'C3': float(row[18]), 'C4': float(row[19]), 'C5': float(row[20])}} for row in reader}
    csv_f.close()





class FlashDrum():

    def __init__(self, mode = 'Isothermal'):
        ''' The Flash Drum has one inlet stream and two outlet stream.
         The program uses the class Stream to represent the inlet and outlet process streams.
         -> feed is the inlet object from the class Stream.
         -> vapor is an outlet object from the class Stream.
         -> liquid is an outlet object from the class Stream.
         -> mode refers to calculations made by the program, default is "Isothermal", it also can work in "Adiabatic".
         -> psi is the vapor outlet / feed inlet ratio.
         -> Heat is the heat in kJ/mol that the Flash Drum requires.
         -> Temperature is the Flash Drum operating temperature in K.
         -> Pressure is the Flash Drum operating pressure kPa.
         -> Tref is the reference temperature in K for the energy balance calculations. 
         This class only works with pressure in kPa and temperature in K. '''
        self.feed = Stream("FEED")
        self.vapor = Stream("VAPOR")
        self.liquid = Stream("LIQUID")
        self.mode = mode
        self.psi = 0
        self.Heat = None
        self.Temperature = None
        self.Pressure = None
        self.Tref = 298.15


    def setFeedStream(self, inletStream = Stream("FEED")):
        '''Set the feed stream properties.'''
        inletStream.normalize()
        self.feed.setT(inletStream.Temperature)
        self.feed.setP(inletStream.Pressure)
        self.feed.setmF(inletStream.molarFlow)
        self.feed.setmC(inletStream.mComposition)
        self.feed.setH(inletStream.Enthalpy)
        

    def Streams(self, energy = False):
        ''' Display the stream results in a table. '''

        stream_table1 = "-"*100 + "\n\t\t\t\tF L A S H  D R U M: \t" + self.mode.upper() + "\n"+"-"*100 \
            + "\nStreams:\t\t" + "FEED" + " " * 20 + "VAPOR " + " " * 20 + "LIQUID" \
            + "\n" + "-"*100 + \
            "\n\t\t\t" + "T_f = " + str(round(self.feed.getT(), 2)) + " K" + \
              "\t\t" + "T_v = " + str(round(self.vapor.getT(), 2)) + " K" + \
              "\t\t  " + "T_l = " + str(round(self.liquid.getT(), 2)) + " K" + \
            "\n\t\t\t" + "P_f = " + str(self.feed.getP()) + " kPa" + \
              "\t\t" + "P_v = " + str(self.vapor.getP()) + " kPa" + \
              "\t\t  " + "P_l = " + str(self.liquid.getP()) + " kPa" + \
            "\n\t\t\t" + "F = " + str(round(self.feed.getmF(), 3)) + " mol/h" + \
              "\t\t" + "V = " + str(round(self.vapor.getmF(), 3)) + " mol/h" + \
              "\t\t  " + "L = " + str(round(self.liquid.getmF(), 3)) + " mol/h"
        stream_table2 = ""
        for key in self.feed.getmC().keys():
            stream_table2 += "\n" + key + "\t\t\tz = " + str(round(self.feed.getmC(key), 3)) + \
              "\t\t" + "y = " + str(round(self.vapor.getmC(key), 3)) + \
              "\t\t\t  " + "x = " + str(round(self.liquid.getmC(key),3))
        stream_table3 = ""
        if energy:    
            stream_table3 += "\n\t\t\t" + "h_f = " + str(round(self.feed.getH(), 3)) + " kJ/mol" + \
                "\t" + "h_v = " + str(round(self.vapor.getH(), 3)) + " kJ/mol" + \
                "\t  " + "h_l = " + str(round(self.liquid.getH(), 3)) + " kJ/mol" + "\n" + "-"*100 + \
                "\n\t\t\tHEAT: Q = " + str(round(self.Heat)) + " kJ/mol"
        stream_table3 += "\n" + "-"*100
        stream_table = stream_table1 + stream_table2 + stream_table3
        return stream_table

    
    def saveResults(self):
        feed = {'name': self.feed.getName(),
                'Temeperature': self.feed.getT(),
                'Pressure': self.feed.getP(),
                'Molar Flow': self.feed.getmF(),
                'Molar Composition': self.feed.getmC(),
                'Enthalpy': self.feed.getH()}
        vapor = {'name': self.vapor.getName(),
                'Temeperature': self.vapor.getT(),
                'Pressure': self.vapor.getP(),
                'Molar Flow': self.vapor.getmF(),
                'Molar Composition': self.vapor.getmC(),
                'Enthalpy': self.vapor.getH()}
        liquid = {'name': self.liquid.getName(),
                'Temeperature': self.liquid.getT(),
                'Pressure': self.liquid.getP(),
                'Molar Flow': self.liquid.getmF(),
                'Molar Composition': self.liquid.getmC(),
                'Enthalpy': self.liquid.getH()}
        Q = self.Heat
        Psi = self.psi
        mode = self.mode
        results = {'Drum': {'mode': mode, 'Heat': Q, 'Psi': Psi},
                    'Feed': feed,
                    'Vapor': vapor,
                    'Liquid': liquid}
        return  results


    def idealK(self, T, P, c):
        ''' Caculates an ideal K parameter with Raoult's Law'''
        Psat = Antoine(T, **c)
        return Psat / P


    def isothermal(self, T, P, c, energy = False):
        ''' Simulates an Isothermal Flash Drum given an operating temperature and pressure.'''
        self.mode = "Isothermal"
        self.vapor.setT(T)
        self.vapor.setP(P)
        self.liquid.setT(T)
        self.liquid.setP(P)
        self.vapor.setmC(None)
        self.liquid.setmC(None)
        Tf_bubble = self.bubbleT(self.feed.getP(), c)
        Tf_dew = self.dewT(self.feed.getP(), c)
        T_bubble = self.bubbleT(P, c)
        T_dew = self.dewT(P, c)
        Tf = self.feed.getT()
        Tf_mode = None
        # Check for the feedstream condition
        if Tf <= Tf_bubble:

            Tf_mode = "liquid"

        elif Tf >= Tf_dew:

            Tf_mode = "vapor"

        else:

            Tf_mode = "mixture"

        Tref = self.Tref            
        cpl = {}
        cpig = {}
        hf = {}
        hv = {}
        hl = {}
        tb = {}

        ### MATERIAL BALANCE AND ENERGY BALANCE
        # Check if the operating temperature is between the limits for the PSI calculations.

        ## BELOW BUBBLE TEMPERATURE MEANS LIQUID PHASE ONLY
        if T <= T_bubble:
            ## MATERIAL BALANCE
            #  There is no vapor phase
            self.psi = 0
            self.vapor.setmF(0) 
            self.liquid.setmF(self.feed.getmF())

            for key in self.feed.getmC().keys():

                self.liquid.setmC((self.feed.getmC(key)), key)
                self.vapor.setmC(0, key)

            ## ENERGY BALANCE, if enabled ...
            if energy:
                
                for key in self.feed.getmC().keys():
                    # Mean heat capacity
                    cpl[key] = meanCP(CP_L, T_bubble,  T_dew, tuple([value for value in c['CPL'][key].values()]))
                    # Enthalply calculation.
                    if Tf_mode == "liquid":

                        hf[key] = self.feed.getmC(key) * cpl[key] * (Tf - Tref)
                        

                    elif Tf_mode == "vapor":

                        cpig[key] = meanCP(CP_ig, T_bubble,  T_dew, tuple([value for value in c['CPig'][key].values()]))
                        tb[key] = AntoineInv(P, **c['AntoineInv'][key])
                        hf[key] = self.feed.getmC(key) * (cpl[key] * (tb[key] - Tref) + HeatVap(tb[key], **c['Hvap'][key]) + cpig[key] * (T - tb[key]))

                    else:

                         hf[key] = self.feed.getmC(key) * (cpl[key] * (T - Tref) + HeatVap(T, **c['Hvap'][key]))

                    hl[key] = self.liquid.getmC(key) * cpl[key] * (T - Tref)
                    hv[key] = 0.0

                self.feed.setH(sum([value for value in hf.values()])) 
                self.liquid.setH( sum([value for value in hl.values()]))
                self.vapor.setH(0.0)

                # Energy balance for heat (Q) caculation.
                self.Heat = self.vapor.getmF() * self.vapor.getH() + self.liquid.getmF() * self.liquid.getH() - self.feed.getmF() * self.feed.getH()

        ## ABOVE DEW TEMPERATURE MEANS VAPOR PHASE ONLY    
        elif T >= T_dew:
            ## MATERIAL BALANCE
            #  There is no vapor phase
            self.psi = 1
            self.vapor.setmF(self.feed.getmF()) 
            self.liquid.setmF(0)

            for key in self.feed.getmC().keys():

                self.liquid.setmC(0, key)
                self.vapor.setmC(self.feed.getmC(key), key)

            ## ENERGY BALANCE, if enabled ...
            if energy:



                for key in self.feed.getmC().keys():
                    # Mean heat capacity
                    cpl[key] = meanCP(CP_L, T_bubble,  T_dew, tuple([value for value in c['CPL'][key].values()]))
                    cpig[key] = meanCP(CP_ig, T_bubble,  T_dew, tuple([value for value in c['CPig'][key].values()]))
                    # Enthalply calculation.
                    if Tf_mode == "liquid":

                        hf[key] = self.feed.getmC(key) * cpl[key] * (Tf - Tref)                        

                    elif Tf_mode == "vapor":

                        tb[key] = AntoineInv(P, **c['AntoineInv'][key])
                        hf[key] = self.feed.getmC(key) * (cpl[key] * (tb[key] - Tref) + HeatVap(tb[key], **c['Hvap'][key]) + cpig[key] * (T - tb[key]))

                    else:

                         hf[key] = self.feed.getmC(key) * (cpl[key] * (T - Tref) + HeatVap(T, **c['Hvap'][key]))

                    hl[key] = 0
                    tb[key] = AntoineInv(P, **c['AntoineInv'][key])
                    hv[key] = self.vapor.getmC(key) * (cpl[key] * (tb[key] - Tref) + HeatVap(tb[key], **c['Hvap'][key]) + cpig[key] * (T - tb[key]))

                self.feed.setH(sum([value for value in hf.values()])) 
                self.liquid.setH(0)
                self.vapor.setH(sum([value for value in hv.values()]))

                # Energy balance for heat (Q) caculation.
                self.Heat = self.vapor.getmF() * self.vapor.getH() + self.liquid.getmF() * self.liquid.getH() - self.feed.getmF() * self.feed.getH()

        # DRUM TEMPERATURE BETWEEN BUBBLE AND DEW TEMPERATURES
        else:
            ## MATERIAL BALANCE
            # Create a gekko model for solve the equations system
            m = GEKKO()        
            # Ki calculations.
            Ki = {}

            for key in self.feed.getmC().keys():

                K = m.Intermediate(self.idealK(T,P, c['Antoine'][key]))
                Ki[key] = K
            
            Psi = m.Var(value=0.5, lb= 0.0, ub = 1.0)
            x = sum([((self.feed.getmC(key) * (1 - Ki[key])) / (1 + Psi * (Ki[key] - 1))) for key in Ki.keys()])
            m.Equation([x == 0])
            m.solve(disp=False) 
            self.psi = float(Psi.value[0]) 
            # Calulate vapor and liquid molar flows.
            self.vapor.setmF(self.psi * self.feed.getmF()) 
            self.liquid.setmF(self.feed.getmF() - self.vapor.getmF())
            # Calculate vapor and liquid molar compositions
            for key in Ki.keys():

                self.liquid.setmC((self.feed.getmC(key)) / (1 + self.psi * (Ki[key][0] - 1)), key)
                self.vapor.setmC(self.liquid.getmC(key)  * Ki[key][0], key)
        
            ## ENERGY BALANCE, if enabled ...        
            if energy:

                for key in self.feed.getmC().keys():
                    # Mean heat capacity
                    cpl[key] = meanCP(CP_L, T_bubble,  T_dew, tuple([value for value in c['CPL'][key].values()]))
                    # Enthalply calculation.
                    if Tf_mode == "liquid":

                        hf[key] = self.feed.getmC(key) * cpl[key] * (Tf - Tref)                        

                    elif Tf_mode == "vapor":

                        cpig[key] = meanCP(CP_ig, T_bubble,  T_dew, tuple([value for value in c['CPig'][key].values()]))
                        tb[key] = AntoineInv(P, **c['AntoineInv'][key])
                        hf[key] = self.feed.getmC(key) * (cpl[key] * (tb[key] - Tref) + HeatVap(tb[key], **c['Hvap'][key]) + cpig[key] * (T - tb[key]))

                    else:

                         hf[key] = self.feed.getmC(key) * (cpl[key] * (T - Tref) + HeatVap(T, **c['Hvap'][key]))

                    hl[key] = self.liquid.getmC(key) * cpl[key] * (T - Tref)
                    hv[key] = self.vapor.getmC(key) * (cpl[key] * (T - Tref) + HeatVap(T, **c['Hvap'][key]))

                self.feed.setH(sum([value for value in hf.values()])) 
                self.liquid.setH( sum([value for value in hl.values()]))
                self.vapor.setH(sum([value for value in hv.values()]))

                # Energy balance for heat (Q) caculation.
                self.Heat = self.vapor.getmF() * self.vapor.getH() + self.liquid.getmF() * self.liquid.getH() - self.feed.getmF() * self.feed.getH()


    def adiabatic(self, P, c):
        ''' It makes adibatic flash caculations given an operating pressure.'''
        self.mode ="Adiabatic"
        self.Pressure = P
        self.vapor.setP(P)
        self.liquid.setP(P)
        self.vapor.setmC(None)
        self.liquid.setmC(None)        
        Tf_bubble = self.bubbleT(self.feed.getP(), c)
        Tf_dew = self.dewT(self.feed.getP(), c)
        Tf = self.feed.getT()
        Tf_mode = None
        Tref = self.Tref        
        cpl = {}
        cpig = {}
        hf = {}
        hg = {}
        hl = {}
        # Check for the feedstream condition
        if Tf <= Tf_bubble:

            Tf_mode = "liquid"
            T_bubble = self.bubbleT(P, c)
            T_dew = self.dewT(P, c)
            Tf = self.feed.getT()
            Tf_mode = None
            Tref = self.Tref        
            cpl = {}
            cpig = {}
            hf = {}
            hg = {}
            hl = {}
            m = GEKKO()
            #m.options.MAX_ITER = 500
            Psi = m.Var(value=0.5, lb= 0.0, ub = 1.0)
            T = m.Var(value=(T_bubble + T_dew) * 0.5, lb = 200, ub = 800)
            # K's 
            Ki = {}
            # Ki calculations are made.
            for key in self.feed.getmC().keys():
                K = m.Intermediate(self.idealK(T,P, c['Antoine'][key]))

                Ki[key] = K

            x = sum([((self.feed.getmC(key) * (1 - Ki[key])) / (1 + Psi * (Ki[key] - 1))) for key in Ki.keys()])
            # Intermediate equations:
            self.vapor.setmF( Psi * self.feed.getmF()) 
            self.liquid.setmF(self.feed.getmF() - self.vapor.getmF())

            for key in Ki.keys():
                self.liquid.setmC((self.feed.getmC(key)) / (1 + Psi * (Ki[key] - 1)), key)
                self.vapor.setmC(self.liquid.getmC(key)  * Ki[key], key)

            # Intermediate energy Balance        
            for key in self.feed.getmC().keys():

                cpl[key] = meanCP(CP_L, T_bubble,  T_dew, tuple([value for value in c['CPL'][key].values()]))
                #cpig[key] = meanCP(CP_ig, T_bubble,  T_dew, tuple([value for value in c['CPig'][key].values()]))
                hf[key] = self.feed.getmC(key) * cpl[key] * (Tf - Tref)                        
                hl[key] = self.liquid.getmC(key) * cpl[key] * (T - Tref)
                hg[key] = self.vapor.getmC(key) * (cpl[key] * (T - Tref) + HeatVap(T, **c['Hvap'][key]))

            self.feed.setH( sum([value for value in hf.values()])) 
            self.liquid.setH( sum([value for value in hl.values()]))
            self.vapor.setH( sum([value for value in hg.values()]))
            # Second equaion: f(T) == 0
            y = self.vapor.getmF() * self.vapor.getH() + self.liquid.getmF() * self.liquid.getH() - self.feed.getmF() * self.feed.getH()
            # Solve the equations system
            m.Equation([x == 0, y == 0])
            m.solve(disp=False)
            # Evaluate the results of T and PSI in the intermediate equations
            self.psi = float(Psi.value[0])
            self.Temperature = float(T.value[0])
            # Real Ki calculations are made.
            for key in self.feed.getmC().keys():

                Ki[key] = Ki[key][0]
            # Calulate vapor and liquid molar flows.
            self.vapor.setmF( self.psi * self.feed.getmF()) 
            self.liquid.setmF(self.feed.getmF() - self.vapor.getmF())
            # Calculate vapor and liquid molar compositions
            for key in Ki.keys():

                self.liquid.setmC((self.feed.getmC(key)) / (1 + self.psi * (Ki[key] - 1)), key)
                self.vapor.setmC(self.liquid.getmC(key)  * Ki[key], key)

            #Real Energy Balance        
            for key in self.feed.getmC().keys():
                # Mean heat capacity
                cpl[key] = meanCP(CP_L, T_bubble,  T_dew, tuple([value for value in c['CPL'][key].values()]))
                #cpig[key] = meanCP(CP_ig, T_bubble,  T_dew, tuple([value for value in c['CPig'][key].values()]))
                # Enthalply calculation.
                hf[key] = self.feed.getmC(key) * cpl[key] * (Tf - Tref)
                hl[key] = self.liquid.getmC(key) * cpl[key] * (self.Temperature - Tref)
                hg[key] = self.vapor.getmC(key) * (cpl[key] * (self.Temperature - Tref) + HeatVap(self.Temperature, **c['Hvap'][key]))

            self.feed.setH( sum([value for value in hf.values()])) 
            self.liquid.setH( sum([value for value in hl.values()]))
            self.vapor.setH( sum([value for value in hg.values()]))
            Q = self.vapor.getmF() * self.vapor.getH() + self.liquid.getmF() * self.liquid.getH() - self.feed.getmF() * self.feed.getH()
            self.vapor.setT(self.Temperature)
            self.liquid.setT(self.Temperature)
            self.Heat = Q

        else:

            self.mode ="Adiabatic: NO SOLVED!"
            self.vapor.setmF(0)
            self.liquid.setmF(0)
            self.vapor.setH(0)
            self.liquid.setH(0)
            self.vapor.setT(0)
            self.liquid.setT(0)
            self.vapor.setP(0)
            self.liquid.setP(0)
            self.Heat = 0

            for key in self.feed.getmC().keys():

                self.vapor.setmC(0, key)
                self.liquid.setmC(0, key)

        


    def bubbleT(self, P, c):
        ''' Bubble temperature calculation given an operating pressure.'''
        m = GEKKO()

        T = m.Var(value = 298.15, lb = 0.0, ub = 800.0)
        # K's 
        Ki = {}

        for key in self.feed.getmC().keys():
            Ki[key] = self.idealK(T,P, c['Antoine'][key])
        
        x = sum([self.feed.getmC(key) * Ki[key] for key in Ki.keys()])
        m.Equation([x - 1 == 0])
        m.solve(disp=False) 

        return round(T.value[0], 2)


    def dewT(self, P, c ):
        ''' Dew temperature calculation given an operating pressure.'''
        m = GEKKO()

        T = m.Var(value = 298.15, lb = 200.0, ub = 800.0)
        # K's 
        Ki = {}

        for key in self.feed.getmC().keys():
            Ki[key] = self.idealK(T,P, c['Antoine'][key])

        x = sum([self.feed.getmC(key) / Ki[key] for key in Ki.keys()])
        m.Equation([x - 1 == 0])
        m.solve(disp=False) 

        return round(T.value[0], 2)


    def bubbleP(self, T, c):
        ''' Bubble pressure calculation given an operating temperature.'''
        P = sum([self.feed.getmC(key) * Antoinenp(T, **c['Antoine'][key]) for key in self.feed.getmC().keys()])

        return P


    def dewP(self, T, c):
        ''' Dew pressure calculation given an operating temperature.'''
        P = sum([self.feed.getmC(key) / Antoinenp(T, **c['Antoine'][key]) for key in self.feed.getmC().keys()]) ** (-1)

        return round(P, 3)

