import chromadb
from chromadb.utils import embedding_functions

def search_vectordb(query: str) -> str:
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="paper_collector",
        embedding_function=sentence_transformer_ef
    )

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    if not results["documents"][0]:
        return "관련 논문을 찾을 수 없습니다."

    output = []
    for i, doc in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        output.append(
            f"제목: {metadata.get('title', '없음')}\n"
            f"내용: {doc[:500]}\n"
        )

    return "\n---\n".join(output)