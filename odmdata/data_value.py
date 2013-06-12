# Declare a mapped class
from sqlalchemy import *
from sqlalchemy.orm import relationship
from base import Base
from site import Site
from variable import Variable
from qualifier import Qualifier
from method import Method
from source import Source
from quality_control_level import QualityControlLevel
from offset_type import OffsetType

class DataValue(Base):
	__tablename__ = 'DataValues'

	id 						 = Column('ValueID', Integer, primary_key=True)
	data_value 		    	 = Column('DataValue', Float)
	value_accuracy	    	 = Column('ValueAccuracy', Float)
	local_date_time	    	 = Column('LocalDateTime', DateTime)
	utc_offset		    	 = Column('UTCOffset', Float)
	date_time_utc			 = Column('DateTimeUTC', DateTime)
	site_id		 	    	 = Column('SiteID', Integer, ForeignKey('Sites.SiteID'), nullable=False)
	variable_id			   	 = Column('VariableID', Integer, ForeignKey('Variables.VariableID'), nullable=False)
	offset_value	    	 = Column('OffsetValue', Float)
	offset_type_id			 = Column('OffsetTypeID', Integer, ForeignKey('OffsetTypes.OffsetTypeID'))
	censor_code		    	 = Column('CensorCode', String)
	qualifier_id	    	 = Column('QualifierID', Integer, ForeignKey('Qualifiers.QualifierID'))
	method_id		    	 = Column('MethodID', Integer, ForeignKey('Methods.MethodID'), nullable=False)
	source_id		    	 = Column('SourceID', Integer, ForeignKey('Sources.SourceID'), nullable=False)
	sample_id			  	 = Column('SampleID', Integer)
	derived_from_id	    	 = Column('DerivedFromID', Integer)
	quality_control_level_id = Column('QualityControlLevelID', Integer, ForeignKey('QualityControlLevels.QualityControlLevelID'))

	# relationships
	site 				  = relationship(Site)
	variable 			  = relationship(Variable)
	qualifier 			  = relationship(Qualifier)
	method 				  = relationship(Method)
	source 				  = relationship(Source)
	quality_control_level = relationship(QualityControlLevel)
	offset_type			  = relationship(OffsetType)


	def __repr__(self):
		return "<DataValue('%s', '%s')>" % (self.data_value, self.local_date_time)

	def toTuple(self):
		pass