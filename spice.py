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

    equations_number = netlist.define_matrix_range()
    nodes_number = equations_number[0]
    auxiliary_equations_number = equations_number[1]

    N = nodes_number + auxiliary_equations_number
    admittance_matrix = np.zeros((N, N))
    current_vector = np.zeros(N)

    components.create_component_stamps(netlist.lines, admittance_matrix, current_vector, nodes_number)

    print(admittance_matrix)
    print(current_vector)

    nodes_voltage = np.linalg.solve(admittance_matrix, current_vector)

    print("The voltage values are: ", nodes_voltage)