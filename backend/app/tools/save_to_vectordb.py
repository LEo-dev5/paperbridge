import chromadb
from chromadb.utils import embedding_functions
from sqlalchemy.orm import Session
from app.models.schema import Paper

def save_to_vectordb(paper_id: int, db: Session) -> str:
    paper = db.query(Paper).filter(Paper.id == paper_id).first()

    if not paper:
        return f"논문을 찾을 수 없습니다: {paper_id}"

    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="paper_collector",
        embedding_function=sentence_transformer_ef
    )

    existing = collection.get(ids=[str(paper.id)])
    if existing["ids"]:
        return "이미 벡터화된 논문입니다."

    collection.add(
        documents=[paper.abstract],
        metadatas=[{
            "paper_id": str(paper.id),
            "title": paper.title,
            "arxiv_id": paper.arxiv_id
        }],
        ids=[str(paper.id)]
    )

    paper.is_vectorized = True
    db.commit()

    return "벡터화 완료"