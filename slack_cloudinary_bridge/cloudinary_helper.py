import cloudinary
import cloudinary.uploader
import httpx
import os

async def upload_to_cloudinary(image_bytes: bytes) -> str:
    """
    Uploads image bytes to Cloudinary using credentials from env vars and returns the public URL.
    
    Args:
        image_bytes (bytes): The image content in bytes. 
        
    Returns:
        str: The public URL of the uploaded image.
        
    Raises:
        ValueError: If required Cloudinary environment variables are not set.
    """
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")

    if not all([api_key, api_secret, cloud_name]):
        missing = []
        if not api_key: missing.append("CLOUDINARY_API_KEY")
        if not api_secret: missing.append("CLOUDINARY_API_SECRET")
        if not cloud_name: missing.append("CLOUDINARY_CLOUD_NAME")
        raise ValueError(f"Missing Cloudinary environment variables: {', '.join(missing)}")

    # Note: Consider configuring Cloudinary once globally instead of per-call if possible.
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    # Note: This uses synchronous cloudinary upload. Consider asyncio.to_thread for async.
    result = cloudinary.uploader.upload(image_bytes)
    if not result or "secure_url" not in result:
        # Or raise a custom exception
        raise RuntimeError(f"Cloudinary upload failed or did not return a secure_url. Result: {result}") 
    return result["secure_url"]