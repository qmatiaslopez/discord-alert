import aiohttp
import os
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
MAX_RETRIES = 3

class WebhookError(Exception):
    """Custom exception for webhook-related errors"""
    pass

async def send_discord_webhook(message: Dict, retry_count: int = 0) -> dict:
    """
    Send formatted message to Discord webhook with retry mechanism
    """
    if not DISCORD_WEBHOOK_URL:
        raise WebhookError("Discord webhook URL not configured")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(DISCORD_WEBHOOK_URL, json=message) as response:
                if response.status == 204:
                    logger.info(f"Message sent successfully: {message['embeds'][0]['title']}")
                    return {
                        "status": response.status,
                        "success": True,
                        "message": "Message sent successfully"
                    }
                
                # Handle rate limits
                if response.status == 429 and retry_count < MAX_RETRIES:
                    retry_after = int(response.headers.get('X-RateLimit-Reset-After', 5))
                    logger.warning(f"Rate limited, retrying after {retry_after} seconds")
                    await asyncio.sleep(retry_after)
                    return await send_discord_webhook(message, retry_count + 1)
                
                error_msg = f"Failed to send message. Status: {response.status}"
                logger.error(error_msg)
                return {
                    "status": response.status,
                    "success": False,
                    "message": error_msg
                }

        except Exception as e:
            error_msg = f"Error sending webhook: {str(e)}"
            logger.error(error_msg)
            return {
                "status": 500,
                "success": False,
                "message": error_msg
            }
