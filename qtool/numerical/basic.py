# _summary_
# ==================================================
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from time import perf_counter
# ==================================================

__all__ = ['Numerical_Diff']
__filedir__ = os.path.dirname(__file__)

# ==================================================

class Numerical_Diff(object):
    """Numerical Differentiation\n
    Continuous Function f with step size h\n
    or\n
    Discrete Data f(x_i) = y_i, i=1,2,...,n
    
    Args:
        f (function): function
        h (float): step size
        x (list | numpy.ndarray): x-axis data
        y (list | numpy.ndarray): y-axis data
    """
    def __init__(self, 
                 f: 'function' = None, h: float = None,
                 x = None, y = None):
        
        if f is None and h is None:
            self._x = x
            self._y = y
            self._h = np.mean(np.diff(x))
            self._type = 'discrete'
        else:
            self._f = f
            self._h = h
            self._type = 'continuous'
            
        self._methods = {
            '2pc1d': self._2pt_central_1stDiff,
            '4pc1d': self._4pt_central_1stDiff,
            '3pf1d': self._3pt_forward_1stDiff,
            '3pb1d': self._3pt_backward_1stDiff,
            '3pc2d': self._3pt_central_2ndDiff,
            '4pf2d': self._4pt_forward_2ndDiff,
            '4pb2d': self._4pt_backward_2ndDiff
        }
        
    def __call__(self, method: str, x = None):
        """
        
        
        self._methods = {
            '2pc1d': self._2pt_central_1stDiff,
            '4pc1d': self._4pt_central_1stDiff,
            '3pf1d': self._3pt_forward_1stDiff,
            '3pb1d': self._3pt_backward_1stDiff,
            '3pc2d': self._3pt_central_2ndDiff,
            '4pf2d': self._4pt_forward_2ndDiff,
            '4pb2d': self._4pt_backward_2ndDiff
        }
        """
        
        
        if method in self._methods.keys():
            
            if self._type == 'continuous':
                y_tmp = np.array(
                    [self._f(x) for x in x + np.arange(-2, 3) * self._h]
                    )
                res = self._methods[method](y_tmp)
                return res[res.size // 2]
                
            else:
                return self._methods[method](self._y)
        
        else:
            raise ValueError('Invalid type')
                       
    def _2pt_central_1stDiff(self, y):
        return (y[2:] - y[:-2]) / (2*self._h)
    
    def _4pt_central_1stDiff(self, y):
        return (y[:-4] - 8*y[1:-3] + 8*y[3:-1] - y[4:]) / (12*self._h)

    def _3pt_forward_1stDiff(self, y):
        return (-3*y[:-2] + 4*y[1:-1] - y[2:]) / (2*self._h)

    def _3pt_backward_1stDiff(self, y):
        return (3*y[2:] - 4*y[1:-1] + y[:-2]) / (2*self._h)

    def _3pt_central_2ndDiff(self, y):
        return (y[:-2] - 2*y[1:-1] + y[2:]) / self._h**2

    def _4pt_forward_2ndDiff(self, y):
        return (2*y[:-3] - 5*y[1:-2] + 4*y[2:-1] - y[3:]) / self._h**2

    def _4pt_backward_2ndDiff(self, y):
        return (2*y[3:] - 5*y[2:-1] + 4*y[1:-2] - y[:-3]) / self._h**2

# ==================================================

def main():
    pass

# ==================================================

if __name__ == '__main__':
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print('\ntime :%.3f ms' %((end_time - start_time)*1000))