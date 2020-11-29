"""
The components module includes the components functions to construct components stamps.
"""

from math import pi
from cmath import rect


def create_component_stamps(lines, matrix, vector, nodes_number, frequency=0):
    auxiliary_counter = 0
    auxiliary_elements = []

    for line in lines:
        line = line.split()

        if line[0][0].upper() == "R":
            print_resistor_stamp(int(line[1]), int(line[2]), float(line[3]), matrix)

        elif line[0][0].upper() == "V":
            auxiliary_counter += 1
            auxiliary_elements += [line[0]]
            if line[3].upper() == "DC":
                print_voltage_independent_source_DC_stamp(int(line[1]), int(line[2]), float(line[4]), 
                                                            nodes_number, auxiliary_counter, matrix, vector)
            elif line[3].upper() == "SIN":
                print_voltage_independent_source_SIN_stamp(int(line[1]), int(line[2]), line[4:],
                                                            nodes_number, auxiliary_counter, matrix, vector)

        elif line[0][0].upper() == "I":
            if line[3].upper() == "DC":
                print_current_independent_source_DC_stamp(int(line[1]), int(line[2]), float(line[4]), vector)
            elif line[3].upper() == "SIN":
                print_current_independent_source_SIN_stamp(int(line[1]), int(line[2]), line[4:], vector)

        elif line[0][0].upper() == "E":
            auxiliary_counter += 1
            auxiliary_elements += [line[0]]
            print_voltage_dependent_voltage_source_stamp(int(line[1]), int(line[2]), int(line[3]), int(line[4]),
                                                        float(line[5]), nodes_number, auxiliary_counter, matrix)

        elif line[0][0].upper() == "H":
            auxiliary_counter += 2
            auxiliary_elements += [line[0]]
            auxiliary_elements += ["Ix" + line[0]]
            print_current_dependent_voltage_source_stamp(int(line[1]), int(line[2]), int(line[3]), int(line[4]),
                                                        float(line[5]), nodes_number, auxiliary_counter, matrix)

        elif line[0][0].upper() == "G":
            print_voltage_dependent_current_source_stamp(int(line[1]), int(line[2]), int(line[3]), int(line[4]),
                                                        float(line[5]), matrix)

        elif line[0][0].upper() == "F":
            auxiliary_counter += 1
            auxiliary_elements += [line[0]]
            print_current_dependent_current_source_stamp(int(line[1]), int(line[2]), int(line[3]), int(line[4]),
                                                        float(line[5]), nodes_number, auxiliary_counter, matrix)

        elif line[0][0].upper() == "C":
            print_capacitor_sinusoidal_stamp(int(line[1]), int(line[2]), float(line[3]), frequency, matrix)

        elif line[0][0].upper() == "L":
            auxiliary_counter += 1
            auxiliary_elements += [line[0]]
            print_inductor_sinusoidal_stamp(int(line[1]), int(line[2]), float(line[3]), frequency, nodes_number, auxiliary_counter, matrix) 

        elif line[0][0].upper() == "K":
            nodeX = nodes_number + auxiliary_elements.index(line[1])
            nodeY = nodes_number + auxiliary_elements.index(line[2])
            print_mutual_inductance_sinusoidal_stamp(nodeX, nodeY, frequency, float(line[3]), matrix)

        elif line[0][0].upper() == "O":
            auxiliary_counter += 1
            auxiliary_elements += [line[0]]
            print_OpAmp_stamp(int(line[1]), int(line[2]), int(line[3]), int(line[4]), nodes_number, auxiliary_counter, matrix)

        else:
            pass
    
    return auxiliary_elements


def print_resistor_stamp(nodeA, nodeB, value, matrix):
    matrix[nodeA][nodeA] += 1/value
    matrix[nodeB][nodeB] += 1/value
    matrix[nodeA][nodeB] += -1/value
    matrix[nodeB][nodeA] += -1/value

    
def print_voltage_independent_source_DC_stamp(nodeA, nodeB, value, nodes_number, auxiliary_counter, matrix, vector):
    matrix[nodeA][nodes_number + auxiliary_counter] += +1
    matrix[nodeB][nodes_number + auxiliary_counter] += -1
    matrix[nodes_number + auxiliary_counter][nodeA] += -1
    matrix[nodes_number + auxiliary_counter][nodeB] += +1
    vector[nodes_number + auxiliary_counter] += -value

def print_voltage_independent_source_SIN_stamp(nodeA, nodeB, type_args, nodes_number, auxiliary_counter, matrix, vector):
    amplitude = float(type_args[1])
    frequency = float(type_args[2])
    angle = float(type_args[5])
    value = rect(amplitude, angle)
    matrix[nodeA][nodes_number + auxiliary_counter] += +1
    matrix[nodeB][nodes_number + auxiliary_counter] += -1
    matrix[nodes_number + auxiliary_counter][nodeA] += -1
    matrix[nodes_number + auxiliary_counter][nodeB] += +1
    vector[nodes_number + auxiliary_counter] += -value

        
def print_current_independent_source_DC_stamp(nodeA, nodeB, value, vector):
    vector[nodeA] += -value
    vector[nodeB] += +value

