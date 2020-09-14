"""
The components module includes the components classes to construct components stamps.
"""


def create_component_stamps(lines, matrix, vector):
    for line in lines:
        line = line.split()

        if line[0][0] == "R":
            # Resistor
            resistor = Resistor(int(line[1]), int(line[2]), int(line[3]))
            resistor.print_stamp(matrix)

        elif line[0][0] == "V":
            # Voltage source
            pass

        elif line[0][0] == "I":
            # Current source
            current_source = CurrentIndependentSource(int(line[1]), int(line[2]), int(line[3]))
            current_source.print_stamp(vector)

        elif line[0][0] == "A":
            # Voltage dependent voltage source
            pass

        elif line[0][0] == "H":
            # Current dependent voltage source
            pass

        elif line[0][0] == "G":
            # Voltage dependent current source
            pass

        elif line[0][0] == "B":
            # Current dependent current source
            pass

        elif line[0][0] == "C":
            # Capacitor
            pass

        elif line[0][0] == "L":
            # Inductor
            pass

        elif line[0][0] == "T":
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
        if self.nodeA == 0:
            matrix[self.nodeB - 1][self.nodeB - 1] += 1/self.value
        elif self.nodeB == 0:
            matrix[self.nodeA - 1][self.nodeA - 1] += 1/self.value
        else:
            matrix[self.nodeA - 1][self.nodeA - 1] += 1/self.value
            matrix[self.nodeB - 1][self.nodeB - 1] += 1/self.value
            matrix[self.nodeA - 1][self.nodeB - 1] += -1/self.value
            matrix[self.nodeB - 1][self.nodeA - 1] += -1/self.value


class VoltageIndependentSource:
    def __init__(self, nodeA, nodeB, value):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.value = value


class CurrentIndependentSource:
    def __init__(self, nodeA, nodeB, value):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.value = value

    def print_stamp(self, vector):
        if self.nodeA == 0:
            vector[self.nodeB - 1] = -self.value
        elif self.nodeB == 0:
            vector[self.nodeA - 1] = +self.value
        else:
            vector[self.nodeA - 1] = self.value
            vector[self.nodeB - 1] = -self.value
            

class VoltageDependentVoltageSource:
    pass

class CurrentDependentVoltageSource:
    pass

class VoltageDependentCurrentSource:
    pass

class CurrentDependentCurrentSource:
    pass
