from mcp.server.fastmcp import FastMCP
from .slack_helper import download_slack_image
from .cloudinary_helper import upload_to_cloudinary
import os

mcp = FastMCP("Slack to Cloudinary Uploader")

# Helper function to check for required environment variables
def check_env_vars(*vars):
    missing = [var for var in vars if not os.environ.get(var)]
    if missing:
        return f"Error: Missing required environment variables: {', '.join(missing)}"
    return None

@mcp.tool()
async def upload_slack_image(slack_url: str) -> str:
    """
    Downloads an image from a Slack private URL and uploads it to Cloudinary.
    Reads required credentials (BOT_TOKEN, CLOUDINARY_*) from environment variables.
    
    Args:
        slack_url (str): The private Slack image URL.
        
    Returns:
        str: The public URL of the uploaded image on Cloudinary, or an error message.
    """
    # Check for environment variables first
    env_error = check_env_vars("BOT_TOKEN", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET", "CLOUDINARY_CLOUD_NAME")
    if env_error:
        return env_error

    try:
        # Download the image asynchronously (but internally uses sync requests)
        image_bytes = await download_slack_image(slack_url)
        # The helper now raises ValueError if token is missing, 
        # but the check above provides a better initial message.
        # We might catch exceptions from download_slack_image more specifically if needed.
        
        # Upload the image asynchronously (but internally uses sync cloudinary)
        public_url = await upload_to_cloudinary(image_bytes)
        # The helper now raises ValueError/RuntimeError if config/upload fails.

        return public_url
        
    except ValueError as e:
        # Catch errors from missing env vars within helpers (redundant but safe)
        # Or other ValueErrors raised by the helpers
        return f"Configuration Error: {e}"
    except RuntimeError as e:
        # Catch upload errors from cloudinary_helper
        return f"Upload Error: {e}"
    except Exception as e:
        # Catch other potential exceptions (e.g., network errors from requests)
        # Log the full error for debugging in a real app
        print(f"An unexpected error occurred: {e}") 
        return f"An unexpected error occurred. Check logs."

# if __name__ == "__main__":
#     mcp.run(transport='stdio')