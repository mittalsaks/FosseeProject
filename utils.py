"""
Utility functions for OS detection and command suggestions
"""


import platform
import shutil

def detect_os():
	"""Detect the current operating system."""
	os_name = platform.system().lower()
	if os_name.startswith('win'):
		return 'windows'
	elif os_name.startswith('linux'):
		return 'linux'
	elif os_name.startswith('darwin'):
		return 'macos'
	else:
		return os_name

def get_install_command(package_name):
	"""Return the package manager install command based on OS."""
	os_type = detect_os()
	if os_type == 'windows':
		return f'choco install {package_name}'
	elif os_type == 'linux':
		return f'sudo apt-get install {package_name}'
	elif os_type == 'macos':
		return f'brew install {package_name}'
	else:
		return f'Install {package_name} manually for {os_type}'

def command_exists(command):
	"""Check if a system command exists."""
	return shutil.which(command) is not None

# detect operating system and return 'linux', 'windows', or 'mac'
def get_os_type():
    return detect_os()

# return package manager install command suggestion based on OS
def suggest_install_command(package_name):
    return get_install_command(package_name)

import os
import subprocess

def install_verilator():
    if os.name == "nt":
        print("Windows detected.")
        print("Please install Verilator using Chocolatey:")
        print("  choco install verilator")
    else:
        print("Linux/macOS detected.")
        print("Run the following command:")
        print("  sudo apt install verilator")

