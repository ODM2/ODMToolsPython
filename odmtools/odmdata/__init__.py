





#from api.versionSwitcher import ODM, refreshDB


# DataTypeCV=ODM.DataTypeCV
# DataValue=ODM.DataValue
# # GeneralCategoryCV=ODM.GeneralCategoryCV
# ISOMetadata=ODM.ISOMetadata
# LabMethod=ODM.LabMethod
# Method=ODM.Method
# OffsetType=ODM.OffsetType
# Qualifier=ODM.Qualifier
# QualityControlLevel=ODM.QualityControlLevel
# Sample =ODM.Sample
# SampledMediumCV= ODM.SampleMediumCV
# # SampleTypeCV=ODM.SampleTypeCV
# Series=ODM.Series
# Site= ODM.Site
# SiteType=ODM.SiteTypeCV
# Source =ODM.Source
# SpatialReferences=ODM.SpatialReference
# SpeciationCV=ODM.SpeciationCV
# # TopicCategoryCV=ODM.TopicCategoryCV
# Unit= ODM.Unit
# # ValueTypeCV=ODM.ValueTypeCV
# Variable = ODM.Variable
# VerticalDatumCV=ODM.VerticalDatumCV
# returnDict = ODM.returnDict
from api.ODM1_1_1.services.series_service import ODM#, refreshDB
from api.ODMconnection import SessionFactory
from api.ODM2.models import change_schema
from odmtools.odmdata.memory_database import MemoryDatabase


from collections import OrderedDict
def returnDict():
    keys = ['SeriesID', 'SiteID', 'SiteCode', 'SiteName', 'VariableID', 'VariableCode', 'VariableName', 'Speciation',
            'VariableUnitsID', 'VariableUnitsName', 'SampleMedium', 'ValueType', 'TimeSupport', 'TimeUnitsID',
            'TimeUnitsName', 'DataType', 'GeneralCategory', 'MethodID', 'MethodDescription', 'SourceID',
            'SourceDescription', 'Organization', 'Citation', 'QualityControlLevelID', 'QualityControlLevelCode',
            'BeginDateTime', 'EndDateTime', 'BeginDateTimeUTC', 'EndDateTimeUTC', 'ValueCount'
            ]
    values = ['id', 'site_id', 'site_code', 'site_name', 'variable_id', 'variable_code', 'variable_name', 'speciation',
              'variable_units_id', 'variable_units_name', 'sample_medium', 'value_type', 'time_support',
              'time_units_id', 'time_units_name', 'data_type', 'general_category', 'method_id', 'method_description',
              'source_id', 'source_description', 'organization', 'citation', 'quality_control_level_id',
              'quality_control_level_code', 'begin_date_time', 'end_date_time', 'begin_date_time_utc',
              'end_date_time_utc', 'value_count'
              ]
    return OrderedDict(zip(keys, values))
__all__=[
        'SessionFactory',
        'refreshDB',
        'change_schema',
        'returnDict',
        'ODM',
        'MemoryDatabase',
        'returnDict'
         ]
