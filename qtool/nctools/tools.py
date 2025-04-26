# nc tools 
# by Quark
# ==================================================
import os
import sys
import numpy              as np
import netCDF4            as nc
from   concurrent.futures import ProcessPoolExecutor
# ==================================================

class Info(object):
    """Information about a netCDF file.
    """
    def __init__(self, filename):
        self.filename = filename
        self.rootgrp  = nc.Dataset(filename, 'r')
    
    def __str__(self):
        info_str = f"{self.filename}:\n"
        # dimensions info
        info_str += "=== Dimensions (size) ===\n"
        for key in self.rootgrp.dimensions.keys():
            info_str += f"{key} ({self.rootgrp.dimensions[key].size})\n"
        # variables info
        info_str += "=== Variables (dimensions) ===\n"
        for key in self.rootgrp.variables.keys():
            info_str += f"{key} {self.rootgrp.variables[key].dimensions}\n"

        return info_str
    
class Converter(object):
    """Create a new netCDF converted from a given netCDF file.
    """
    def __init__(self, new_filename, **kwargs):
        pass

                   
# ==================================================
def main():
    print(Info('test.nc'))
    
    return 0
# ==================================================
if __name__ == '__main__':
    main()