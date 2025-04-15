"""
Entry point for running the module using 'python -m slack_cloudinary_bridge'.
"""

# Use relative import to get the mcp instance from core.py within the package
from .core import mcp

if __name__ == "__main__":
    print("Running Slack-Cloudinary Bridge via __main__...")
    # Ensure necessary environment variables are set before running
    # (The check is also done within the tool, but good practice to check early)
    # import os
    # required_vars = ["BOT_TOKEN", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET", "CLOUDINARY_CLOUD_NAME"]
    # missing_vars = [var for var in required_vars if not os.environ.get(var)]
    # if missing_vars:
    #     print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    #     exit(1)
    
    # Run the FastMCP server with stdio transport
    mcp.run(transport='stdio')
