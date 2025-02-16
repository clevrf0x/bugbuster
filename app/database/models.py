from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class XSSComment(Base):
    __tablename__ = "xss_comments"
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    level = Column(Integer, nullable=False)  # New field to store the level (1, 2, or 3)
