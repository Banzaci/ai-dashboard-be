uvicorn app.main:app --reload


python -m app.db.init_db


CREATE EXTENSION IF NOT EXISTS vector; för vector db