from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class SessionFactory():
	def __init__(self, connection_string, echo):
	
		self.engine = create_engine(connection_string, encoding='utf-8', echo=echo)

		# Create session maker
		self.Session = sessionmaker(bind=self.engine)

	def get_session(self):
		return self.Session()

	def __repr__(self):
		return "<SessionFactory('%s')>" % (self.engine)


# for testing
if (__name__ == "__main__"):
	sf = SessionFactory()
	# print sf