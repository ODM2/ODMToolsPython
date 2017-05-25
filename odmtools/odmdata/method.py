from sqlalchemy import Column, Integer, String
from base import Base

class Method(Base):
	__tablename__ = 'Methods'

	id 			= Column('MethodID', Integer, primary_key=True)
	description	= Column('MethodDescription', String, nullable=False)
	link		= Column('MethodLink', String)

	def __repr__(self):
		return "<Method('%s', '%s', '%s')>" % (self.id, self.description.encode("utf-8", 'ignore'), self.link.encode("utf-8", 'ignore'))