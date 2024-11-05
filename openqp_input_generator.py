
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class OpenQPInputGenerator:
    def __init__(self, parent):
        self.parent = parent
        
        #  templates for each calculation type
        self.templates = {
            "DFT Energy": """[input]
system=water.xyz
charge=0
functional=bhhlyp
basis=3-21g
method=hf
runtype=energy

[guess]
type=huckel
save_mol=True

[scf]
multiplicity=1
type=rhf
save_molden=True

""",
            "DFT Geometry Optimization": """[input]
system=water.xyz
charge=0
functional=bhhlyp
basis=3-21g
runtype=optimize
method=hf

[guess]
type=huckel
save_mol=True

[scf]
type=rhf
multiplicity=1
save_molden=True

[optimize]
istate=0
""",
            "MRSF-TDDFT Ground State Energy": """[input]
system=water.xyz
charge=0
runtype=energy
basis=3-21g
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
nstate=1
""",
            "MRSF-TDDFT First Excited State Energy": """[input]
system=water.xyz
charge=0
runtype=energy
basis=3-21g
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
nstate=2
""",
            "MRSF-TDDFT Ground State Geometry Optimization": """[input]
system=water.xyz
charge=0
runtype=optimize
basis=3-21g
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

[optimize]
istate=1
""",
            "MRSF-TDDFT First Excited State Geometry Optimization": """[input]
system=water.xyz
charge=0
runtype=optimize
basis=3-21g
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

[optimize]
istate=2
"""
        }
        self.input_file_path = None

    def set_geometry_path(self, geometry_filename: str):
        """Set the path of the geometry file within the template."""
        self.geometry_filename = os.path.basename(geometry_filename)
        
    def generate_input_text(self, calc_type: str, geometry_filename: str):
        """Generate the input text based on the selected calculation type."""
        template = self.templates.get(calc_type, "")
        input_content = template.replace("system=water.xyz", f"system={self.geometry_filename}")
        return input_content

    def generate_input_file(self, input_text: str, job_name: str):
        """Save input file to be used with OpenQP in Docker."""
        self.input_file_path = os.path.join(os.getcwd(), f"{job_name}.inp")
        with open(self.input_file_path, 'w') as file:
            file.write(input_text)
        return self.input_file_path

