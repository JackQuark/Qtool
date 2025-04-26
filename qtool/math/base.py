# _summary_
# ==================================================
import numpy as np
import sympy as sp
from numpy import cos, sin

from latex2sympy2 import latex2sympy
# ==================================================
__all__ = ['Piecewise_Func']
# ==================================================
class Piecewise_Func(object):
    """
    Args:
        eq (str | dict[str, function]):
            if str, it should be a string of latex equation, and the boundary condition will be set to ALL.\\
            if dict, it should be a string of latex equation as key and function of boundary condition as value.
    """
    def __init__(self, eq: str | dict[str, 'function']):
        if isinstance(eq, str):
            eq = {eq: lambda x: True}

        self._f = []
        self._cond = []       
        for key, val in eq.items():
            self._f.append(sp.lambdify(sp.symbols('x'), latex2sympy(key), 'numpy'))
            self._cond.append(val)

    def __call__(self, t):
        if isinstance(t, int | float):
            for f_, cond_ in zip(self._f, self._cond):
                if cond_(t):
                    return f_(t)
        else:            
            res = np.zeros(len(t))
            for f_, cond_ in zip(self._f, self._cond):
                res += np.where(cond_(t), f_(t), 0)
            return res

class _Piecewise_Func(object):
    """
    Args:
        funcs (list[typeA]):
            typeA: int | float | str | 'function'
        conds (list[typeB]):
            typeB: str | 'function'
        """
    def __init__(self, 
                 funcs: list[int | float | str], 
                 conds: list[str]):
        if (N := len(funcs)) != len(conds):
            raise ValueError("len(eqs) doesn't match len(conds)")
        self._funcs = []
        self._conds = []
        for i in range(N):
            self._funcs.append(self._phase_func(funcs[i]))
            self._conds.append(self._phase_cond(conds[i]))
    
    def _phase_func(self, o):
        if isinstance(o, (int, float)):
            return lambda x: o
        elif isinstance(o, str):
            return sp.lambdify()
        elif callable(o):
            return o
        else:
            raise ValueError(f"Invalid func type: {type(o)}")
    
    def _phase_cond(self, o):
        if isinstance(o, str):
            return sp.lambdify()
        elif callable(o):
            return o
        else:
            raise ValueError(f"Invalid cond type: {type(o)}")
        
    def __call__(self, x):
        if hasattr(x, '__iter__'): # for a sequence of x
            res = np.zeros(len(x))
            for func, cond in zip(self._funcs, self._conds):
                res += np.where(cond(x), func(x), 0)
            return res
        else: # for single x
            res = 0
            for func, cond in zip(self._funcs, self._conds):
                if cond(x): 
                    res += func(x)
            return res

class Delta_Func(object):
    def __init__(self, ):
        pass
# ==================================================

def main():
    
    f = _Piecewise_Func(
        [0, lambda x: x, 0], [lambda x: x<1, lambda x: (x>=1) & (x<3), lambda x: x>=3]
    )
    
    t = np.arange(0, 5, 0.01)  
    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(4, 2))
    plt.plot(t, f(t))
    

# ==================================================
from time import perf_counter
if __name__ == '__main__':
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print('\ntime :%.3f ms' %((end_time - start_time)*1000))
