"""
The components module includes the components classes to construct components stamps.
"""

from math import pi
from cmath import rect
import sympy as sp
from sympy.abc import s, t
from sympy.integrals import laplace_transform, inverse_laplace_transform


def create_component_stamps(lines, matrix, vector, nodes_number, frequency=0):
    auxiliary_counter = 0
    
    for line in lines:
        line = line.split()

        if line[0][0].upper() == "R":
            resistor = Resistor(int(line[1]), int(line[2]), float(line[3]))
            resistor.print_stamp(matrix)

        elif line[0][0].upper() == "V":
            auxiliary_counter += 1
            voltage_source = VoltageIndependentSource(int(line[1]), int(line[2]), line[3], line[4:], 
                                                        nodes_number, auxiliary_counter)
            if voltage_source.type.upper() == "DC":
                voltage_source.print_DC_stamp(matrix, vector)
            elif voltage_source.type.upper() == "SIN":
                voltage_source.print_SIN_stamp(matrix, vector)

        elif line[0][0].upper() == "I":
            current_source = CurrentIndependentSource(int(line[1]), int(line[2]), line[3], line[4:])
            if current_source.type.upper() == "DC":
                current_source.print_DC_stamp(vector)
            elif current_source.type.upper() == "SIN":
                current_source.print_SIN_stamp(vector)

        elif line[0][0].upper() == "E":
            auxiliary_counter += 1
            voltage_dependent_voltage_source = VoltageDependentVoltageSource(int(line[1]), int(line[2]), int(line[3]), int(line[4]),
                                                                            float(line[5]), nodes_number, auxiliary_counter)
            voltage_dependent_voltage_source.print_stamp(matrix)

        elif line[0][0].upper() == "H":
            auxiliary_counter += 2
            current_dependent_voltage_source = CurrentDependentVoltageSource(int(line[1]), int(line[2]), int(line[3]), int(line[4]),
                                                                            float(line[5]), nodes_number, auxiliary_counter)
            current_dependent_voltage_source.print_stamp(matrix)

        elif line[0][0].upper() == "G":
            voltage_dependent_current_source = VoltageDependentCurrentSource(int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5]))
            voltage_dependent_current_source.print_stamp(matrix)

        elif line[0][0].upper() == "F":
            auxiliary_counter += 1
            current_dependent_current_source = CurrentDependentCurrentSource(int(line[1]), int(line[2]), int(line[3]), int(line[4]),
                                                                            float(line[5]), nodes_number, auxiliary_counter)
            current_dependent_current_source.print_stamp(matrix)

        elif line[0][0].upper() == "C":
            if frequency != 0:
                capacitor = Capacitor(int(line[1]), int(line[2]), float(line[3]), frequency)
                capacitor.print_sinusoidal_stamp(matrix)

        elif line[0][0].upper() == "L":
            auxiliary_counter += 1
            inductor = Inductor(int(line[1]), int(line[2]), float(line[3]), frequency, nodes_number, auxiliary_counter)
            inductor.print_sinusoidal_stamp(matrix) 

        elif line[0][0].upper() == "T":
            # Transformer
            pass

        else:
            pass


class Resistor:
    def __init__(self, nodeA, nodeB, value):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.value = value
    
    def print_stamp(self, matrix):
        matrix[self.nodeA - 1][self.nodeA - 1] += (1/self.value) * (self.nodeA != 0)
        matrix[self.nodeB - 1][self.nodeB - 1] += (1/self.value) * (self.nodeB != 0)
        matrix[self.nodeA - 1][self.nodeB - 1] += (-1/self.value) * ((self.nodeA != 0) and (self.nodeB != 0))
        matrix[self.nodeB - 1][self.nodeA - 1] += (-1/self.value) * ((self.nodeA != 0) and (self.nodeB != 0))


