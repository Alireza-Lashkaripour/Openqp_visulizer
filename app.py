from flask import Flask, request, render_template, jsonify
from molecule_visualizer import MoleculeVisualizer
from openqp_input_generator import OpenQPInputGenerator
from job_manager import JobManager
from results_viewer import ResultsViewer
from geometry_extractor import GeometryExtractor
import os

app = Flask(__name__)

visualizer = MoleculeVisualizer(None)
input_generator = OpenQPInputGenerator(None)
job_manager = JobManager(None)
results_viewer = ResultsViewer(None)

@app.route("/")
def index():
    calc_options = [
        "DFT Energy",
        "DFT Geometry Optimization",
        "MRSF-TDDFT Ground State Energy",
        "MRSF-TDDFT First Excited State Energy",
        "MRSF-TDDFT Ground State Geometry Optimization",
        "MRSF-TDDFT First Excited State Geometry Optimization"
    ]
    return render_template("index.html", calc_options=calc_options)

@app.route("/load_geometry", methods=["POST"])
def load_geometry():
    file = request.files["file"]
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    
    with open(file_path, "r") as f:
        geometry_content = f.read()
        
    visualizer.set_geometry_path(file_path)
    input_generator.set_geometry_path(file_path)
    
    return jsonify({"geometry_content": geometry_content})

@app.route("/save_geometry", methods=["POST"])
def save_geometry():
    geometry_content = request.form["geometry_content"]
    file_name = request.form["file_name"]
    file_path = os.path.join("uploads", file_name)
    
    with open(file_path, "w") as f:
        f.write(geometry_content)
        
    visualizer.set_geometry_path(file_path)
    input_generator.set_geometry_path(file_path)
    
    return jsonify({"status": "Geometry saved successfully", "file_path": file_path})

@app.route("/generate_input", methods=["POST"])
def generate_input():
    calc_type = request.form["calc_type"]
    input_text = input_generator.generate_input_text(calc_type, input_generator.geometry_filename)
    return jsonify({"input_text": input_text})

@app.route("/submit_job", methods=["POST"])
def submit_job():
    job_name = request.form["job_name"]
    input_text = request.form["input_text"]
    
    input_file_path = input_generator.generate_input_file(input_text, job_name)
    log_file_path = os.path.join(os.path.dirname(input_file_path), f"{job_name}.log")
    
    job_manager._execute_job(input_file_path, log_file_path, None)
    
    return jsonify({"status": "Job submitted successfully", "log_file_path": log_file_path})

@app.route("/extract_geometry", methods=["POST"])
def extract_geometry():
    job_name = request.form["job_name"]
    log_file_path = os.path.join(os.getcwd(), f"{job_name}.log")
    
    try:
        extractor = GeometryExtractor(log_file_path)
        xyz_path = extractor.save_optimized_geometry(job_name)
        visualizer.set_geometry_path(xyz_path)
        return jsonify({"status": "Optimized geometry extracted", "xyz_path": xyz_path})
    except ValueError as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)  
    app.run(host="0.0.0.0", port=5000)

