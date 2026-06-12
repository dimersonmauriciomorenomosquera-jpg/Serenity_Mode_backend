from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql



engine = create_engine("mysql+pymysql://root@localhost:3306/serenitymode?charset=utf8mb4")

connetion = engine.connect()

Session = sessionmarker(bind-engine)

session = Session()

Base = declarative_base()
Base.metadata.bind = engine