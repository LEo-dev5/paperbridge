
tools = [
    {
        "name": "search_papers",
        "description": "arXiv에서 논문 검색",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색어"},
                "categories": {"type": "array", "items": {"type": "string"}, "description": "arXiv 카테고리 리스트 (예: cs.AI, cs.CL)"}
            },
            "required": ["query", "categories"]
        }
    },
    {
        "name": "get_paper_content",
        "description": "특정 논문 상세 내용 가져오기",
        "input_schema": {
            "type": "object",
            "properties": {
                "arxiv_id": {"type": "string", "description" : "arXiv 논문 ID"},
            },
            "required": ["arxiv_id"]
        }
    },
    {
        "name": "search_vectordb",
        "description": "ChromaDB에서 유사한 논문 검색 (RAG용)",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"]
        }
    },
    {
        "name": "save_to_vectordb",
        "description": "논문을 ChromaDB에 벡터화해서 저장",
        "input_schema": {
            "type": "object",
            "properties": {
                "paper_id": {"type": "integer", "description": "논문"},
            },
            "required": ["paper_id"]
        }
    },
   {
        "name": "update_categories",
        "description": "settings 테이블의 카테고리/키워드 변경",
        "input_schema": {
            "type": "object",
            "properties": {
                "categories": {"type": "array", "items": {"type": "string"}, "description": "arXiv 카테고리 리스트 (예: cs.AI, cs.CL)"},
                "keywords": {"type": "array", "items": {"type": "string"}, "description": "논문 키워드 리스트"}
            },
            "required": ["categories", "keywords"]
        }
    },
]
