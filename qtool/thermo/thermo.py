from math import exp, log

# thermodynamic functioms
class Thermo:
    # thermodynamic parameters
    Rd = 287.  # J/kg/K
    Cp = 1004. # J/kg/K
    Lv = 2.5e6 # J/kg
    Rv = 461.  # J/kg/K
    g  = 9.81  # m/s^2
    epsilon= Rd / Rv 
    Gamma_d = g / Cp 
    
    def __init__(self):
        pass
    
    @staticmethod
    def th_2_T(th, P):
        """potential Temp. [K] => Temp. [K]"""
        Temp = th * (P / 1e3)**(Thermo.Rd/Thermo.Cp)
        return Temp
    
    @staticmethod
    def T_2_th(Temp, P):
        """Temp. [K] => potential Temp. [K]"""
        th = Temp * (1e3 / P)**(Thermo.Rd/Thermo.Cp)
        return th
    
    @staticmethod
    def T_2_Tv(Temp, qv):
        """=> virtual Temp. [K]"""
        Tv = Temp * (1 + qv * (1-Thermo.epsilon) / Thermo.epsilon)
        return Tv

    @staticmethod
    def theta_e(Temp, qv, p):
        """equivalent potential Temp. [K]"""
        return Thermo.T_2_th(Temp + qv * Thermo.Lv / Thermo.Cp, p)
    
    @staticmethod
    def theta_e_ac(th, Tc, qv):
        return th * exp((Thermo.Lv * qv) / (Thermo.Cp * Tc))
        
    # cc equation
    # Temp. [K] <=> saturated vapor pressure [hPa]
    @staticmethod
    def cc_equation(Temp):
        es = 6.112 * exp(Thermo.Lv/Thermo.Rv * (1/273 - 1/Temp)) # hPa
        return es
    
    @staticmethod
    def anti_cc_equation(es):
        Temp = 1 / ((1/273.15) - (Thermo.Rv/Thermo.Lv) * log(es/6.112))
        return Temp
        
    # specific humidity [kg/kg] <=> vapor pressure [hPa]
    @staticmethod
    def e_2_qv(e, P):
        qv = (Thermo.Rd/Thermo.Rv) * e / P
        return qv
    
    @staticmethod
    def qv_2_e(qv, P):
        e = P * qv / (Thermo.Rd/Thermo.Rv)
        return e
    
    # moist adiabatic lapse rate [K/m]
    @staticmethod
    def gamma_m(T, qvs):
        Cp_star = (Thermo.Cp *
            (1 + (Thermo.Lv**2 * qvs / (Thermo.Cp * Thermo.Rv * T**2))) /
            (1 + (Thermo.Lv * qvs / (Thermo.Rd * T))))
        return Thermo.g / Cp_star
    