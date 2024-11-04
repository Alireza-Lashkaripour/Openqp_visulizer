import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
import json

class MoleculeVisualizer:
    def __init__(self, parent):
        """Initialize the MoleculeVisualizer with a parent window."""
        self.parent = parent
        self.file_path = None
        self.js_url = "https://3Dmol.org/build/3Dmol-min.js"
        
    def set_geometry_path(self, path):
        """Set the path of the geometry file to visualize."""
        if not path:
            raise ValueError("Path cannot be None or empty")
            
        if os.path.isfile(path):
            self.file_path = path
        else:
            raise FileNotFoundError(f"File not found: {path}")
            
    def _read_xyz_file(self):
        """Read and validate the XYZ file contents."""
        if not self.file_path:
            raise ValueError("No geometry file selected for visualization")
            
        try:
            with open(self.file_path, 'r') as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Failed to read file: {str(e)}")
            
    def _generate_html(self, xyz_data):
        """Generate the HTML content for visualization."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="{self.js_url}"></script>
            <style>
                #viewer_container {{
                    width: 100%;
                    height: 100vh;
                    position: relative;
                }}
            </style>
        </head>
        <body>
            <div id="viewer_container"></div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    let viewer = $3Dmol.createViewer(
                        document.getElementById('viewer_container'),
                        {{backgroundColor: 'white'}}
                    );
                    
                    viewer.addModel({json.dumps(xyz_data)}, "xyz");
                    viewer.setStyle({{"stick": {{}}}});
                    viewer.zoomTo();
                    viewer.render();
                }});
            </script>
        </body>
        </html>
        """
            
    def show(self):
        """Display the molecule structure using 3Dmol.js."""
        try:
            xyz_data = self._read_xyz_file()
            
            html_content = self._generate_html(xyz_data)
            
            html_file_path = os.path.join(os.getcwd(), "molecule_visualization.html")
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            webbrowser.open(f"file://{html_file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

