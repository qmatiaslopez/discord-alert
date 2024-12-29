import aiohttp
import os
import asyncio
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebhookError(Exception):
    """Custom exception for webhook-related errors"""
    pass

class OutputService:
    """
    Service responsible for sending messages to Discord
    """
    
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        self.max_retries = 3
        
        if not self.webhook_url:
            logger.error("Discord webhook URL not configured")
            raise WebhookError("Discord webhook URL not configured")

    async def send_discord_webhook(self, message: Dict, retry_count: int = 0) -> dict:
        """
        Sends formatted message to Discord webhook with retry mechanism
        
        Args:
            message: Formatted message to send
            retry_count: Current retry attempt number
            
        Returns:
            Dict containing the response status and details
            
        Raises:
            WebhookError: If sending fails after all retries
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.webhook_url, json=message) as response:
                    # Successful response
                    if response.status == 204:
                        logger.info(
                            f"Message sent successfully: {message['embeds'][0]['title']}"
                        )
                        return {
                            "status": response.status,
                            "success": True,
                            "message": "Message sent successfully"
                        }
                    
                    # Handle rate limits
                    if response.status == 429 and retry_count < self.max_retries:
                        retry_after = int(response.headers.get('X-RateLimit-Reset-After', 5))
                        logger.warning(f"Rate limited, retrying after {retry_after} seconds")
                        await asyncio.sleep(retry_after)
                        return await self.send_discord_webhook(message, retry_count + 1)
                    
                    # Handle other errors
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
                
                # Retry on connection errors
                if retry_count < self.max_retries:
                    logger.info(f"Retrying... Attempt {retry_count + 1}")
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                    return await self.send_discord_webhook(message, retry_count + 1)
                
                return {
                    "status": 500,
                    "success": False,
                    "message": error_msg
                }