from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE='mysql+pymysql://root:TheBest#27062004@localhost:3306/orderingschema'

engine=create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind = engine)

Base = declarative_base()