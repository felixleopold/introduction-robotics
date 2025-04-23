# Introduction to Robotics

This repository contains the practical project for the Introduction to Robotics course.

- [File Structure](#file-structure)
- [Installation](#installation)
  - [Cloning the Repo](#cloning-the-repo)
  - [Virtual Environment & Dependencies](#virtual-environment-&-Dependencies)
- [Usage](#usage)
  - [Simulation](#simulation)
  - [LEGO Robot](#lego-robot)
- [Information & Documents](information-&-documents)
  - [CoppeliaSim](coppeliasim)
  - [Building the Robot](building-the-robot)

## File Structure

```
.
├── Assignment.pdf
├── README.md
├── lego
│   └── lego_lineMaze.llsp3
│   └── lego_sortCubes.llsp3
├── python
│   ├── lineMaze.py
│   ├── robots.py
│   └── wall_e_script.py
├── requirements.txt
└── scenes
    ├── lineMaze.ttt
    └── wall_e_v4.1.ttt
```

## Installation

### 1 Clone the repo

```bash
git clone https://github.com/felixleopold/introduction-robotics.git
cd introduction-robotics
```

### 2 Create a virtual environment

**macOS/Linux**

```bash
python3 -m venv venv
```

**Windows**

```bash
python -m venv venv
```

### 3 Activate the virtual environment

**macOS/Linux**

```bash
source venv/bin/activate
```

**Windows (cmd)**

```bash
venv\\Scripts\\activate
```

**Windows (PowerShell)**

```powershell
.\\venv\\Scripts\\Activate.ps1
```

### 4 Install dependencies

**macOS/Linux**

```bash
pip3 install -r requirements.txt
```

**Windows**

```bash
pip install -r requirements.txt
```

## Usage

### Simulation

1. start `CoppeliaSim`
2. open a scene file from the `scenes` folder:
   - `scenes/lineMaze.ttt`
   - `scenes/wall_e_v4.1.ttt`
3. run the matching Python script

```bash
source venv/bin/activate          # skip source on Windows
python3 python/lineMaze.py        # for line maze
python3 python/wall_e_script.py   # for Wall‑E
```

### Lego Robot

```bash
open -a "Spike" lego/lego_lineMaze.llsp3
open -a "Spike" lego/lego_sortCubes.llsp3
```

# Information & Documents

## CoppeliaSim

[CoppeliaSim](https://www.coppeliarobotics.com/) is the simulation software for this course

API reference: https://manual.coppeliarobotics.com/en/apiFunctions.htm

## Building the robot

YouTube video by Mr Hino: https://www.youtube.com/watch?v=FlnZsZSEvhU