def print_current_independent_source_SIN_stamp(nodeA, nodeB, type_args, vector):
    amplitude = float(type_args[1])
    frequency = float(type_args[2])
    angle = float(type_args[5])
    value = rect(amplitude, angle)
    vector[nodeA] += -value
    vector[nodeB] += +value


def print_voltage_dependent_voltage_source_stamp(nodeA, nodeB, nodeC, nodeD, gain, nodes_number, auxiliary_counter, matrix):
    matrix[nodeA][nodes_number + auxiliary_counter] += +1
    matrix[nodeB][nodes_number + auxiliary_counter] += -1
    matrix[nodes_number + auxiliary_counter][nodeA] += -1
    matrix[nodes_number + auxiliary_counter][nodeB] += +1
    matrix[nodes_number + auxiliary_counter][nodeC] += +gain
    matrix[nodes_number + auxiliary_counter][nodeD] += -gain

    
def print_current_dependent_voltage_source_stamp(nodeA, nodeB, nodeC, nodeD, gain, nodes_number, auxiliary_counter, matrix):
    matrix[nodeA][nodes_number + auxiliary_counter] += +1
    matrix[nodeB][nodes_number + auxiliary_counter] += -1
    matrix[nodeC][nodes_number + auxiliary_counter - 1] += (+1 and not (matrix[nodeC][nodeD]))
    matrix[nodeD][nodes_number + auxiliary_counter - 1] += (-1 and not (matrix[nodeC][nodeD]))
    matrix[nodes_number + auxiliary_counter][nodeA] += -1
    matrix[nodes_number + auxiliary_counter][nodeB] += +1
    matrix[nodes_number + auxiliary_counter - 1][nodeC] += -1
    matrix[nodes_number + auxiliary_counter - 1][nodeD] += +1
    matrix[nodes_number + auxiliary_counter - 1][nodes_number + auxiliary_counter - 1] += -matrix[nodeC][nodeD]**(-1) if (matrix[nodeC][nodeD] != 0) else 0
    matrix[nodes_number + auxiliary_counter][nodes_number + auxiliary_counter - 1] += +gain

    
def print_voltage_dependent_current_source_stamp(nodeA, nodeB, nodeC, nodeD, gain, matrix):
    matrix[nodeA][nodeC] += +gain
    matrix[nodeA][nodeD] += -gain
    matrix[nodeB][nodeC] += -gain
    matrix[nodeB][nodeD] += +gain


def print_current_dependent_current_source_stamp(nodeA, nodeB, nodeC, nodeD, gain, nodes_number, auxiliary_counter, matrix):
    matrix[nodeA][nodes_number + auxiliary_counter] += +gain
    matrix[nodeB][nodes_number + auxiliary_counter] += -gain
    matrix[nodeC][nodes_number + auxiliary_counter] += (+1 and not (matrix[nodeC][nodeD]))
    matrix[nodeD][nodes_number + auxiliary_counter] += (-1 and not (matrix[nodeC][nodeD]))
    matrix[nodes_number + auxiliary_counter][nodeC] += -1
    matrix[nodes_number + auxiliary_counter][nodeD] += +1
    matrix[nodes_number + auxiliary_counter][nodes_number + auxiliary_counter] += -matrix[nodeC][nodeD]**(-1) if (matrix[nodeC][nodeD] != 0) else 0


def print_capacitor_sinusoidal_stamp(nodeA, nodeB, value, frequency, matrix, initial_condition=0):
    w = frequency * 2 * pi
    matrix[nodeA][nodeA] += (1j * w * value)
    matrix[nodeB][nodeB] += (1j * w * value)
    matrix[nodeA][nodeB] += (-1j * w * value)
    matrix[nodeB][nodeA] += (-1j * w * value)


def print_inductor_sinusoidal_stamp(nodeA, nodeB, value, frequency, nodes_number, auxiliary_counter, matrix, initial_condition=0):
    w = frequency * 2 * pi
    matrix[nodeA][nodes_number + auxiliary_counter] += 1
    matrix[nodeB][nodes_number + auxiliary_counter] += -1
    matrix[nodes_number + auxiliary_counter][nodeA] += -1
    matrix[nodes_number + auxiliary_counter][nodeB] += 1
    matrix[nodes_number + auxiliary_counter][nodes_number + auxiliary_counter] += (1j * w * value)


def print_mutual_inductance_sinusoidal_stamp(nodeX, nodeY, frequency, coefficient_of_coupling, matrix):
    w = frequency * 2 * pi
    matrix[nodeX][nodeY] += (1j * w * coefficient_of_coupling)
    matrix[nodeY][nodeX] += (1j * w * coefficient_of_coupling)


def print_OpAmp_stamp(nodeA, nodeB, nodeC, nodeD, nodes_number, auxiliary_counter, matrix):
    matrix[nodeA][nodes_number + auxiliary_counter] += 1
    matrix[nodeB][nodes_number + auxiliary_counter] += -1
    matrix[nodes_number + auxiliary_counter][nodeC] += 1
    matrix[nodes_number + auxiliary_counter][nodeD] += -1
