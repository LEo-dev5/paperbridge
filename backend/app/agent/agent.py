import anthropic
from app.core.config import settings
from app.agent.tools import tools
from app.agent.prompts import get_system_prompt
from app.services.arxiv_service import get_settings
from sqlalchemy.orm import Session

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def run_agent(query: str, db: Session) -> str:

    setting = get_settings(db)
    system_prompt = get_system_prompt(setting.categories, setting.keywords)

    messages = [{"role": "user", "content": query}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=system_prompt,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason == "tool_use":

            pass
        else:

            break