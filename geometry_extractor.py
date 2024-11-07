import re
from pathlib import Path

class GeometryExtractor:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def extract_optimized_geometry(self):
        geometry_data = []
        found_geometry = False
        
        try:
            with open(self.log_file_path, 'r') as file:
                lines = file.readlines()

            for i in range(len(lines)-1, -1, -1):
                line = lines[i]
                if "PyOQP: Geometry Optimization Step" in line:
                    found_geometry = True
                    break

            if not found_geometry:
                raise ValueError("Optimized geometry not found in log file.")

            for j in range(i, len(lines)):
                line = lines[j]
                if "Cartesian Coordinate in Angstrom" in line:
                    j += 2
                    while j < len(lines) and lines[j].strip():
                        if "ATOM" in lines[j] or "ZNUC" in lines[j]:
                            j += 1
                            continue
                        geometry_data.append(lines[j].strip())
                        j += 1
                    break

            xyz_data = self.convert_to_xyz(geometry_data)
            return xyz_data

        except Exception as e:
            raise ValueError(f"Failed to extract geometry: {e}")

    def convert_to_xyz(self, geometry_data):
        atom_lines = [line for line in geometry_data if len(line.split()) >= 5]
        atom_count = len(atom_lines)
        xyz_content = [f"{atom_count}", "Optimized Geometry"]

        for line in atom_lines:
            parts = line.split()
            if len(parts) >= 5:
                element = self.get_element_symbol(float(parts[1]))
                x, y, z = map(float, parts[2:5])
                xyz_content.append(f"{element:<2} {x:>10.6f} {y:>10.6f} {z:>10.6f}")
        
        return "\n".join(xyz_content)

    def get_element_symbol(self, atomic_number):
        periodic_table = {
            1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne',
            11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca',
            21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn',
            31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr',
            41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn',
            51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd',
            61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd'
        }
        return periodic_table.get(int(atomic_number), "X")

    def save_optimized_geometry(self, job_name):
        xyz_data = self.extract_optimized_geometry()
        file_name = f"{job_name}_opt_geo.xyz"
        save_path = Path(file_name)
        
        with open(save_path, 'w') as xyz_file:
            xyz_file.write(xyz_data)
        
        return save_path
