# Class Polynomial 
# ==================================================
import numpy                as np
import matplotlib.pyplot    as plt
from   math                 import pi, sin, cos, sqrt
# ==================================================

def pt_to_poly(x: list|np.ndarray, y: list|np.ndarray) -> np.ndarray:
    """n points to n-1 degree polynomial (invertible)

    Args:
        x (list | np.ndarray): x values
        y (list | np.ndarray): y values

    Returns:
        np.ndarray: _coeff of the polynomial (0 to n-1 degree)_
    """
    if len(x)!= len(y):
        raise ValueError("x and y must have the same length")
    
    x_i = np.array(x).reshape(-1, 1)
    y_i = np.array(y).reshape(-1, 1)
    
    power_x = np.power(x_i, np.arange(x_i.size))
    
    try:
        power = np.linalg.inv(power_x)
    except np.linalg.LinAlgError:
        raise ValueError("The polynomial is not invertible")
    
    return np.dot(power, y_i).reshape(-1)

class Polynomial(object):
    def __init__(self, coeff: list|np.ndarray, symbol='x'):
        """single variable polynomial
        Args:
            coeff (list): order from degree 0 to highest degree \n
                e.g. [1, 2, 3] represents 1 + 2x + 3x^2
            symbol (str): default is 'x'
        """
        self._coeff  = np.array(coeff)
        self._symbol = symbol
        self._degree = len(coeff) - 1
    
    @property
    def coeff(self):
        return self._coeff
    @coeff.setter
    def coeff(self, value):
        if type(value) is list or type(value) is np.ndarray:
            self._coeff = value
            self._degree = len(value) - 1
        raise TypeError
    
    @property
    def degree(self):
        return self._degree
    
    @property
    def roots(self):
        return np.roots(self._coeff[::-1]) 

    # magic methods
    def __str__(self):
        s = ""
        for i in range(len(self._coeff)-1, -1, -1):
            if self._coeff[i] == 0:
                continue
            
            if i == 0:
                s += str(self._coeff[i])
            elif i == 1:
                s += str(self._coeff[i]) + self._symbol
            else:
                s += str(self._coeff[i]) + self._symbol + "^" + str(i)
                
            if i != 0:
                s += " + "
                
        return s
    
    def __call__(self, x):
        try:
            return np.array([self(i) for i in x])
        except:
            return np.sum(np.power(x, np.arange(0, self.degree+1)).dot(self._coeff))

    def __neg__(self):
        return Polynomial(-self._coeff)
    
    def __add__(self, other):
        if type(other) is Polynomial:
            if self.degree == other.degree:
                new_coeff = self.coeff + other.coeff
            elif self.degree > other.degree:
                new_coeff = self.coeff + np.pad(other.coeff, (0, self.degree - other.degree), 'constant')
            else:
                new_coeff = other.coeff + np.pad(self.coeff, (0, other.degree - self.degree), 'constant')
            
            return Polynomial(new_coeff)
        
        elif type(other) is int or type(other) is float:
            new_coeff = self.coeff[0] + other
            return Polynomial(new_coeff)
        
        raise TypeError
    
    def __sub__(self, other):
        if type(other) is Polynomial:
            if self.degree == other.degree:
                new_coeff = self.coeff - other.coeff
            elif self.degree > other.degree:
                new_coeff = self.coeff - np.pad(other.coeff, (0, self.degree - other.degree), 'constant')
            else:
                new_coeff = -other.coeff + np.pad(self.coeff, (0, other.degree - self.degree), 'constant')
            
            return Polynomial(new_coeff)
        
        elif type(other) is int or type(other) is float:
            new_coeff = self.coeff[0] - other
            return Polynomial(new_coeff)

        raise TypeError
    
    def __mul__(self, other):
        if type(other) is Polynomial:
            new_coeff = np.convolve(self.coeff, other.coeff)
            
            return Polynomial(new_coeff)
        
        elif type(other) is int or type(other) is float:
            new_coeff = other * self.coeff
            
            return Polynomial(new_coeff)
        raise TypeError
        
    def __eq__(self, other):
        if type(other) is Polynomial:
            return np.array_equal(self.coeff, other.coeff)
        return False
    
    
    # other methods
    def diff(self):
        """returns the derivative of the polynomial"""
        n = self._coeff.size
        return Polynomial(np.arange(1, n) * self._coeff[1:], self._symbol)
    
    def integrate(self, a=None, b=None):
        """
        Args:
            a (float): lower limit of integration
            b (float): upper limit of integration
            
        a and b are None -> antiderivative of the polynomial_
        """
        n = self._coeff.size
        if a is not None and b is not None:
            new_poly = Polynomial(np.append(0, self.coeff / np.arange(1, n+1)), self._symbol)
            return new_poly(b) - new_poly(a)
        else:
            return Polynomial(np.append("c", self.coeff / np.arange(1, n+1)), self._symbol)                    
    
        
    def plot(self, a=-10, b=10, n=101):
        x = np.linspace(a, b, n)
        y = np.array([self(i) for i in x])
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(x, y)
        
        ax.set_xlim(a, b)
        ax.set_xlabel(self._symbol)
        ax.set_ylabel("f(x)")
        ax.set_title(f"$f(x) = {self.__str__()}$")
        
        plt.show()