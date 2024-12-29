from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field
from typing import Optional, Dict
from datetime import datetime, timezone
import enum
import json

class MessageType(str, enum.Enum):
    """
    Enumeration of allowed message types
    """
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    SUCCESS = "SUCCESS"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"

class Message(BaseModel):
    """
    Model representing a message to be processed and sent to Discord
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "type": "INFO",
                    "content": "User login successful",
                    "origin": "auth_service",
                    "details": {
                        "user_id": "123",
                        "ip": "192.168.1.1"
                    }
                }
            ]
        }
    )

    type: MessageType
    content: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The main content of the message"
    )
    origin: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The system or service that generated the message"
    )
    details: Optional[Dict] = Field(
        default=None,
        description="Additional contextual information about the message"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the message was created"
    )

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()

    @field_validator('origin')
    @classmethod
    def validate_origin(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message origin cannot be empty")
        return v.strip()

    @computed_field
    def formatted_timestamp(self) -> str:
        """Return ISO formatted timestamp string"""
        return self.timestamp.isoformat()

    def model_dump_json(self, **kwargs) -> str:
        """
        Custom JSON serialization that ensures datetime is properly handled
        """
        data = self.model_dump()
        data['timestamp'] = self.timestamp.isoformat()
        return json.dumps(data)