# Introduction-Robotics

This repository contains the practical project for the Introduction to Robotics course.

- [Installation](#installation)
  - [Cloning the Repo](#cloning-the-repo)
  - [Virtual Environment & Dependencies](#virtual-environment-&-Dependencies)
- [Information & Documents](information-&-documents)
  - [CoppeliaSim](coppeliasim)
  - [Building the Robot](building-the-robot)

# Installation

## Cloning the Repo

```bash
https://github.com/felixleopold/introduction-robotics.git
cd introduction-robotics
```

## Virtual Environment & Dependencies

### 2. Create a virtual environment

- **macOS/Linux:**
```bash
python3 -m venv venv
```

- **Windows:**
```bash
python -m venv venv
```

### 3. Activate the virtual environment

- **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

- **Windows (cmd):**

  ```bash
  venv\Scripts\activate
  ```

- **Windows (PowerShell):**

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 4. Install dependencies


- **Windows:**
```bash
pip install -r requirements.txt
```


- **macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

# Usage

1. Start `CoppeliaSim`

2.
```bash
source venv/bin/activate
cd StarterFiles/

# for line maze
python3 lineMaze.py

# for wall e
python3 wall_e_script.py
```

# Information & Documents

## CoppeliaSim

[CoppeliaSim](https://www.coppeliarobotics.com/) is the simulation software we will be using for this course.

[Regular API reference](https://manual.coppeliarobotics.com/en/apiFunctions.htm)

## Building the Robot

[YouTube Video by Mr.Hino](https://www.youtube.com/watch?v=FlnZsZSEvhU)