# Class Vector 
# ==================================================
import numpy                as np
import matplotlib.pyplot    as plt
from   math                 import pi, sin, cos, sqrt
# ==================================================

class Vector(object):
    """2D Vector
    arg*: x, y or vector
    """
    def __init__(self, *args):
        if len(args) == 2:
            self._x = float(args[0])
            self._y = float(args[1])
        elif len(args) == 1 and isinstance(args[0], Vector):
            other = args[0]
            self._x = other._x
            self._y = other._y
        else:
            raise TypeError('Invalid arguments for Vector()')

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    
    @property
    def pos(self):
        return (self._x, self._y)
    @pos.setter
    def pos(self, value: tuple):
        self._x = value[0]
        self._y = value[1]
    
    @property
    def magnitude(self):
        return sqrt(self._x**2 + self._y**2)
    @magnitude.setter
    def magnitude(self, value):
        mag = self.magnitude
        if mag == 0:
            return
        self._x = value * self._x / mag
        self._y = value * self._y / mag
    
    @property
    def angle(self):
        return np.arctan2(self._y, self._x)
    @angle.setter
    def angle(self, value):
        mag = self.magnitude
        self._x = mag * cos(value)
        self._y = mag * sin(value)
    
    @property
    def hat(self):
        mag = self.magnitude
        return Vector(self._x / mag, self._y / mag)

    def __str__(self):
        return '<{:.6g}, {:.6g}>'.format(self._x, self._y)
    
    def __neg__(self):
        return Vector(-self._x, -self._y,)
    
    def __add__(self, other):
        if type(other) is Vector:
            return Vector(self._x + other._x, self._y + other._y)
        raise TypeError
        
    def __sub__(self, other):
        if type(other) is Vector:
            return Vector(self._x - other._x, self._y - other._y)
        raise TypeError
    
    def __eq__(self, other):
        if type(self) is Vector and type(other) is Vector:
            return self._x == other._x and self._y == other._y
        raise TypeError
    
    def dot(self, other):
        if type(other) is Vector:
            return self._x * other._x + self._y * other._y
        raise TypeError

    def cross(self, other):
        if type(other) is Vector:
            return self._x * other._y - self._y * other._x
        raise TypeError
    
# ==================================================    
# static methods
def dot(v1, v2):
    if type(v1) is Vector and type(v2) is Vector:
        return v1.dot(v2)
    raise TypeError

def cross(v1, v2):
    if type(v1) is Vector and type(v2) is Vector:
        return v1.cross(v2)
    raise TypeError

def angle(v1, v2):
    if type(v1) is Vector and type(v2) is Vector:
        return v2.angle - v1.angle
    raise TypeError

# ==================================================

def main():
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11, 2))
    plt.yticks(np.arange(-10, 11, 2))
    plt.grid()
    
    v1 = Vector(7, 4)
    v2 = Vector(-4, 2)
    print(v1 + v2)
    print(v1.dot(v2))    
    plt.quiver(0, 0, v1.x, v1.y, color='r', scale=1, angles='xy', scale_units='xy')
    plt.quiver(0, 0, v2.x, v2.y, color='b', scale=1, angles='xy', scale_units='xy')
    return None

# ==================================================
if __name__ == '__main__':
    main()