# results_viewer.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import webbrowser
import py3Dmol

class ResultsViewer:
    def __init__(self, parent):
        self.parent = parent

    def show_results(self):
        """Main function to display options for viewing results."""
        results_window = tk.Toplevel(self.parent)
        results_window.title("Results Viewer")

        # Buttons for Log File and Molecular Orbital Visualization
        tk.Button(results_window, text="Open Log File", command=self.open_log_file).pack(pady=5)
        tk.Button(results_window, text="Visualize Molecular Orbitals", command=self.visualize_molecular_orbitals).pack(pady=5)

    def open_log_file(self):
        """Open and display the contents of a selected log file."""
        log_file_path = filedialog.askopenfilename(filetypes=[("Log files", "*.log")])
        
        if not log_file_path or not os.path.exists(log_file_path):
            messagebox.showwarning("Warning", "Log file not found.")
            return

        log_window = tk.Toplevel(self.parent)
        log_window.title("Log File Viewer")

        log_text = scrolledtext.ScrolledText(log_window, wrap="word", width=80, height=20)
        log_text.pack(padx=10, pady=10, expand=True, fill="both")

        with open(log_file_path, 'r') as log_file:
            log_text.insert(tk.END, log_file.read())

    def visualize_molecular_orbitals(self):
        """Visualize molecular orbitals using a Cube file generated from the Molden data."""
        # Select XYZ file for structure and Cube file for MO data
        xyz_file_path = filedialog.askopenfilename(filetypes=[("XYZ files", "*.xyz")])
        cube_file_path = filedialog.askopenfilename(filetypes=[("Cube files", "*.cube")])

        if not xyz_file_path or not os.path.exists(xyz_file_path):
            messagebox.showwarning("Warning", "XYZ file not found.")
            return
        if not cube_file_path or not os.path.exists(cube_file_path):
            messagebox.showwarning("Warning", "Cube file not found.")
            return

        # Load XYZ data for molecular structure
        with open(xyz_file_path, 'r') as xyz_file:
            xyz_data = xyz_file.read()

        # Load Cube data for MO visualization
        with open(cube_file_path, 'r') as cube_file:
            cube_data = cube_file.read()

        # Set up Py3Dmol viewer in a new window
        viewer_window = tk.Toplevel(self.parent)
        viewer_window.title("Molecular Orbital Visualization")

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
        </head>
        <body>
            <div id="viewer" style="width: 100%; height: 100vh;"></div>
            <script>
                const viewer = $3Dmol.createViewer("viewer", {{backgroundColor: "white"}});
                viewer.addModel(`{xyz_data}`, "xyz");
                viewer.setStyle({{"stick":{{}}}});
                viewer.addVolumetricData(`{cube_data}`, "cube", {{isoval: 0.02, color: "blue"}});
                viewer.zoomTo();
                viewer.render();
            </script>
        </body>
        </html>
        """

        # Save the HTML to a temporary file and open in the default web browser
        html_file_path = os.path.join(os.getcwd(), "molecular_orbitals_viewer.html")
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_content)

        webbrowser.open(f"file://{html_file_path}")

