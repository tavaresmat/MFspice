"""
The netlist module includes the netlist class to work with the netlist file informations.
"""


class NetList:
    def __init__(self, name="netlist.txt"):
        self.name = name
        self.lines = []
    
    def read_netlist(self):
        """
        -> The method reads the netlist file with the argument name and updates the list with the netlist file lines.
        """
        netlist_file = open(self.name, "r")
        for line in netlist_file:
            self.lines += [line]
        netlist_file.close()
    
    def define_matrix_range(self):
        """
        -> The method analyses the netlist lines and returns the dimension of the Yn matrix.
        :return: the number of nodes and auxiliary equations needed to solve a Yn matrix. 
        """
        nodes = 0
        auxiliary = 0
        for element in self.lines:
            if element[0] == ".":
                # The dot is the last value in the netlist and represents the operation mode.
                break
            if element[0] in "VEF":
                # These Leters represent components that need an auxiliary equation.
                auxiliary += 1
            
            values = element.split()

            if (int(values[1]) > nodes) or (int(values[2]) > nodes):
                # values[1] and values[2] are the positions for component's nodes.
                nodes = int(max(values[1], values[2]))

        return [nodes, auxiliary]
