from sqlalchemy import Column, Integer, String, Numeric
from app.database import Base

class Videogame(Base):
    __tablename__ = "videogames"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    genre = Column(String(100), nullable=False)
    platform = Column(String(100), nullable=False)
    release_year = Column(Integer, nullable=False)
    rating = Column(Numeric(3, 1), nullable=False)
    developer = Column(String(150), nullable=False)
