# This file marks the directory as a Python package.
# Use relative import to get the mcp instance from core.py within the package
from .slack_cloudinary_bridge import mcp

def main() -> None:
    mcp.run()