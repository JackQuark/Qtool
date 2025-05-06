# _summary_
# ==================================================
import sys
import os
import numpy     as np
import matplotlib.pyplot  as plt

from matplotlib.axes import Axes

import metpy.calc as mpcalc
import metpy.units as mpunit
import metpy.plots as mpplt
# ==================================================

class SkewAxes(Axes):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skew_angle = 30
        self.skew_ax = self.inset_axes([0.5, 0.5, 0.4, 0.4], transform=self.transAxes)
        self.skew_ax.set_xlim(0, 1)
        self.skew_ax.set_ylim(0, 1)
        self.skew_ax.set_xticks([])
        self.skew_ax.set_yticks([])
        self.skew_ax.set_aspect('equal')
        self.plot_skew()

    def plot_skew(self):
        theta = np.deg2rad(self.skew_angle)
        x = np.array([0, 1])
        y = np.array([0, 1/np.tan(theta)])
        self.skew_ax.plot(x, y, 'k-')



class SkewT(object):
    def __init__(self):
        pass
    
# ==================================================

def main():
    
    fig = plt.figure(figsize=(6, 6))
    ax  = fig.add_subplot(111)
    
    pass

# ==================================================
from time import perf_counter
if __name__ == '__main__':
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print('\ntime :%.3f ms' %((end_time - start_time)*1000))
