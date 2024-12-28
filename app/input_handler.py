from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from .processor import process_message
from datetime import datetime

app = FastAPI(title="Notification System")

class Message(BaseModel):
    type: str
    content: str
    origin: str
    details: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "type": "INFO",
                "content": "User login successful",
                "origin": "auth_service",
                "details": {
                    "user_id": "123",
                    "ip": "192.168.1.1"
                }
            }]
        }
    }

@app.post("/webhook", summary="Send notification to Discord")
async def receive_message(message: Message):
    try:
        processed_message = await process_message(
            msg_type=message.type,
            content=message.content,
            origin=message.origin,
            details=message.details,
            timestamp=message.timestamp
        )
        return processed_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
