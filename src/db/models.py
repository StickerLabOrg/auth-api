from sqlalchemy import Column, Integer, String
from src.db.session import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    time_do_coracao = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
