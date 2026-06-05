import anthropic
from app.core.config import settings
from app.agent.tools import tools
from app.agent.prompts import get_system_prompt
from app.services.arxiv_service import get_settings
from app.tools.search_papers import search_papers
from app.tools.get_paper_content import get_paper_content
from app.tools.search_vectordb import search_vectordb
from app.tools.save_to_vectordb import save_to_vectordb
from app.tools.update_categories import update_categories
from sqlalchemy.orm import Session

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def execute_tool(tool_name: str, tool_input: dict, db: Session) -> str:
    if tool_name == "search_papers":
        return search_papers(tool_input["query"], tool_input["categories"])
    elif tool_name == "get_paper_content":
        return get_paper_content(tool_input["arxiv_id"], db)
    elif tool_name == "search_vectordb":
        return search_vectordb(tool_input["query"])
    elif tool_name == "save_to_vectordb":
        return save_to_vectordb(tool_input["paper_id"], db)
    elif tool_name == "update_categories":
        return update_categories(tool_input["categories"], tool_input["keywords"], db)
    return "알 수 없는 도구입니다."

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
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input, db)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })

            messages.append({"role": "user", "content": tool_results})

        else:
            return response.content[0].text