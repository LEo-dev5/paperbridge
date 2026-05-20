import requests
from app.core.config import settings

def send_discord(message: str):
    response = requests.post(
        settings.DISCORD_WEBHOOK_URL,
        json={"content": message}
    )
    return response.status_code