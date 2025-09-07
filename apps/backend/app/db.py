from sqlmodel import SQLModel, create_engine, Session

# SQLite file at ./data/app.db (relative to backend folder)
DATABASE_URL = "sqlite:///./data/app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
