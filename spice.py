"""
Author: Matheus Felinto
Description: A simple electronic circuit simulator
"""


import numpy as np

from lib.netlist import NetList
from lib import components


if __name__ == "__main__":
    netlist = NetList()
    netlist.read_netlist()

    N = netlist.define_matrix_range()
    conductance_matrix = np.zeros((N, N))
    print(conductance_matrix)
    if netlist.lines[-1] == ".op":
        # Resistive circuit analysis
        pass
    else:
        pass
