from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):

	__tablename__='users'
	id = Column(Integer,primary_key=True)
	password = Column(String(255))
	email = Column(String(255))

	def __init__(self,email,password):
		self.password=password
		self.email=email

engine = create_engine("sqlite:///exam3database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session=Session()