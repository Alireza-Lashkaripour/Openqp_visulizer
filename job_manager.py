
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import threading
import queue
from typing import Optional

class JobManager:
    def __init__(self, parent):
        self.parent = parent
        self.process: Optional[subprocess.Popen] = None
        self.stop_flag = threading.Event()
        self.log_queue = queue.Queue()
        
    def _execute_job(self, input_file_path: str, log_file_path: str, log_text_widget: scrolledtext.ScrolledText):
        """
        Execute the job and monitor log output.
        """
        try:
            abs_input_path = os.path.abspath(input_file_path)
            input_dir = os.path.dirname(abs_input_path)
            input_filename = os.path.basename(abs_input_path)

            cmd = [
                "docker", "run",
                "--rm",
                "-v", f"{input_dir}:/data",
                "-w", "/data",
                "openqp:fixed",  
                "/usr/local/bin/openqp",  
                input_filename
            ]
            
            self._safe_log_update(log_text_widget, f"Starting job with command:\n{' '.join(cmd)}\n\n")
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            while self.process.poll() is None and not self.stop_flag.is_set():
                stdout_line = self.process.stdout.readline()
                if stdout_line:
                    self._safe_log_update(log_text_widget, stdout_line)
                
                stderr_line = self.process.stderr.readline()
                if stderr_line:
                    self._safe_log_update(log_text_widget, f"Error: {stderr_line}")
            
            stdout, stderr = self.process.communicate()
            if stdout:
                self._safe_log_update(log_text_widget, stdout)
            if stderr:
                self._safe_log_update(log_text_widget, f"Error: {stderr}\n")
            
            if self.process.returncode != 0:
                self._safe_log_update(
                    log_text_widget,
                    f"\nJob failed with exit code {self.process.returncode}\n"
                )
            else:
                self._safe_log_update(log_text_widget, "\nJob completed successfully.\n")
                
            if os.path.exists(log_file_path):
                self._safe_log_update(log_text_widget, "\nLog file contents:\n")
                with open(log_file_path, 'r') as log_file:
                    self._safe_log_update(log_text_widget, log_file.read())
                    
        except Exception as e:
            self._safe_log_update(
                log_text_widget,
                f"\nAn error occurred while executing the job: {str(e)}\n"
            )
        finally:
            self.process = None

    def _safe_log_update(self, log_widget: scrolledtext.ScrolledText, message: str):
        """Thread-safe method to update the log widget."""
        self.log_queue.put(message)
        self.parent.after(10, self._process_log_queue, log_widget)

    def _process_log_queue(self, log_widget: scrolledtext.ScrolledText):
        """Process pending log messages."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                log_widget.insert(tk.END, message)
                log_widget.see(tk.END)
                log_widget.update_idletasks()
        except queue.Empty:
            pass

