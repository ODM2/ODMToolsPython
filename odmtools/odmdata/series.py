from collections import OrderedDict # Requires Python 2.7 >=

from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship

from base import Base
from site import Site
from variable import Variable
from method import Method
from source import Source
from quality_control_level import QualityControlLevel

def copy_series(from_series):
    new = Series()
    new.site_id = from_series.site_id
    new.site_code = from_series.site_code
    new.site_name = from_series.site_name
    new.variable_id = from_series.variable_id
    new.variable_code = from_series.variable_code
    new.variable_name = from_series.variable_name
    new.speciation = from_series.speciation
    new.variable_units_id = from_series.variable_units_id
    new.variable_units_name = from_series.variable_units_name
    new.sample_medium = from_series.sample_medium
    new.value_type = from_series.value_type
    new.time_support = from_series.time_support
    new.time_units_id = from_series.time_units_id
    new.time_units_name = from_series.time_units_name
    new.data_type = from_series.data_type
    new.general_category = from_series.general_category
    new.method_id = from_series.method_id
    new.method_description = from_series.method_description
    new.source_id = from_series.source_id
    new.source_description = from_series.source_description
    new.organization = from_series.organization
    new.citation = from_series.citation
    new.quality_control_level_id = from_series.quality_control_level_id
    new.quality_control_level_code = from_series.quality_control_level_code
    new.begin_date_time = from_series.begin_date_time
    new.begin_date_time_utc = from_series.begin_date_time_utc
    new.end_date_time_utc = from_series.end_date_time_utc
    new.value_count = from_series.value_count
    return new
