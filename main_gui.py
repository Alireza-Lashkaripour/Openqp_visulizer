import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, StringVar, OptionMenu
from molecule_visualizer import MoleculeVisualizer
from openqp_input_generator import OpenQPInputGenerator
from job_manager import JobManager
from results_viewer import ResultsViewer
from geometry_extractor import GeometryExtractor
import os

class OpenQPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenQP GUI")
        
        self.visualizer = MoleculeVisualizer(self.root)
        self.input_generator = OpenQPInputGenerator(self.root)
        self.job_manager = JobManager(self.root)
        self.results_viewer = ResultsViewer(self.root)
        
        calc_options = [
            "DFT Energy",
            "DFT Geometry Optimization",
            "MRSF-TDDFT Ground State Energy",
            "MRSF-TDDFT First Excited State Energy",
            "MRSF-TDDFT Ground State Geometry Optimization",
            "MRSF-TDDFT First Excited State Geometry Optimization"
        ]
        
        left_frame = tk.Frame(self.root, padx=10, pady=10)
        right_frame = tk.Frame(self.root, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(left_frame, text="Paste or Load Geometry (XYZ format)").pack()
        self.geometry_text = scrolledtext.ScrolledText(left_frame, wrap="word", height=10, width=30)
        self.geometry_text.pack()

        tk.Button(left_frame, text="Load Geometry", command=self.load_geometry).pack(pady=5)
        tk.Button(left_frame, text="Save Geometry", command=self.save_geometry).pack(pady=5)
        tk.Button(left_frame, text="Visualize Molecule", command=self.visualizer.show).pack(pady=5)

        tk.Label(right_frame, text="Calculation Type").pack()
        self.calc_type = StringVar(value="MRSF-TDDFT Ground State Energy")
        
        self.calc_menu = OptionMenu(right_frame, self.calc_type, *calc_options, command=self.update_input_text)
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
        tk.Button(right_frame, text="Extract Optimized Geometry", command=self.extract_geometry).pack(pady=5)

    def load_geometry(self):
        file_path = filedialog.askopenfilename(
            title="Select XYZ File",
            filetypes=[("XYZ files", "*.xyz"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    geometry_content = file.read()
                
                self.geometry_text.delete("1.0", tk.END)
                self.geometry_text.insert("1.0", geometry_content)
                
                self.visualizer.set_geometry_path(file_path)
                self.input_generator.set_geometry_path(file_path)
                
                self.update_input_text(self.calc_type.get())
                
                messagebox.showinfo("Loaded", f"Geometry loaded from {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def save_geometry(self):
        geometry_content = self.geometry_text.get("1.0", tk.END).strip()
        if not geometry_content:
            messagebox.showwarning("Warning", "No geometry data entered.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xyz", filetypes=[("XYZ files", "*.xyz")])
        if save_path:
            with open(save_path, 'w') as file:
                file.write(geometry_content)
            messagebox.showinfo("Saved", f"Geometry saved as {save_path}")

            self.visualizer.set_geometry_path(save_path)
            self.input_generator.set_geometry_path(save_path)

            self.update_input_text(self.calc_type.get())

    def update_input_text(self, calc_type):
        input_text = self.input_generator.generate_input_text(calc_type, self.input_generator.geometry_filename)
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", input_text)

    def submit_job(self):
        job_name = self.job_name_entry.get().strip()
        if not job_name:
            messagebox.showwarning("Warning", "Please enter a job name.")
            return

        input_file_path = self.input_generator.generate_input_file(self.input_text.get("1.0", tk.END), job_name)
        log_file_path = os.path.join(os.path.dirname(input_file_path), f"{job_name}.log")

        if input_file_path:
            self.job_manager._execute_job(input_file_path, log_file_path, self.log_text)

    def extract_geometry(self):
        job_name = self.job_name_entry.get().strip()
        if not job_name:
            messagebox.showwarning("Warning", "Please enter a job name.")
            return

        log_file_path = os.path.join(os.getcwd(), f"{job_name}.log")
        
        try:
            extractor = GeometryExtractor(log_file_path)
            xyz_path = extractor.save_optimized_geometry(job_name)
            
            self.visualizer.set_geometry_path(xyz_path)
            messagebox.showinfo("Success", f"Optimized geometry saved as {xyz_path}")
            self.visualizer.show()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenQPGUI(root)
    root.mainloop()

