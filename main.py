"""
CLI entry point for eSim Automated Tool Manager
Commands:
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
        for dep, info in deps.items():
            status = "OK" if info["installed"] else "MISSING"
            print(f"{tool}\t{dep}\t{status}")


def show_status():
    results = check_all_dependencies()
    print("Tool\tStatus")

    for tool, deps in results.items():
        ready = all(info["installed"] for info in deps.values())
        print(f"{tool}\t{'Ready' if ready else 'Incomplete'}")


def display_log():
    log_path = "tool_manager.log"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            print(f.read())
    else:
        print("No logs available.")


def main():
    parser = argparse.ArgumentParser(description="eSim Automated Tool Manager")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list")
    subparsers.add_parser("check")
    subparsers.add_parser("status")
    subparsers.add_parser("log")

    args = parser.parse_args()
    logger = get_logger()

    if args.command == "list":
        logger.info("Listing tools")
        list_tools()
    elif args.command == "check":
        logger.info("Checking dependencies")
        check_dependencies()
    elif args.command == "status":
        logger.info("Showing status")
        show_status()
    elif args.command == "log":
        display_log()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
