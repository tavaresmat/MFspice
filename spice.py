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

    if netlist.lines[-1].split()[0].upper() == ".DC":
        print("The voltage values are: \n", nodes_voltage)
        for i in range(1, len(nodes_voltage) + 1):
            print(f"nó ({i}) = {nodes_voltage[i - 1]}")
    elif netlist.lines[-1].split()[0].upper() == ".SIN":
        print("The voltage values are: \n", nodes_voltage)
        for i in range(1, len(nodes_voltage) + 1):
            print(f"nó ({i}) = {nodes_voltage[i - 1].real} Cos({frequency}t) + {-nodes_voltage[i - 1].imag} Sin({frequency}t)")
