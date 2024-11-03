
# OpenQP GUI Application

This application provides an easy-to-use GUI for **OpenQP** to set up molecular calculations, visualize molecular structures, and view molecular orbitals (MOs).

## Requirements

1. **Docker** installed on your system ([Get Docker](https://docs.docker.com/get-docker/))
2. **Python 3.x** installed with the following packages:
   - `tkinter` for GUI
   - `py3Dmol` for molecular visualization
   - `subprocess` and `os` for Docker integration

> Note: These libraries are used within Python scripts, and Docker is used to run OpenQP itself.

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Alireza-Lashkaripour/Openqp_visulizer.git
   cd Openqp_visulizer
   ```

2. **Download the Docker Image**:
   Use the pre-built Docker image to avoid any manual setup.
   ```bash
   docker pull alireza0027/openqp:fixed
   ```

3. **Build the Docker Image Locally (Optional)**:
   If you prefer to build it yourself, ensure you’re in the correct directory with the Dockerfile and run:
   ```bash
   docker build -t openqp:fixed .
   ```

## Running the Application

1. **Launch the GUI**:
   Run the main Python script to start the GUI.
   ```bash
   python3 main_gui.py
   ```

2. **Using the GUI**:

   - **Input Geometry**: Paste or load the molecular geometry in XYZ format in the provided input box.
   - **Visualize Molecule**: Click “Visualize Molecule” to see a 3D representation of the structure.
   - **Set Calculation Type**: Currently, “MRSF ENERGY” is supported. Additional types can be added if needed.
   - **Generate and Submit Job**:
      - Enter a job name and click **Submit Job**. The GUI will manage Docker and execute the job automatically.
      - The console log will update in real-time with job progress and errors.
   - **View Results**:
      - Click “View Results” after completion to view output data, including .log and Molden files for molecular orbitals.

## Visualizing Molecular Orbitals

Molecular orbital visualizations are based on Molden files generated from OpenQP. The GUI will automatically load and display the MOs after the job completes.

