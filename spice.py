"""
Author: Matheus Felinto
Description: A simple electronic circuit simulator
"""


import numpy as np
import sympy as sp
from sympy.abc import s, t
from sympy.integrals import laplace_transform, inverse_laplace_transform 

from lib.netlist import NetList
from lib import components


if __name__ == "__main__":
    netlist = NetList()
    netlist.read_netlist()

    nodes_number, auxiliary_equations_number = netlist.define_matrix_range() 

    N = nodes_number + auxiliary_equations_number
    admittance_matrix = np.zeros((N, N), dtype=complex)
    current_vector = np.zeros(N, dtype=complex)

    frequency = 0
    if netlist.lines[-1].split()[0].upper() == ".SIN":
        frequency = float(netlist.lines[-1].split()[1])
    components.create_component_stamps(netlist.lines, admittance_matrix, current_vector, nodes_number, frequency)

    print(admittance_matrix)
    print(current_vector)

    nodes_voltage = np.linalg.solve(admittance_matrix, current_vector)

    print("""
 _____ _                 _                _ _                _                 
|_   _| |__   ___    ___(_)_ __ ___ _   _(_) |_  __   ____ _| |_   _  ___  ___ 
  | | | '_ \ / _ \  / __| | '__/ __| | | | | __| \ \ / / _` | | | | |/ _ \/ __|
  | | | | | |  __/ | (__| | | | (__| |_| | | |_   \ V / (_| | | |_| |  __/\__ \\
  |_| |_| |_|\___|  \___|_|_|  \___|\__,_|_|\__|   \_/ \__,_|_|\__,_|\___||___/
                                                                               
                  
  __ _ _ __ ___ _ 
 / _` | '__/ _ (_)
| (_| | | |  __/_ 
 \__,_|_|  \___(_)
 """)

    if netlist.lines[-1].split()[0].upper() == ".DC":
        for index in range(1, len(nodes_voltage) + 1):
            print(f"{'node' if index <= nodes_number else 'current'} ({index}) = {nodes_voltage[index - 1]:.3f}")

    elif netlist.lines[-1].split()[0].upper() == ".SIN":
        for index in range(1, len(nodes_voltage) + 1):
            print(f"{'node' if index <= nodes_number else 'current'} ({index}) = {nodes_voltage[index - 1].real:.3f} Cos({frequency}t) + {-nodes_voltage[index - 1].imag:.3f} Sin({frequency}t)")
