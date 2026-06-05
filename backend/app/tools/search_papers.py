import arxiv

def search_papers(query: str, categories: list) -> str:
    cat_query = " OR ".join([f"cat:{c}" for c in categories])
    full_query = f"({cat_query}) AND ({query})"

    client = arxiv.Client(
        page_size=5,
        delay_seconds=3,
        num_retries=3
    )

    search = arxiv.Search(
        query=full_query,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = []
    for paper in client.results(search):
        results.append(
            f"제목: {paper.title}\n"
            f"ID: {paper.entry_id}\n"
            f"초록: {paper.summary[:500]}\n"
        )

    return "\n---\n".join(results) if results else "검색 결과 없음"