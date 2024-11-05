
# OpenQP GUI Application

This application provides a graphical user interface (GUI) for **OpenQP** to set up molecular calculations, 
visualize molecular structures, and view optimized geometries and molecular orbitals.

## Prerequisites

1. **Docker**: Required for running OpenQP in an isolated environment.
   - [Get Docker for Linux](https://docs.docker.com/engine/install/)
   - [Get Docker for macOS](https://docs.docker.com/docker-for-mac/install/)
   - [Get Docker for Windows](https://docs.docker.com/docker-for-windows/install/)

2. **Python 3.x**: Required for running the GUI.
   - Linux/macOS: Install via package manager (`apt`, `brew`).
   - Windows: Install from [python.org](https://www.python.org/downloads/).

3. **Python Libraries**:
   - `tkinter`: For GUI (usually pre-installed with Python, but may need to be installed separately on Linux).
   - `py3Dmol`: For molecular visualization.
   - Install required libraries using:
     ```bash
     pip install tkinter py3Dmol
     ```

## Installation & Setup

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/Alireza-Lashkaripour/Openqp_visulizer.git
cd Openqp_visulizer
```

### 2. Download Docker Image
Pull the pre-built Docker image for OpenQP:
```bash
docker pull alireza0027/openqp:fixed
```

## Running the Application

### Linux

1. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   pip3 install py3Dmol
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Openqp_visulizer
   ```

3. **Launch the GUI**:
   ```bash
   python3 main_gui.py
   ```

### macOS

1. **Install dependencies**:
   ```bash
   brew install python3
   pip3 install py3Dmol
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Openqp_visulizer
   ```

3. **Launch the GUI**:
   ```bash
   python3 main_gui.py
   ```

### Windows (Spyder)

1. **Install dependencies**:
   ```Spyder
   python -m pip install --upgrade pip
   python -m pip install py3Dmol
   ```

2. **Navigate to the project directory**:
   ```Spyder
   cd Openqp_visulizer
   ```

3. **Launch the GUI**:
   ```Spyder
   python main_gui.py
   ```

## Usage

1. **Load Geometry**: Use the "Load Geometry" button to select and load an XYZ file or paste the geometry manually.
2. **Visualize Molecule**: Click "Visualize Molecule" to see a 3D representation of the molecular structure.
3. **Set Calculation Type**: Choose the desired calculation type from the dropdown menu.
4. **Generate Input**: The input file for OpenQP is automatically generated based on the selected calculation type and geometry.
5. **Submit Job**: Enter a job name and click "Submit Job" to run the calculation. The console log updates in real-time.
6. **View Results**: Once the job completes, click "View Results" to open the log file or visualize molecular orbitals.
7. **Extract Optimized Geometry**: For optimization calculations, click "Extract Optimized Geometry" to extract and visualize the final optimized geometry.





# OpenQP GUI 애플리케이션

이 애플리케이션은 **OpenQP**를 위한 그래픽 사용자 인터페이스(GUI)를 제공하여 분자 계산을 설정하고, 
분자 구조를 시각화하며, 최적화된 기하학과 분자 오비탈을 확인할 수 있습니다.

## 사전 요구 사항

1. **Docker**: OpenQP를 격리된 환경에서 실행하기 위해 필요합니다.
   - [Linux용 Docker 설치](https://docs.docker.com/engine/install/)
   - [macOS용 Docker 설치](https://docs.docker.com/docker-for-mac/install/)
   - [Windows용 Docker 설치](https://docs.docker.com/docker-for-windows/install/)

2. **Python 3.x**: GUI를 실행하기 위해 필요합니다.
   - Linux/macOS: 패키지 관리자(`apt`, `brew`)를 통해 설치하세요.
   - Windows: [python.org](https://www.python.org/downloads/)에서 설치하세요.

3. **Python 라이브러리**:
   - `tkinter`: GUI를 위한 라이브러리 (일반적으로 Python에 기본 설치되어 있지만, Linux에서는 별도로 설치해야 할 수 있습니다).
   - `py3Dmol`: 분자 시각화를 위한 라이브러리.
   - 다음 명령어를 통해 필요한 라이브러리를 설치하세요:
     ```bash
     pip install tkinter py3Dmol
     ```

## 설치 및 설정

### 1. 리포지토리 클론
로컬 컴퓨터에 이 리포지토리를 클론하세요:
```bash
git clone https://github.com/Alireza-Lashkaripour/Openqp_visulizer.git
cd Openqp_visulizer
```

### 2. Docker 이미지 다운로드
OpenQP의 사전 빌드된 Docker 이미지를 다운로드하세요:
```bash
docker pull alireza0027/openqp:fixed
```

## 애플리케이션 실행

### Linux

1. **필수 패키지 설치**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   pip3 install py3Dmol
   ```

2. **프로젝트 디렉토리로 이동**:
   ```bash
   cd Openqp_visulizer
   ```

3. **GUI 실행**:
   ```bash
   python3 main_gui.py
   ```

### macOS

1. **필수 패키지 설치**:
   ```bash
   brew install python3
   pip3 install py3Dmol
   ```

2. **프로젝트 디렉토리로 이동**:
   ```bash
   cd Openqp_visulizer
   ```

3. **GUI 실행**:
   ```bash
   python3 main_gui.py
   ```

### Windows (PowerShell)

1. **필수 패키지 설치**:
   ```Spyder
   python -m pip install --upgrade pip
   python -m pip install py3Dmol
   ```

2. **프로젝트 디렉토리로 이동**:
   ```Spyder
   cd Openqp_visulizer
   ```

3. **GUI 실행**:
   ```Spyder
   python main_gui.py
   ```

## 사용 방법

1. **기하학 로드**: "Load Geometry" 버튼을 사용하여 XYZ 파일을 선택하고 로드하거나 기하학을 수동으로 붙여넣습니다.
2. **분자 시각화**: "Visualize Molecule" 버튼을 클릭하여 분자 구조의 3D 표현을 확인합니다.
3. **계산 유형 설정**: 드롭다운 메뉴에서 원하는 계산 유형을 선택합니다.
4. **입력 파일 생성**: 선택한 계산 유형과 기하학을 기반으로 OpenQP 입력 파일이 자동으로 생성됩니다.
5. **작업 제출**: 작업 이름을 입력하고 "Submit Job" 버튼을 클릭하여 계산을 실행합니다. 콘솔 로그가 실시간으로 업데이트됩니다.
6. **결과 보기**: 작업이 완료되면 "View Results" 버튼을 클릭하여 로그 파일을 열거나 분자 오비탈을 시각화합니다.
7. **최적화된 기하학 추출**: 최적화 계산의 경우 "Extract Optimized Geometry" 버튼을 클릭하여 최적화된 최종 기하학을 추출하고 시각화합니다.

