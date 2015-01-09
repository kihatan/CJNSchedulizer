from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


engine = create_engine(os.environ["DATABASE_URL"], echo=True)
Base = declarative_base()


class Show(Base):
    __tablename__ = 'shows'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    type = Column(String())
    start = Column(Integer)
    finish = Column(Integer)
    location = Column(String())
    person1 = Column(String())
    person2 = Column(String())
    link = Column(String())


class Login(Base):
    __tablename__ = 'login'

    username = Column(String(), primary_key=True)
    password = Column(String())
    

Session = sessionmaker(bind=engine)
session = Session()


