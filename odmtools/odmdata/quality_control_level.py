from sqlalchemy import Column, String, Integer
from base import Base

class QualityControlLevel(Base):
	__tablename__ = 'QualityControlLevels'

	id 			= Column('QualityControlLevelID', Integer, primary_key=True)
	code		= Column('QualityControlLevelCode', String, nullable=False)
	definition  = Column('Definition', String, nullable=False)
	explanation = Column('Explanation', String, nullable=False)

	def __repr__(self):
		return "<QualityControlLevel('%s', '%s', '%s', '%s')>" % (self.id, self.code, self.definition, self.explanation)