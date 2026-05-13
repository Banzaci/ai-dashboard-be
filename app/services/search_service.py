from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.intent_router import route_intent
from app.services.embedding_service import embed


from sqlalchemy import text
from sqlalchemy.orm import Session
from app.services.embedding_service import embed


from sqlalchemy import text
from sqlalchemy.orm import Session
from app.services.embedding_service import embed


def search_training_questions(db: Session, query: str):

    query_embedding = embed(query)

    result = db.execute(
        text("""
            SELECT question, intent, embedding <-> CAST(:embedding AS vector) AS distance
            FROM training_questions
            ORDER BY distance
            LIMIT 1
        """),
        {"embedding": query_embedding}
    ).fetchone()

    print(f"Search result: {result}")

    if not result:
        return None

    # threshold (justera senare)
    if result.distance > 0.8:
        return None

    return {
        "question": result.question,
        "intent": result.intent,
        "distance": result.distance
    }