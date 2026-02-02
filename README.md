# eSim Automated Tool Manager

An OS-independent Automated Tool Manager for eSim that focuses on dependency checking and a user-friendly command-line interface (CLI).
This tool helps users verify whether required external tools and their dependencies are correctly installed and compatible with their system.


## Project Overview

eSim integrates multiple external EDA tools such as **Ngspice, KiCad, Scilab, and Verilator**. Managing these tools manually across different operating systems can lead to missing dependencies and configuration issues.

This project provides:

* An **OS-aware dependency checker** (Windows / Linux / macOS)
* A simple **CLI interface** to view tool and dependency status
* Clear user feedback for missing or incompatible dependencies
* Logging of actions and errors for traceability

> **Note:** This prototype focuses on *Dependency Checker* and *User Interface* deliverables as required by the task.

##  Repository Structure
```
eSim-Automated-Tool-Manager/
│
├── main.py                  # CLI entry point
├── dependency_checker.py    # Core dependency checking logic
├── utils.py                 # OS detection & helper utilities
├── logger_config.py         # Logging configuration
├── tool_db.json             # Tool & dependency metadata
├── requirements.txt         # Python dependencies
├── tool_manager.log         # Runtime logs
├── README.md                # Project documentation
│
└── docs/
    └── Design_Document.md   # Detailed design document
```


## Supported Tools (Prototype Scope)

* Ngspice
* KiCad
* Verilator
* Scilab
* Java (dependency for Scilab)


## Key Features

### Dependency Checker

* Checks required system tools and dependencies
* Uses **OS-aware logic** to avoid false positives

  * Windows: executable path checks (e.g., `Scilab.exe`)
  * Linux/macOS: CLI-based checks (e.g., `verilator --version`)
* Detects tool availability and versions (when possible)

### Command-Line Interface (CLI)

* Simple command to run all dependency checks
* Displays:

  * Tool name
  * Dependency name
  * Installation status
  * Version information
* Logs results and errors


## Prerequisites

* Python **3.8 or higher**
* Windows / Linux / macOS


## Installation & Setup

### 1 Clone the Repository

```bash
git clone <your-private-repo-url>
cd eSim-Automated-Tool-Manager
```

### 2️ Install Python Dependencies

```bash
pip install -r requirements.txt
```


## How to Run

Run the Automated Tool Manager:

```bash
python main.py
```

This will execute dependency checks and display the results in the terminal.


## 🧪 Testing Instructions

### Test OS Detection

```bash
python -c "import platform; print(platform.system())"
```

### Test Scilab Dependency Check

```bash
python -c "from dependency_checker import check_scilab; print(check_scilab())"
```

> **Note:**  
> On **Windows**, Scilab is detected via installation paths and executables  
> (GUI-based installation, limited CLI support).  
> On **Linux/macOS**, Scilab is detected using CLI-based version checks.


### Test Verilator Dependency Check

```bash
python -c "from dependency_checker import check_verilator; print(check_verilator())"
```

### Run Full Dependency Scan

```bash
python main.py
```


## Design Documentation

A detailed design document describing the architecture, module breakdown, and interaction between components is available at:
```
docs/Design_Document.md
```


## Future Enhancements

* Automatic installation using package managers (apt, Chocolatey, Homebrew)
* Tool update and upgrade management
* Version compatibility enforcement
* Graphical User Interface (GUI)
* Deeper integration with eSim configuration


## Submission Notes

This repository is submitted as part of:

**eSim Semester Long Internship – Spring 2026**
**Task 5 Submission**

The repository is private and access has been granted to the evaluators as per submission guidelines.

---

## Authors

- **Saumya Dwivedi**  
  📧 saumya.23bce10331@vitbhopal.ac.in

- **Sakshi Mittal**  
  📧 sakshi.23bce11231@vitbhopal.ac.in
