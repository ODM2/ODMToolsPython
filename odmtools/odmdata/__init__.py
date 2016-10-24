<<<<<<< HEAD
=======
from base import Base
from censor_code_cv import CensorCodeCV
from data_type_cv import DataTypeCV
from data_value import DataValue
from general_category_cv import GeneralCategoryCV
from iso_metadata import ISOMetadata
from lab_method import LabMethod
from method import Method
from odm_version import ODMVersion
from offset_type import OffsetType
from qualifier import Qualifier
from quality_control_level import QualityControlLevel
from sample import Sample
from sample_medium_cv import SampleMediumCV
from sample_type_cv import SampleTypeCV
from series import Series
from odm2api.ODMconnection import SessionFactory
from site import Site
from site_type_cv import SiteTypeCV
from source import Source
from spatial_reference import SpatialReference
from speciation_cv import SpeciationCV
from topic_category_cv import TopicCategoryCV
from unit import Unit
from value_type_cv import ValueTypeCV
from variable import Variable
from variable_name_cv import VariableNameCV
from vertical_datum_cv import VerticalDatumCV
from memory_database import MemoryDatabase
>>>>>>> origin/update_cvs



#from odm2api.ODM1_1_1.services import SeriesService#, refreshDB

from odm2api.ODMconnection import SessionFactory,  dbconnection
from odm2api.ODM2.models import _changeSchema as change_schema
from odmtools.odmdata.memory_database import MemoryDatabase
#ODM = SeriesService.ODM

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
        #'SessionFactory',
        'refreshDB',
        'change_schema',
        'returnDict',
        #'ODM',
        'MemoryDatabase',
        'returnDict'
        #'SeriesService'
        'readService', 'createService', 'updateService', 'deleteService'
        'dbconnection'
         ]
