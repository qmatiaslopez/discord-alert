from .output_handler import send_discord_webhook
from datetime import datetime
from typing import Optional, Dict

def format_message(
    msg_type: str,
    content: str,
    origin: str,
    details: Optional[Dict] = None,
    timestamp: datetime = None
) -> dict:
    """
    Format the message according to its type and add visual elements
    """
    formats = {
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
    
    msg_format = formats.get(msg_type.upper(), formats["INFO"])
    
    # Create fields for details if they exist
    fields = []
    if details:
        for key, value in details.items():
            fields.append({
                "name": key.replace("_", " ").title(),
                "value": str(value),  # Convert value to string and use directly
                "inline": True
            })

    return {
        "embeds": [{
            "title": f"{msg_format['title_emoji']} {msg_type.upper()} from {origin}",
            "description": f"{msg_format['symbol']} {content}",
            "color": msg_format['color'],
            "fields": fields,
            "footer": {
                "text": f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}"
            }
        }]
    }

async def process_message(
    msg_type: str,
    content: str,
    origin: str,
    details: Optional[Dict] = None,
    timestamp: datetime = None
) -> dict:
    """
    Process the message and send it to Discord
    """
    formatted_message = format_message(
        msg_type=msg_type,
        content=content,
        origin=origin,
        details=details,
        timestamp=timestamp
    )
    response = await send_discord_webhook(formatted_message)
    return response
