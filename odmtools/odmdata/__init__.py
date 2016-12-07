


from odm2api.ODMconnection import SessionFactory,  dbconnection
from odm2api.ODM2.models import _changeSchema as change_schema
from odmtools.odmdata.memory_database import MemoryDatabase
#ODM = SeriesService.ODM

from collections import OrderedDict
def returnDict():
    keys = ['ResultID', 'SamplingFeatureCode', 'SamplingFeatureName', 'MethodCode', 'MethodName', 'VariableCode', 'VariableNameCV', 'ProcessingLevelCode','ProcessingLevelDefinition', 'UnitsName', 'ValueCount', 'BeginDateTime', 'EndDateTime']
    # keys = ['SeriesID', 'SiteID', 'SiteCode', 'SiteName', 'VariableID', 'VariableCode', 'VariableName', 'Speciation',
    #         'VariableUnitsID', 'VariableUnitsName', 'SampleMedium', 'ValueType', 'TimeSupport', 'TimeUnitsID',
    #         'TimeUnitsName', 'DataType', 'GeneralCategory', 'MethodID', 'MethodDescription', 'SourceID',
    #         'SourceDescription', 'Organization', 'Citation', 'QualityControlLevelID', 'QualityControlLevelCode',
    #         'BeginDateTime', 'EndDateTime', 'BeginDateTimeUTC', 'EndDateTimeUTC', 'ValueCount'
    #         ]
    # values = ['id', 'site_id', 'site_code', 'site_name', 'variable_id', 'variable_code', 'variable_name', 'speciation',
    #           'variable_units_id', 'variable_units_name', 'sample_medium', 'value_type', 'time_support',
    #           'time_units_id', 'time_units_name', 'data_type', 'general_category', 'method_id', 'method_description',
    #           'source_id', 'source_description', 'organization', 'citation', 'quality_control_level_id',
    #           'quality_control_level_code', 'begin_date_time', 'end_date_time', 'begin_date_time_utc',
    #           'end_date_time_utc', 'value_count'
    #           ]
    return OrderedDict(zip(keys, keys))
__all__=[
        #'SessionFactory',
        'refreshDB',
        'change_schema',
        #'returnDict',
        #'ODM',
        'MemoryDatabase',
        'returnDict'
        #'SeriesService'
        'readService', 'createService', 'updateService', 'deleteService'
        'dbconnection'
         ]
