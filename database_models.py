from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Column, Integer, String, Float

Base = declarative_base()

class Books(Base):

    __tablename__="books"

    name = Column(String)
    author = Column(String)
    status = Column(String)
    borrower = Column(String)