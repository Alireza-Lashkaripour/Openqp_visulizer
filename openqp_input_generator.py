# openqp_input_generator.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox

class OpenQPInputGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.template = """[input]
system=water.xyz
charge=0
runtype=energy
basis=6-31g(d)
functional=bhhlyp
method=tdhf

[guess]
type=huckel
save_mol=True

[scf]
multiplicity=3
type=rohf
save_molden=True

[tdhf]
type=mrsf
nstate=3
"""
        self.input_file_path = None

    def set_geometry_path(self, geometry_filename: str):
        """Set the path of the geometry file within the template."""
        self.geometry_filename = os.path.basename(geometry_filename)
        
    def generate_input_text(self, calc_type: str, geometry_filename: str):
        """Generate the input text with the relative system path."""
        input_content = self.template.replace("system=water.xyz", f"system={self.geometry_filename}")
        return input_content

    def generate_input_file(self, input_text: str, job_name: str):
        """Save input file to be used with OpenQP in Docker."""
        self.input_file_path = os.path.join(os.getcwd(), f"{job_name}.inp")
        with open(self.input_file_path, 'w') as file:
            file.write(input_text)
        return self.input_file_path