class VoltageIndependentSource:
    def __init__(self, nodeA, nodeB, signal_type, type_args, nodes_number, auxiliary_counter):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.type = signal_type
        self.type_args = type_args
        self.nodes_number = nodes_number
        self.auxiliary_counter = auxiliary_counter
    
    def print_DC_stamp(self, matrix, vector):
        self.value = float(self.type_args[0])
        matrix[self.nodeA - 1][self.nodes_number + self.auxiliary_counter - 1] += +1 * (self.nodeA != 0)
        matrix[self.nodeB - 1][self.nodes_number + self.auxiliary_counter - 1] += -1 * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeA - 1] += -1 * (self.nodeA != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeB - 1] += +1 * (self.nodeB != 0)
        vector[self.nodes_number + self.auxiliary_counter -1] += -self.value

    def print_SIN_stamp(self, matrix, vector):
        self.amplitude = float(self.type_args[1])
        self.frequency = float(self.type_args[2])
        self.angle = float(self.type_args[5])
        self.value = rect(self.amplitude, self.angle)
        matrix[self.nodeA - 1][self.nodes_number + self.auxiliary_counter - 1] += +1 * (self.nodeA != 0)
        matrix[self.nodeB - 1][self.nodes_number + self.auxiliary_counter - 1] += -1 * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeA - 1] += -1 * (self.nodeA != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeB - 1] += +1 * (self.nodeB != 0)
        vector[self.nodes_number + self.auxiliary_counter -1] += -self.value

        
class CurrentIndependentSource:
    def __init__(self, nodeA, nodeB, signal_type, type_args):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.type = signal_type
        self.type_args = type_args

    def print_DC_stamp(self, vector):
        self.value = float(self.type_args[0])
        vector[self.nodeA - 1] += -self.value * (self.nodeA != 0)
        vector[self.nodeB - 1] += +self.value * (self.nodeB != 0)
    
    def print_SIN_stamp(self, vector):
        self.amplitude = float(self.type_args[1])
        self.frequency = float(self.type_args[2])
        self.angle = float(self.type_args[5])
        self.value = rect(self.amplitude, self.angle)
        vector[self.nodeA - 1] += -self.value * (self.nodeA != 0)
        vector[self.nodeB - 1] += +self.value * (self.nodeB != 0)


class VoltageDependentVoltageSource:
    def __init__(self, nodeA, nodeB, nodeC, nodeD, gain, nodes_number, auxiliary_counter):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.nodeC = nodeC
        self.nodeD = nodeD
        self.gain = gain
        self.nodes_number = nodes_number
        self.auxiliary_counter = auxiliary_counter

    def print_stamp(self, matrix):
        matrix[self.nodeA - 1][self.nodes_number + self.auxiliary_counter - 1] += +1 * (self.nodeA != 0)
        matrix[self.nodeB - 1][self.nodes_number + self.auxiliary_counter - 1] += -1 * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeA - 1] += -1 * (self.nodeA != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeB - 1] += +1 * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeC - 1] += +self.gain * (self.nodeC != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeD - 1] += -self.gain * (self.nodeD != 0)


class CurrentDependentVoltageSource:
    def __init__(self, nodeA, nodeB, nodeC, nodeD, gain, nodes_number, auxiliary_counter):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.nodeC = nodeC
        self.nodeD = nodeD
        self.gain = gain
        self.nodes_number = nodes_number
        self.auxiliary_counter = auxiliary_counter
    
    def print_stamp(self, matrix):
        matrix[self.nodeA - 1][self.nodes_number + self.auxiliary_counter - 1] += +1 * (self.nodeA != 0)
        matrix[self.nodeB - 1][self.nodes_number + self.auxiliary_counter - 1] += -1 * (self.nodeB != 0)
        matrix[self.nodeC - 1][self.nodes_number + self.auxiliary_counter - 2] += +1 * (self.nodeC != 0)
        matrix[self.nodeD - 1][self.nodes_number + self.auxiliary_counter - 2] += -1 * (self.nodeD != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeA - 1] += -1 * (self.nodeA != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeB - 1] += +1 * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter -2][self.nodeC - 1] += -1 * (self.nodeC != 0)
        matrix[self.nodes_number + self.auxiliary_counter -2][self.nodeD - 1] += +1 * (self.nodeD != 0)
        matrix[self.nodes_number + self.auxiliary_counter - 2][self.nodes_number + self.auxiliary_counter - 2] += (((self.nodeC != 0) and (self.nodeD != 0)) and
                                                                                                                (matrix[self.nodeC - 1][self.nodeD - 1])**(-1))
        matrix[self.nodes_number + self.auxiliary_counter - 1][self.nodes_number + self.auxiliary_counter - 2] += +self.gain


