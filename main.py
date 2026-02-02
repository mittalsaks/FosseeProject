"""
CLI entry point for eSim Automated Tool Manager
Supports commands:
- list
- check
- status
- log
"""


import argparse
import os
from dependency_checker import load_tool_db, check_all_dependencies
from logger_config import get_logger

def list_tools():
	db = load_tool_db()
	print("Tool\tExpected Version")
	for tool, info in db.items():
		print(f"{tool}\t{info.get('version', 'N/A')}")

def check_dependencies():
	results = check_all_dependencies()
	print("Tool\tDependency\tStatus")
	for tool, deps in results.items():
		for dep, status in deps.items():
			print(f"{tool}\t{dep}\t{'OK' if status else 'Missing'}")

def show_status():
	results = check_all_dependencies()
	summary = {}
	for tool, deps in results.items():
		summary[tool] = all(deps.values())
	print("Tool\tStatus")
	for tool, status in summary.items():
		print(f"{tool}\t{'Ready' if status else 'Incomplete'}")

def display_log():
	log_path = "tool_manager.log"
	if os.path.exists(log_path):
		with open(log_path, "r") as f:
			print(f.read())
	else:
		print("Log file not found.")

def main():
	parser = argparse.ArgumentParser(description="eSim Automated Tool Manager")
	subparsers = parser.add_subparsers(dest="command")

	subparsers.add_parser("list", help="List all tools and expected versions")
	subparsers.add_parser("check", help="Check dependencies and display results")
	subparsers.add_parser("status", help="Show summary status of all tools")
	subparsers.add_parser("log", help="Display log file")

	args = parser.parse_args()
	logger = get_logger()

	if args.command == "list":
		logger.info("Listing all tools.")
		list_tools()
	elif args.command == "check":
		logger.info("Checking dependencies.")
		check_dependencies()
	elif args.command == "status":
		logger.info("Showing summary status.")
		show_status()
	elif args.command == "log":
		logger.info("Displaying log file.")
		display_log()
	else:
		parser.print_help()

if __name__ == "__main__":
	main()

# display dependency check results in a color-coded table
# green for installed, red for missing
def display_colored_dependency_table():
    from rich.table import Table
    from rich.console import Console
    from rich import box

    console = Console()
    table = Table(title="Dependency Check Results", box=box.SIMPLE_HEAVY)

    table.add_column("Tool", style="cyan", no_wrap=True)
    table.add_column("Dependency", style="magenta")
    table.add_column("Status", style="green")

    results = check_all_dependencies()
    for tool, deps in results.items():
        for dep, status in deps.items():
            status_str = "[green]Installed[/green]" if status else "[red]Missing[/red]"
            table.add_row(tool, dep, status_str)

    console.print(table)
	
# show summary including total tools and missing dependencies
def show_summary():
    results = check_all_dependencies()
    total_tools = len(results)
    tools_ready = sum(1 for deps in results.values() if all(deps.values()))
    total_missing = sum(1 for deps in results.values() for status in deps.values() if not status)

    print(f"Total Tools: {total_tools}")
    print(f"Tools Ready: {tools_ready}")
    print(f"Total Missing Dependencies: {total_missing}")

from dependency_checker import check_verilator
from utils import install_verilator

def main():
    result = check_verilator()

    if not result["installed"]:
        print("Verilator not found.")
        install_verilator()
    else:
        print(f"Verilator installed. Version: {result['version']}")
