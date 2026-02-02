"""
Configure logging for the tool manager
Logs should be written to tool_manager.log
"""


import logging

def get_logger(name: str = "tool_manager"):
	"""Create and return a logger with INFO level, logging to tool_manager.log."""
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)
	if not logger.handlers:
		file_handler = logging.FileHandler("tool_manager.log")
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
	return logger

# log missing dependencies with tool name and dependency name
def log_missing_dependency(tool_name: str, dependency: str):
    logger = get_logger()
    logger.warning(f"Missing dependency for {tool_name}: {dependency}")