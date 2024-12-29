from datetime import datetime
from typing import Optional, Dict
from .input import InputService
from .output import OutputService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessService:
    """
    Service responsible for message processing and formatting
    """
    
    # Message format configurations
    MESSAGE_FORMATS = {
        "INFO": {
            "symbol": "ℹ️",
            "color": 0x3498db,
            "title_emoji": "📢"
        },
        "ERROR": {
            "symbol": "⚠️",
            "color": 0xe74c3c,
            "title_emoji": "❌"
        },
        "WARNING": {
            "symbol": "⚡",
            "color": 0xf1c40f,
            "title_emoji": "⚠️"
        },
        "SUCCESS": {
            "symbol": "✅",
            "color": 0x2ecc71,
            "title_emoji": "🎉"
        },
        "DEBUG": {
            "symbol": "🔍",
            "color": 0x95a5a6,
            "title_emoji": "🐛"
        },
        "CRITICAL": {
            "symbol": "🚨",
            "color": 0x992d22,
            "title_emoji": "💀"
        }
    }

    def __init__(self):
        """Initialize the ProcessService with input and output services"""
        self.input_service = InputService()
        self.output_service = OutputService()

    def _format_message(
        self,
        msg_type: str,
        content: str,
        origin: str,
        details: Optional[Dict] = None,
        timestamp: datetime = None
    ) -> dict:
        """
        Formats the message according to its type with visual elements
        
        Args:
            msg_type: Type of message (INFO, ERROR, etc.)
            content: Main message content
            origin: Source of the message
            details: Additional contextual details
            timestamp: Message timestamp
            
        Returns:
            dict: Formatted message ready for Discord webhook
        """
        msg_format = self.MESSAGE_FORMATS.get(
            msg_type.upper(),
            self.MESSAGE_FORMATS["INFO"]
        )
        
        # Format details into fields if present
        fields = []
        if details:
            fields = [
                {
                    "name": key.replace("_", " ").title(),
                    "value": str(value),
                    "inline": True
                }
                for key, value in details.items()
            ]

        # Ensure timestamp is present
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S UTC') if timestamp else \
                            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        # Create the formatted message
        return {
            "embeds": [{
                "title": f"{msg_format['title_emoji']} {msg_type.upper()} from {origin}",
                "description": f"{msg_format['symbol']} {content}",
                "color": msg_format['color'],
                "fields": fields,
                "footer": {
                    "text": f"Timestamp: {formatted_timestamp}"
                }
            }]
        }

    async def process_message(
        self,
        msg_type: str,
        content: str,
        origin: str,
        details: Optional[Dict] = None,
        timestamp: datetime = None
    ) -> dict:
        """
        Processes and sends the message to Discord
        
        Args:
            msg_type: Type of message
            content: Message content
            origin: Source of the message
            details: Additional details
            timestamp: Message timestamp
            
        Returns:
            dict: Processing result including status
            
        Raises:
            Exception: If processing or sending fails
        """
        try:
            # Validate input data
            validated_data = await self.input_service.validate_message_data(
                msg_type=msg_type,
                content=content,
                origin=origin,
                details=details,
                timestamp=timestamp
            )
            
            # Convert 'type' to 'msg_type' for format_message
            if 'type' in validated_data:
                validated_data['msg_type'] = validated_data.pop('type')
            
            # Format the message for Discord
            formatted_message = self._format_message(**validated_data)
            
            # Send to Discord and get response
            response = await self.output_service.send_discord_webhook(formatted_message)
            
            # Log success if appropriate
            if response.get('success'):
                logger.info(f"Message processed and sent successfully from {origin}")
            
            return response
            
        except Exception as e:
            # Log the error and re-raise
            error_msg = f"Message processing failed: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)