from sqlalchemy import Column, String
from base import Base

class VariableNameCV(Base):
	__tablename__ = 'VariableNameCV'

	term   	   = Column('Term', String, primary_key=True)
	definition = Column('Definition', String)

	def __repr__(self):
		return "<VariableNameCV('%s', '%s')>" % (self.term, self.definition)