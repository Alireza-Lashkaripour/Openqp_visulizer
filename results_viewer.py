import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, StringVar, OptionMenu
import os
import webbrowser
from pathlib import Path
import tempfile

class ResultsViewer:
    def __init__(self, parent):
        """Initialize the ResultsViewer with a parent window."""
        self.parent = parent
        self.temp_files = []
        self.mo_data = []  

    def __del__(self):
        """Cleanup temporary files when the object is destroyed."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Error cleaning up temporary file {temp_file}: {e}")

    def show_results(self):
        """Main function to display options for viewing results."""
        results_window = tk.Toplevel(self.parent)
        results_window.title("Results Viewer")
        results_window.geometry("300x300")

        frame = tk.Frame(results_window, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text="Select an option to view results:", 
                 font=('Arial', 10, 'bold')).pack(pady=(0, 10))
        
        tk.Button(frame, text="Open Log File", 
                  command=self.open_log_file,
                  width=25, 
                  relief=tk.GROOVE).pack(pady=5)

        tk.Label(frame, text="Choose Molecular Orbital:").pack(pady=5)
        
        
        if not self.mo_data:
            self.mo_data = ["MO 1"]  
        
        self.mo_var = StringVar(value="Select MO")
        self.mo_options = [f"MO {i + 1}" for i in range(len(self.mo_data))]
        
        mo_menu = OptionMenu(frame, self.mo_var, *self.mo_options, command=self.visualize_selected_mo)
        mo_menu.pack(pady=5)



    def open_log_file(self):
        """Open and display the contents of a selected log file."""
        try:
            log_file_path = filedialog.askopenfilename(
                title="Select Log File",
                filetypes=[("Log files", "*.log"), ("All files", "*.*")]
            )
            
            if not log_file_path:  
                return
                
            if not os.path.exists(log_file_path):
                messagebox.showwarning("Warning", "Selected file does not exist.")
                return

            log_window = tk.Toplevel(self.parent)
            log_window.title(f"Log File Viewer - {Path(log_file_path).name}")
            log_window.geometry("800x600")

            menubar = tk.Menu(log_window)
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="Save As...", 
                                  command=lambda: self.save_log_content(log_text))
            menubar.add_cascade(label="File", menu=file_menu)
            log_window.config(menu=menubar)

            frame = tk.Frame(log_window)
            frame.pack(fill='both', expand=True, padx=5, pady=5)

            search_frame = tk.Frame(frame)
            search_frame.pack(fill='x', padx=5, pady=(0, 5))
            
            tk.Label(search_frame, text="Search:").pack(side='left')
            search_var = tk.StringVar()
            search_entry = tk.Entry(search_frame, textvariable=search_var)
            search_entry.pack(side='left', padx=5)
            
            tk.Button(search_frame, text="Find",
                      command=lambda: self.search_text(log_text, search_var.get())
                      ).pack(side='left')

            log_text = scrolledtext.ScrolledText(
                frame, 
                wrap=tk.WORD, 
                width=80, 
                height=20,
                font=('Courier', 10)
            )
            log_text.pack(expand=True, fill='both')

            try:
                with open(log_file_path, 'r', encoding='utf-8') as log_file:
                    log_text.insert(tk.END, log_file.read())
                log_text.config(state='disabled')  
            except UnicodeDecodeError:
                with open(log_file_path, 'r', encoding='latin-1') as log_file:
                    log_text.insert(tk.END, log_file.read())
                log_text.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log file: {str(e)}")

    def save_log_content(self, text_widget):
        """Save the content of the text widget to a file."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_widget.get(1.0, tk.END))
                messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def search_text(self, text_widget, search_string):
        """Search for text in the text widget and highlight matches."""
        text_widget.tag_remove('search', '1.0', tk.END)
        if search_string:
            pos = '1.0'
            while True:
                pos = text_widget.search(search_string, pos, tk.END, nocase=True)
                if not pos:
                    break
                end_pos = f"{pos}+{len(search_string)}c"
                text_widget.tag_add('search', pos, end_pos)
                pos = end_pos
            text_widget.tag_config('search', background='yellow')


    def visualize_selected_mo(self, selected_mo):
        """Visualize the selected molecular orbital using 3Dmol.js."""
        try:
            
            if not hasattr(self, 'molden_file_path') or not self.molden_file_path:
                molden_file_path = filedialog.askopenfilename(
                    title="Select Molden File",
                    filetypes=[("Molden files", "*.molden"), ("All files", "*.*")]
                )
                if molden_file_path:
                    self.molden_file_path = molden_file_path
                else:
                    messagebox.showwarning("Warning", "No Molden file selected.")
                    return

            mo_index = int(selected_mo.split()[1]) - 1
            xyz_data, mo_data = self.parse_molden_file(self.molden_file_path)

            if not xyz_data or not mo_data:
                messagebox.showerror("Error", "No atomic coordinates or MO data found in the Molden file.")
                return

            html_content = self.create_visualization_html(xyz_data, mo_data[mo_index])

            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.html',
                delete=False,
                encoding='utf-8'
            ) as temp_file:
                temp_file.write(html_content)
                self.temp_files.append(temp_file.name)
                
            webbrowser.open(f"file://{temp_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize molecular orbitals: {str(e)}")



    def parse_molden_file(self, molden_file_path):
        """Parse atomic coordinates and MO data from the Molden file."""
        try:
            xyz_data = []
            mo_data = []  
            with open(molden_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            reading_atoms = False
            reading_mos = False
            for line in lines:
                if "[Atoms]" in line:
                    reading_atoms = True
                    reading_mos = False
                    continue
                elif "[MO]" in line:
                    reading_atoms = False
                    reading_mos = True
                    continue
                elif line.strip() == "" or "[" in line:
                    reading_atoms = False
                    reading_mos = False

                if reading_atoms:
                    parts = line.split()
                    if len(parts) >= 5:
                        element = parts[0]
                        x, y, z = map(float, parts[2:5])
                        xyz_data.append(f"{element} {x:.6f} {y:.6f} {z:.6f}")
                
                if reading_mos:
                    mo_data.append(line.strip())  

            return xyz_data, mo_data

        except Exception as e:
            print(f"Error parsing Molden file: {e}")
            return None, None

    def create_visualization_html(self, xyz_data, mo_data):
        """Create HTML content for molecular orbital visualization."""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Molecular Orbital Visualization</title>
            <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
            <style>
                body {{ margin: 0; padding: 0; }}
                #viewer {{ width: 100vw; height: 100vh; }}
            </style>
        </head>
        <body>
            <div id="viewer"></div>
            <script>
                let viewer = $3Dmol.createViewer(document.getElementById("viewer"), {{
                    backgroundColor: "white"
                }});
                
                viewer.addModel({xyz_data}, "xyz");
                viewer.setStyle({{"stick":{{}}}});
                
                viewer.addSurface($3Dmol.SurfaceType.VDW, {{
                    opacity: 0.85,
                    colorscheme: 'orangeCarbon',
                    voldata: {mo_data}
                }});

                viewer.zoomTo();
                viewer.render();
            </script>
        </body>
        </html>
        """
