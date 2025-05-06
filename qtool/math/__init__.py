"""
Q_toolkit.math
==============

Provides:
    1. numerical methods for mathematical calculations
    2. tools for symbolic calculations
    3. tools for vector calculations

Submodules:
    base         : numerical methods for mathematical calculations
    de           : tools for differential equations
    polynomial   : tools for polynomial calculations
    vector       : tools for vector calculations
"""
import sys
sys.path.append(__file__[:-12])

from .base       import *
from .de         import *
from .polynomial import *
from .vector     import *
from .numerical  import *