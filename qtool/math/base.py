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
    """1 variable piecewise function.
    Args:
        items (list[tuple]):
            tuple: (function, condition) \\
            function: int | float | str | 'function' \\
            condition: str | 'function'
            
    Example:
        ```python
        f = Piecewise_Func([
            (lambda x: 2*x, 'x < 1'),
            ('x^2', lambda x: (x>=1) & (x<3)),
            (1, lambda x: (x>=3) & (x<5)),
        ])
        ```
    """
    def __init__(self, items: list[tuple]):
        self._funcs = []
        self._conds = []
        for i in range(N := len(items)):
            self._funcs.append(self._phase_func(items[i][0]))
            self._conds.append(self._phase_cond(items[i][1]))
    
    def _phase_func(self, o):
        if isinstance(o, (int, float)):
            return lambda x: o
        elif isinstance(o, str):
            return sp.lambdify('x', latex2sympy(o), 'numpy')
        elif callable(o):
            return o
        else:
            raise ValueError(f"Invalid func type: {type(o)}")
    
    def _phase_cond(self, o):
        if isinstance(o, str):
            return sp.lambdify('x', latex2sympy(o), 'numpy')
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
    def __init__(self, x, dx=1e-4):
        self.x  = x
        self.dx = dx
        self.h  = 1 / dx
        
    def __call__(self, x):
        if abs(x-self.x) < self.dx:
            return self.h
        else:
            return 0
    
# ==================================================

def main():
    
    return 

# ==================================================
from time import perf_counter
if __name__ == '__main__':
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print('\ntime :%.3f ms' %((end_time - start_time)*1000))