class Series(Base):
    __tablename__ = 'seriescatalog'

    id =                            Column('SeriesID', Integer, primary_key=True)
    site_id =                       Column('SiteID', Integer, ForeignKey('Sites.SiteID'), nullable=False)
    site_code =                     Column('SiteCode', String)
    site_name =                     Column('SiteName', String)
    variable_id =                   Column('VariableID', Integer, ForeignKey('Variables.VariableID'), nullable=False)
    variable_code =                 Column('VariableCode', String)
    variable_name =                 Column('VariableName', String)

    speciation =                    Column('Speciation', String)
    variable_units_id =             Column('VariableUnitsID', Integer)
    variable_units_name =           Column('VariableUnitsName', String)
    sample_medium =                 Column('SampleMedium', String)
    value_type =                    Column('ValueType', String)
    time_support =                  Column('TimeSupport', Float)
    time_units_id =                 Column('TimeUnitsID', Integer)
    time_units_name =               Column('TimeUnitsName', String)
    data_type =                     Column('DataType', String)
    general_category =              Column('GeneralCategory', String)
    method_id =                     Column('MethodID', Integer, ForeignKey('Methods.MethodID'), nullable=False)
    method_description =            Column('MethodDescription', String)
    source_id =                     Column('SourceID', Integer, ForeignKey('Sources.SourceID'), nullable=False)
    source_description =            Column('SourceDescription', String)
    organization =                  Column('Organization', String)
    citation =                      Column('Citation', String)
    quality_control_level_id =      Column('QualityControlLevelID', Integer,
                                           ForeignKey('QualityControlLevels.QualityControlLevelID'), nullable=False)
    quality_control_level_code =    Column('QualityControlLevelCode', String)
    begin_date_time =               Column('BeginDateTime', DateTime)
    end_date_time =                 Column('EndDateTime', DateTime)
    begin_date_time_utc =           Column('BeginDateTimeUTC', DateTime)
    end_date_time_utc =             Column('EndDateTimeUTC', DateTime)
    value_count =                   Column('ValueCount', Integer)

    data_values = relationship("DataValue",
                               primaryjoin="and_(DataValue.site_id == Series.site_id, "
                                           "DataValue.variable_id == Series.variable_id, "
                                           "DataValue.method_id == Series.method_id, "
                                           "DataValue.source_id == Series.source_id, "
                                           "DataValue.quality_control_level_id == Series.quality_control_level_id)",
                               foreign_keys="[DataValue.site_id, DataValue.variable_id, DataValue.method_id, DataValue.source_id, DataValue.quality_control_level_id]",
                               order_by="DataValue.local_date_time",
                               backref="series")

    site = relationship(Site)
    variable = relationship(Variable)
    method = relationship(Method)
    source = relationship(Source)
    quality_control_level = relationship(QualityControlLevel)


    def __repr__(self):
        return "<Series('%s', '%s', '%s', '%s')>" % (self.id, self.site_name, self.variable_code, self.variable_name)

    def __eq__(self, other) :
        # return self.__dict__ == other.__dict__
        return [self.id, self.site_id, self.site_code, self.site_name, self.variable_id, self.variable_code,
                self.variable_name, self.speciation, self.variable_units_id, self.variable_units_name,
                self.sample_medium, self.value_type, self.time_support, self.time_units_id, self.time_units_name,
                self.data_type, self.general_category, self.method_id, self.method_description,
                self.source_id, self.source_description, self.organization, self.citation,
                self.quality_control_level_id, self.quality_control_level_code, self.begin_date_time,
                self.end_date_time, self.begin_date_time_utc, self.end_date_time_utc, self.value_count] ==\
               [other.id, other.site_id, other.site_code, other.site_name, other.variable_id, other.variable_code,
                other.variable_name, other.speciation, other.variable_units_id, other.variable_units_name,
                other.sample_medium, other.value_type, other.time_support, other.time_units_id, other.time_units_name,
                other.data_type, other.general_category, other.method_id, other.method_description,
                other.source_id, other.source_description, other.organization, other.citation,
                other.quality_control_level_id, other.quality_control_level_code, other.begin_date_time,
                other.end_date_time, other.begin_date_time_utc, other.end_date_time_utc, other.value_count]


    def get_table_columns(self):
        return self.__table__.columns.keys()

    def list_repr(self):
        return [self.id, self.site_code, self.variable_code, self.quality_control_level_code,
                self.site_id,  self.site_name, self.variable_id,
                self.variable_name, self.speciation, self.variable_units_id, self.variable_units_name,
                self.sample_medium, self.value_type, self.time_support, self.time_units_id, self.time_units_name,
                self.data_type, self.general_category, self.method_id, self.method_description,
                self.source_id, self.source_description, self.organization, self.citation,
                self.quality_control_level_id,  self.begin_date_time,
                self.end_date_time, self.begin_date_time_utc, self.end_date_time_utc, self.value_count]

def returnDict():
    keys = ['SeriesID', 'SiteCode','VariableCode','QualityControlLevelCode',
            'SiteID',  'SiteName', 'VariableID',  'VariableName', 'Speciation',
            'VariableUnitsID', 'VariableUnitsName', 'SampleMedium', 'ValueType', 'TimeSupport', 'TimeUnitsID',
            'TimeUnitsName', 'DataType', 'GeneralCategory', 'MethodID', 'MethodDescription', 'SourceID',
            'SourceDescription', 'Organization', 'Citation', 'QualityControlLevelID',
            'BeginDateTime', 'EndDateTime', 'BeginDateTimeUTC', 'EndDateTimeUTC', 'ValueCount'
    ]
    values = ['id', 'site_code','variable_code','quality_control_level_code',
              'site_id',  'site_name', 'variable_id',  'variable_name', 'speciation',
              'variable_units_id', 'variable_units_name', 'sample_medium', 'value_type', 'time_support',
              'time_units_id', 'time_units_name', 'data_type', 'general_category', 'method_id', 'method_description',
              'source_id', 'source_description', 'organization', 'citation', 'quality_control_level_id',
               'begin_date_time', 'end_date_time', 'begin_date_time_utc',
              'end_date_time_utc', 'value_count'
    ]
    return OrderedDict(zip(keys, values))



