# _summary_
# ==================================================
from numpy import exp, log
# ==================================================

Rd = 287.  # J/kg/K
Cp = 1004. # J/kg/K
Lv = 2.5e6 # J/kg
Rv = 461.  # J/kg/K
g  = 9.81  # m/s^2
Gamma_d = g / Cp # K/m
    
def th_2_T(th, P):
    """potential Temp. [K] => Temp. [K]"""
    Temp = th * (P / 1e3)**(Rd/Cp)
    return Temp

def T_2_th(Temp, P):
    """Temp. [K] => potential Temp. [K]"""
    th = Temp * (1e3 / P)**(Rd/Cp)
    return th

def T_2_Tv(Temp, qv):
    """Temp. [K] => virtual Temp. [K]"""
    Tv = Temp * (1 + qv * (1-Rd / Rv) / Rd / Rv)
    return Tv

def theta_e(Temp, qv, p):
    """equivalent potential Temp. [K]"""
    return T_2_th(Temp + qv * Lv / Cp, p)

def theta_e_ac(th, Tc, qv):
    return th * exp((Lv * qv) / (Cp * Tc))
    
# cc equation
# Temp. [K] <=> saturated vapor pressure [hPa]
def cc_equation(Temp):
    es = 6.112 * exp(Lv/Rv * (1/273 - 1/Temp)) # hPa
    return es

def anti_cc_equation(es):
    Temp = 1 / ((1/273.15) - (Rv/Lv) * log(es/6.112))
    return Temp
    
# specific humidity [kg/kg] <=> vapor pressure [hPa]
def e_2_qv(e, P):
    qv = (Rd/Rv) * e / P
    return qv

def qv_2_e(qv, P):
    e = P * qv / (Rd/Rv)
    return e

# moist adiabatic lapse rate [K/m]
def gamma_m(T, qvs):
    Cp_star = (Cp *
        (1 + (Lv**2 * qvs / (Cp * Rv * T**2))) /
        (1 + (Lv * qvs / (Rd * T))))
    return g / Cp_star
    
# ==================================================
    
def main():
    pass

# ==================================================
from time import perf_counter
if __name__ == '__main__':
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print('\ntime :%.3f ms' %((end_time - start_time)*1000))