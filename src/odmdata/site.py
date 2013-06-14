# Declare a mapped class
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from base import Base
from spatial_reference import SpatialReference

class Site(Base):
	__tablename__ = 'Sites'

	id 					= Column('SiteID', Integer, primary_key=True)
	site_code 		    = Column('SiteCode', String)
	site_name 		    = Column('SiteName', String)
	latitude  		    = Column('Latitude', Float)
	longitude			= Column('Longitude', Float)
	lat_long_datum_id   = Column('LatLongDatumID', Integer, ForeignKey('SpatialReferences.SpatialReferenceID'))
	elevation_m 	    = Column('Elevation_m', Float)
	vertical_datum_id   = Column('VerticalDatum', Integer)
	local_x			    = Column('LocalX', Float)
	local_y			    = Column('LocalY', Float)
	local_projection_id = Column('LocalProjectionID', Integer)
	pos_accuracy_m	    = Column('PosAccuracy_m', Float)
	state			    = Column('State', String)
	county			    = Column('County', String)
	comments		    = Column('Comments', String)

	site_type			= Column('SiteType', String)

	# relationships
	spatial_reference = relationship(SpatialReference, primaryjoin=("SpatialReference.id==Site.lat_long_datum_id"))

	def __init__(self, site_code, site_name):
		self.site_code = site_code
		self.site_name = site_name

	def __repr__(self):
		return "<Site('%s', '%s')>" % (self.site_code, self.site_name)