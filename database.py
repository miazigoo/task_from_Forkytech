from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker


SQL_DB_URL = "sqlite:///./my.db"
engine = create_engine(
    SQL_DB_URL,
    connect_args={"check_same_thread": False}
)

new_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
