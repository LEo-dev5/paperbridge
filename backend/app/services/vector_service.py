import chromadb
from chromadb.utils import embedding_functions
from sqlalchemy.orm import Session
from app.models.schema import Paper

def get_collection():
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(
        name="paper_collector",
        embedding_function=sentence_transformer_ef
    )

def vectorize_papers(db: Session):
    collection = get_collection()
    papers = db.query(Paper).filter(
        Paper.is_vectorized == False
    ).all()

    if not papers:
        return
    
    for paper in papers:
        existing = collection.get(ids=[str(paper.id)])
        if existing['ids']:
            paper.is_vectorized = True
            continue

        collection.add(
            documents=[paper.abstract],
            metadatas=[{
                "paper_id": str(paper.id),
                "title": paper.title,
                "arxiv_id": paper.arxiv_id,
            }],
            ids=[str(paper.id)]
        )
        paper.is_vectorized = True
    db.commit()