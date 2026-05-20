import arxiv
from sqlalchemy.orm import Session
from app.models.schema import Setting
from app.models.schema import Paper

def get_settings(db: Session):
    setting = db.query(Setting).first()
    if not setting:
        setting = Setting(
            categories=["cs.RO", "cs.CV"],
            keywords=["SLAM", "LiDAR"],
            max_results=5
        )
        db.add(setting)
        db.commit()
    return setting

def fetch_papers(db: Session):
    try:
        setting = get_settings(db)

        cat_query = " OR ".join([f"cat:{c}" for c in setting.categories])
        kw_query = " OR ".join(setting.keywords)
        query = f"({cat_query}) AND ({kw_query})"

        client = arxiv.Client(
            page_size=5,
            delay_seconds=3,
            num_retries=3
        )

        search = arxiv.Search(
            query=query,
            max_results=setting.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        saved_papers = []
        for result in client.results(search):
            existing = db.query(Paper).filter(
                Paper.arxiv_id == result.entry_id
            ).first()

            if existing:
                continue

            paper = Paper(
                arxiv_id=result.entry_id,
                title=result.title,
                authors=str(result.authors),
                abstract=result.summary,
                categories=result.categories,
                pdf_url=result.pdf_url,
                published_at=result.published.date()
            )
            db.add(paper)
            saved_papers.append(paper)

        db.commit()
        return len(saved_papers)

    except Exception as e:
        print(f"Error: {e}")
        return 0