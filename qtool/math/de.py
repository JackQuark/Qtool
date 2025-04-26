# _summary_
# ==================================================
import numpy as np
import sympy as sp
from latex2sympy2 import latex2sympy
# ==================================================
__all__ = ['ODE', 'ODE_Solver']
# ==================================================

class ODE(object):
    """"""
    def __init__(self, eq: str, forcing: None | str = None):
        try:
            self.eq = latex2sympy(eq)
            lhs, rhs = eq.split('=')
            self.order = int(lhs[lhs.find('y_') + 2:])
        except Exception as e:
            raise e
        if forcing is None:
            self.forcing = lambda x: 0
        elif isinstance(forcing, str):
            self.forcing = sp.lambdify(sp.symbols('x'), latex2sympy(forcing), 'numpy')
        else:
            self.forcing = forcing

        self.varnames = ['x', 'y'] + [f'y_{i}' for i in range(1, self.order)]
        self._yn = sp.lambdify(sp.symbols(self.varnames), self.eq, modules='numpy')
        self._Y = np.zeros(self.order) # array: [y, y', y'',... y_n-1]
            
    def __call__(self, x, Y):
        """
        Args:
            x (float): 
            Y (np.ndarray): shape (order,), [y, y', y'',... y_n-1]
            """
        return self._yn(x, *Y) + self.forcing(x)
        
class ODE_Solver(object):
    """"""
    def __init__(self, ode: ODE, ic: list | np.ndarray):
        self.ode = ode
        self._ic  = ic
        if self.ode.order != len(self.ic): raise ValueError('ic length not match order of ode.')
        
    @property
    def ic(self):
        return self._ic
    @ic.setter
    def ic(self, value):
        if len(value) != self.ode.order: raise ValueError('ic length not match order of ode.')
    
    def solve(self, x0, x1, dx=.01, method='Euler'):
        """solve ode from x0 to x1 with step dx
        Args:
            x0 (float): start point of x
            x1 (float): end point of x
            dx (float): step size
            method (str): 'Euler' or 'RK4'"""
        x = np.arange(x0, x1, dx)
        Y = np.zeros((x.size, self.ode.order))
        Y[0] = self.ic
        if method == 'Euler':
            for i in range(1, x.size):
                Y[i] = self.step_Euler(dx, self.ode, x[i-1], Y[i-1])
        elif method == 'RK4':
            for i in range(1, x.size):
                Y[i] = self.step_RK4(dx, self.ode, x[i-1], Y[i-1])
        else:
            raise ValueError(f'Method {method} not supported.')
        return x, Y

    @staticmethod
    def step_Euler(dx, f, x, Y):
        return Y + np.append(Y[1:], f(x, Y)) * dx

    @staticmethod
    def step_RK4(dx, f, x, Y):
        k1 = np.append(Y[1:], f(x, Y)) * dx
        k2 = np.append(Y[1:] + k1[1:]/2, f(x, Y + k1/2)) * dx
        k3 = np.append(Y[1:] + k2[1:]/2, f(x, Y + k2/2)) * dx
        k4 = np.append(Y[1:] + k3[1:], f(x, Y + k3)) * dx
        return Y + (k1 + 2*k2 + 2*k3 + k4) / 6

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
