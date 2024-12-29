from fastapi import FastAPI, HTTPException
from .app.models import Message
from .app.services import ProcessService

app = FastAPI(
    title="Discord Alert Service",
    description="Service for sending notifications to Discord",
    version="1.0.0"
)

process_service = ProcessService()

@app.post(
    "/webhook",
    summary="Send notification to Discord",
    response_description="Message processing result"
)
async def receive_message(message: Message):
    """
    Endpoint to receive and process messages for Discord delivery
    
    Args:
        message (Message): The message to process and send
        
    Returns:
        dict: Message processing and delivery result
        
    Raises:
        HTTPException: If processing or delivery fails
    """
    try:
        processed_message = await process_service.process_message(
            msg_type=message.type,
            content=message.content,
            origin=message.origin,
            details=message.details,
            timestamp=message.timestamp
        )
        return processed_message
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Message processing failed: {str(e)}"
        )

@app.get(
    "/health",
    summary="Service health check",
    response_description="Health status"
)
async def health_check():
    """
    Health check endpoint to verify service status
    
    Returns:
        dict: Service health status
    """
    return {
        "status": "healthy",
        "service": "discord-alert",
        "version": "1.0.0"
    }