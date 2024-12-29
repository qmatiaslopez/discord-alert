from typing import Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InputService:
    """
    Service responsible for initial message validation and preparation
    """
    
    @staticmethod
    async def validate_message_data(
        msg_type: str,
        content: str,
        origin: str,
        details: Optional[Dict] = None,
        timestamp: datetime = None
    ) -> Dict:
        """
        Validates and prepares the incoming message data
        
        Args:
            msg_type: Type of the message
            content: Main message content
            origin: Source system/service
            details: Additional message details
            timestamp: Message creation time
            
        Returns:
            Dict containing validated message data
            
        Raises:
            ValueError: If validation fails
        """
        try:
            # Basic validation
            if not content or not content.strip():
                raise ValueError("Content cannot be empty")
                
            if not origin or not origin.strip():
                raise ValueError("Origin cannot be empty")
            
            # Prepare message data
            message_data = {
                "type": msg_type.upper(),
                "content": content.strip(),
                "origin": origin.strip(),
                "details": details or {},
                "timestamp": timestamp or datetime.utcnow()
            }
            
            logger.info(f"Message validated successfully from {origin}")
            return message_data
            
        except Exception as e:
            logger.error(f"Message validation failed: {str(e)}")
            raise ValueError(f"Message validation failed: {str(e)}")