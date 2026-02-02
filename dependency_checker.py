"""
Dependency checker module
Reads tool_db.json and checks if required dependencies are installed
Supports system tools and python packages
"""

import json
import importlib.util
import subprocess
import os
import re

TOOL_DB_PATH = "tool_db.json"


# -------------------- LOAD TOOL DATABASE --------------------

def load_tool_db(path=TOOL_DB_PATH):
    """Load tool database from JSON file."""
    with open(path, "r") as f:
        return json.load(f)


# -------------------- GENERIC CHECKERS --------------------

def check_python_package(package_name):
    """Check if a Python package is installed."""
    return importlib.util.find_spec(package_name) is not None


def check_system_command(command):
    """Check if a system command exists."""
    try:
        subprocess.run(
            [command, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False


# -------------------- VERILATOR --------------------

def check_verilator():
    """Check if Verilator is installed and return version."""
    try:
        result = subprocess.run(
            ["verilator", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout.strip() or result.stderr.strip()
        if output:
            return True, output
    except FileNotFoundError:
        pass
    return False, None


# -------------------- SCILAB --------------------

def check_scilab():
    """
    Check if Scilab is installed.
    Tries multiple command names and captures stdout or stderr.
    """
    commands = ["scilab", "scilab-cli", "scilab-cli.exe"]

    for cmd in commands:
        try:
            result = subprocess.run(
                [cmd, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout.strip() or result.stderr.strip()
            if output:
                return True, extract_scilab_version(output)
        except FileNotFoundError:
            continue

    return False, None


def extract_scilab_version(output):
    """Extract version number from Scilab output."""
    match = re.search(r"\d+\.\d+(\.\d+)?", output)
    return match.group(0) if match else "Unknown"


def check_java():
    """Check Java dependency required by Scilab."""
    try:
        subprocess.run(
            ["java", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False


# -------------------- CORE LOGIC --------------------

def check_dependencies_for_tool(tool_name, tool_info):
    """
    Check dependencies for a single tool.
    Returns detailed status including versions where applicable.
    """
    results = {}

    # Special handling
    if tool_name.lower() == "verilator":
        installed, version = check_verilator()
        results["verilator"] = {
            "installed": installed,
            "version": version or "Not Found"
        }
        return results

    if tool_name.lower() == "scilab":
        installed, version = check_scilab()
        results["scilab"] = {
            "installed": installed,
            "version": version or "Not Found"
        }
        results["java"] = {
            "installed": check_java(),
            "version": "N/A"
        }
        return results

    # Generic dependency handling
    for dep in tool_info.get("dependencies", []):
        if dep.startswith("python"):
            results[dep] = {
                "installed": check_python_package("sys"),
                "version": "N/A"
            }
        else:
            results[dep] = {
                "installed": check_system_command(dep),
                "version": "N/A"
            }

    return results


def check_all_dependencies():
    """Check dependencies for all tools."""
    db = load_tool_db()
    all_results = {}

    for tool_name, tool_info in db.items():
        all_results[tool_name] = check_dependencies_for_tool(tool_name, tool_info)

    return all_results
