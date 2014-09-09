from sqlalchemy import Column, String
from base import Base

class TopicCategoryCV(Base):
	__tablename__ = 'TopicCategoryCV'

	term   	   = Column('Term', String, primary_key=True)
	definition = Column('Definition', String)

	def __repr__(self):
		return "<TopicCategoryCV('%s', '%s')>" % (self.term, self.definition)