# MFSPICE

MFSPICE is a simple electronic circuit simulator for Electric Circuits II course.
From a list that describes a circuit (NETLIST), the program can predict the node voltage values.

---

## Usage

```bash
python3 spice.py <netlist_file_name>
```

Circuit and NetList for circuit example:

![Circuit example picture]("/images/circuit_example.png")

>R1 1 2 2
R2 2 0 4
R3 2 3 8
R4 1 3 4
I1 0 1 DC 3
F1 3 0 1 2 2
>.DC

**Obs**: The program uses [numpy](https://numpy.org/) lib for calculations.

---

## General instructions

Components format for NETLIST:

![Component models]("/images/Components.png")
![AmpOp model]("/images/AmpOp.png")

- **Voltage Source**:   V<name> <a(node+)> <b(node-)> <source_type>
- **Current Source**:   I<name> <a(node+)> <b(node-)> <source_type>
- **Resistor**:  R<name> <a(node+)> <b(node-)> <R(resistence)>
- **Capacitor**: C<name> <a(node+)> <b(node-)> <C(capacitance)>
- **Indutor**:   L<name> <a(node+)> <b(node-)> <L(inductance)>
- **Mutual Inductance**: K<name> <inductor_1_name> <inductor_2_name> <M(coupling_coefficient)>
- **Voltage Controlled Current Source**: G<name> <a(output_node+)> <b(output_node-)> <c(reference_node+)> <d(reference_node-)> <Gm(gain)>
- **Voltage Controlled Voltage Source**: E<name> <a(output_node+)> <b(output_node-)> <c(reference_node+)> <d(reference_node-)> <Av(gain)>
- **Current Controlled Current Source**: F<name> <a(output_node+)> <b(output_node-)> <c(reference_node+)> <d(reference_node-)> <Bi(gain)>
- **Current Controlled Voltage Source**: H<name> <a(output_node+)> <b(output_node-)> <c(reference_node+)> <d(reference_node-)> <Rm(gain)>
- **Amp. op.**:  O<name> <a(output_node+)> <b(output_node-)> <c(input_node+)> <d(input_node-)>
- _**Source types**_:
    - DC <Value>
    - SIN <DC_level> <Amplitude> <Frequency> <Delay> <Attenuation> <Angle> <Cicles>

The last line in the Netlist file has one of these formats:

>.DC

or

>.SIN <frequency>


**OBS:** Currently the program only supports one frequency per circuit, so if it is not a DC circuit the frequency used is passed in the last line.

**OBS_2:** The order of the components in the netlist must be:
1. passive components(resistors, capacitors and inductors)
2. independent sources and AmpOps
3. current controlled sources
4. voltage controlled sources

---

## Possible future implementations

- multi-frequency compatible (implement superposition)
- literal resolutions
- graphical user interface
- ~~stories (share the circuit you're working with your friends)~~ just kidding

---

## References

- Queiroz, A.C.M. (2019). "Circuitos elétricos, métodos de análise e introdução à sintese".
- Alexander, C.K. and Sadiku, M.N.O. (2007). "Fundamentals of electric circuits".