class VoltageDependentCurrentSource:
    def __init__(self, nodeA, nodeB, nodeC, nodeD, gain):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.nodeC = nodeC
        self.nodeD = nodeD
        self.gain = gain
    
    def print_stamp(self, matrix):
        matrix[self.nodeA - 1][self.nodeC - 1] += +self.gain * ((self.nodeA != 0) and (self.nodeC != 0))
        matrix[self.nodeA - 1][self.nodeD - 1] += -self.gain * ((self.nodeA != 0) and (self.nodeD != 0))
        matrix[self.nodeB - 1][self.nodeC - 1] += -self.gain * ((self.nodeB != 0) and (self.nodeC != 0))
        matrix[self.nodeB - 1][self.nodeD - 1] += +self.gain * ((self.nodeB != 0) and (self.nodeD != 0))

class CurrentDependentCurrentSource:
    def __init__(self, nodeA, nodeB, nodeC, nodeD, gain, nodes_number, auxiliary_counter):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.nodeC = nodeC
        self.nodeD = nodeD
        self.gain = gain
        self.nodes_number = nodes_number
        self.auxiliary_counter = auxiliary_counter
    
    def print_stamp(self, matrix):
        matrix[self.nodeA - 1][self.nodes_number + self.auxiliary_counter - 1] += +self.gain * (self.nodeA != 0)
        matrix[self.nodeB - 1][self.nodes_number + self.auxiliary_counter - 1] += -self.gain * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeC - 1] += -1 * (self.nodeC != 0)
        matrix[self.nodes_number + self.auxiliary_counter -1][self.nodeD - 1] += +1 * (self.nodeD != 0)
        matrix[self.nodeC - 1][self.nodes_number + self.auxiliary_counter - 1] += +1 * (self.nodeC != 0)
        matrix[self.nodeD - 1][self.nodes_number + self.auxiliary_counter - 1] += -1 * (self.nodeD != 0)
        matrix[self.nodes_number + self.auxiliary_counter - 1][self.nodes_number + self.auxiliary_counter - 1] += (((self.nodeB != 0) and (self.nodeC != 0)) and
                                                                                                                (matrix[self.nodeC - 1][self.nodeD - 1])**(-1))


class Capacitor:
    def __init__(self, nodeA, nodeB, value, frequency, initial_condition=0):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.value = value
        self.w = frequency * 2 * pi
        self.initial_condition = initial_condition

    def print_sinusoidal_stamp(self, matrix):
        matrix[self.nodeA - 1][self.nodeA - 1] += (1j * self.w * self.value) * (self.nodeA != 0)
        matrix[self.nodeB - 1][self.nodeB - 1] += (1j * self.w * self.value) * (self.nodeB != 0)
        matrix[self.nodeA - 1][self.nodeB - 1] += (-1j * self.w * self.value) * ((self.nodeA != 0) and (self.nodeB != 0))
        matrix[self.nodeB - 1][self.nodeA - 1] += (-1j * self.w * self.value) * ((self.nodeA != 0) and (self.nodeB != 0))


class Inductor:
    def __init__(self, nodeA, nodeB, value, frequency, nodes_number, auxiliary_counter, initial_condition=0):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.value = value
        self.w = frequency * 2 * pi
        self.nodes_number = nodes_number
        self.auxiliary_counter = auxiliary_counter
        self.initial_condition = initial_condition

    def print_sinusoidal_stamp(self, matrix):
        matrix[self.nodeA -1][self.nodes_number + self.auxiliary_counter - 1] += 1 * (self.nodeA != 0)
        matrix[self.nodeB -1][self.nodes_number + self.auxiliary_counter - 1] += -1 * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter - 1][self.nodeA -1] += -1 * (self.nodeA != 0)
        matrix[self.nodes_number + self.auxiliary_counter - 1][self.nodeB -1] += 1 * (self.nodeB != 0)
        matrix[self.nodes_number + self.auxiliary_counter - 1][self.nodes_number + self.auxiliary_counter - 1] += (1j * self.w * self.value)
