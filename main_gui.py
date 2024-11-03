# main_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, StringVar, OptionMenu
from molecule_visualizer import MoleculeVisualizer
from openqp_input_generator import OpenQPInputGenerator
from job_manager import JobManager
from results_viewer import ResultsViewer
import os

class OpenQPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenQP GUI")
        
        # Initialize modules
        self.visualizer = MoleculeVisualizer(self.root)
        self.input_generator = OpenQPInputGenerator(self.root)
        self.job_manager = JobManager(self.root)
        self.results_viewer = ResultsViewer(self.root)
        
        # Layout: Left and Right Panels
        left_frame = tk.Frame(self.root, padx=10, pady=10)
        right_frame = tk.Frame(self.root, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Left Panel: Geometry Input and Visualization
        tk.Label(left_frame, text="Paste Geometry (XYZ format)").pack()
        self.geometry_text = scrolledtext.ScrolledText(left_frame, wrap="word", height=10, width=30)
        self.geometry_text.pack()

        tk.Button(left_frame, text="Save Geometry", command=self.save_geometry).pack(pady=5)
        tk.Button(left_frame, text="Visualize Molecule", command=self.visualizer.show).pack(pady=5)

        # Right Panel: Calculation and Job Management
        tk.Label(right_frame, text="Calculation Type").pack()
        self.calc_type = StringVar(value="MRSF ENERGY")
        calc_options = ["MRSF ENERGY"]
        self.calc_menu = OptionMenu(right_frame, self.calc_type, *calc_options)
        self.calc_menu.pack()

        tk.Label(right_frame, text="Generated Input").pack()
        self.input_text = scrolledtext.ScrolledText(right_frame, wrap="word", height=10, width=40)
        self.input_text.pack()
        
        tk.Label(right_frame, text="Job Name").pack()
        self.job_name_entry = tk.Entry(right_frame)
        self.job_name_entry.pack()

        tk.Button(right_frame, text="Submit Job", command=self.submit_job).pack(pady=5)

        self.log_text = scrolledtext.ScrolledText(right_frame, wrap="word", height=5, width=40)
        self.log_text.pack(pady=5)

        tk.Button(right_frame, text="View Results", command=self.results_viewer.show_results).pack(pady=5)

    def save_geometry(self):
        """Save the geometry text as an .xyz file and set it for visualization and input generation."""
        geometry_content = self.geometry_text.get("1.0", tk.END).strip()
        if not geometry_content:
            messagebox.showwarning("Warning", "No geometry data entered.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xyz", filetypes=[("XYZ files", "*.xyz")])
        if save_path:
            with open(save_path, 'w') as file:
                file.write(geometry_content)
            messagebox.showinfo("Saved", f"Geometry saved as {save_path}")

            # Set the saved file path in the visualizer and input generator
            self.visualizer.set_geometry_path(save_path)
            self.input_generator.set_geometry_path(save_path)

            # Generate and display the input text in the GUI
            input_text = self.input_generator.generate_input_text(self.calc_type.get(), save_path)
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", input_text)

    def submit_job(self):
        """Generate input file and run the job based on user input."""
        job_name = self.job_name_entry.get().strip()
        if not job_name:
            messagebox.showwarning("Warning", "Please enter a job name.")
            return

        # Define the path for the input and log files
        input_file_path = self.input_generator.generate_input_file(self.input_text.get("1.0", tk.END), job_name)
        log_file_path = os.path.join(os.path.dirname(input_file_path), f"{job_name}.log")

        # Start the job with the specified input and log paths
        if input_file_path:
            self.job_manager._execute_job(input_file_path, log_file_path, self.log_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenQPGUI(root)
    root.mainloop()

