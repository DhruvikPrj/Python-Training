from sqlmodel import SQLModel, create_engine

# Create SQLite database file named "users.db"
DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL logs

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
