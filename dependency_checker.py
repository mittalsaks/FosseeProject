"""
Dependency checker module
Reads tool_db.json and checks if required dependencies are installed
"""

import json
import importlib.util
import subprocess
import re

TOOL_DB_PATH = "tool_db.json"


def load_tool_db(path=TOOL_DB_PATH):
    with open(path, "r") as f:
        return json.load(f)


# ---------------- GENERIC CHECKERS ----------------

def check_python_package(pkg):
    return importlib.util.find_spec(pkg) is not None


def check_system_command(cmd):
    try:
        subprocess.run(
            [cmd, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False


# ---------------- VERILATOR ----------------

def check_verilator():
    try:
        result = subprocess.run(
            ["verilator", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout.strip() or result.stderr.strip()
        return True, output
    except FileNotFoundError:
        return False, "Not Found"


# ---------------- SCILAB ----------------

def check_scilab():
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

    return False, "Not Found"


def extract_scilab_version(output):
    match = re.search(r"\d+\.\d+(\.\d+)?", output)
    return match.group(0) if match else "Unknown"


def check_java():
    try:
        subprocess.run(["java", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


# ---------------- CORE ----------------

def check_dependencies_for_tool(tool_name, tool_info):
    results = {}

    if tool_name.lower() == "verilator":
        installed, version = check_verilator()
        results["verilator"] = {
            "installed": installed,
            "version": version
        }
        return results

    if tool_name.lower() == "scilab":
        installed, version = check_scilab()
        results["scilab"] = {
            "installed": installed,
            "version": version
        }
        results["java"] = {
            "installed": check_java(),
            "version": "N/A"
        }
        return results

    for dep in tool_info.get("dependencies", []):
        if dep.startswith("python"):
            installed = check_python_package("sys")
        else:
            installed = check_system_command(dep)

        results[dep] = {
            "installed": installed,
            "version": "N/A"
        }

    return results


def check_all_dependencies():
    db = load_tool_db()
    return {
        tool: check_dependencies_for_tool(tool, info)
        for tool, info in db.items()
    }
