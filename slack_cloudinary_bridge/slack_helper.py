import requests
import os

async def download_slack_image(slack_url: str) -> bytes:
    """
    Downloads an image from a Slack private URL using the bot token from env vars.
    
    Args:
        slack_url (str): The private Slack image URL.
    
    Returns:
        bytes: The image content in bytes.
        
    Raises:
        ValueError: If the BOT_TOKEN environment variable is not set.
    """
    slack_token = os.environ.get("BOT_TOKEN")
    if not slack_token:
        raise ValueError("BOT_TOKEN environment variable not set.")
        
    headers = {
        "Authorization": f"Bearer {slack_token}"
    }
    # Note: This still uses synchronous requests. Consider httpx for async.
    response = requests.get(slack_url, headers=headers)
    response.raise_for_status() # Raises exceptions for 4xx/5xx responses
    return response.content