import datetime
import pandas as pd
from odmtools.odmdata import *
import os
import sys
from odm2api.ODM2.models import *
from odm2api.ODM2.services.readService import DetailedResult


def build_db(engine):
    Base.metadata.create_all(engine)


# Create DB objects #

def add_bulk_data_values(session, series, dvs_size):
    """
    Load up exampleData.csv into a series_service' datavalues field
    """
    assert 10000 >= dvs_size > 0
    path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(path, 'example_files', 'exampleData.csv')
    df = pd.read_csv(filepath)
    df['LocalDateTime'] = pd.to_datetime(df['LocalDateTime']).astype(datetime.datetime)
    df['DateTimeUTC'] = pd.to_datetime(df['DateTimeUTC']).astype(datetime.datetime)
    dvs = []
    for record in df.to_dict('records')[:dvs_size]:
        timeseries_result_value = TimeSeriesResultValues()
        timeseries_result_value.DataValue = record["DataValue"]
        timeseries_result_value.ValueDateTimeUTCOffset = record["UTCOffset"]
        timeseries_result_value.ValueDateTime = record["DateTimeUTC"]
        timeseries_result_value.CensorCodeCV = record["CensorCode"]
        timeseries_result_value.QualityCodeCV = series.quality_control_level_code
        dvs.append(timeseries_result_value)
    series.data_values = dvs
    session.add_all(dvs)
    session.commit()
    return df


def add_series_bulk_data(session, dvs_size=50):
    site = add_site(session)
    var = add_variable(session)
    qcl = add_process_level(session)
    method = add_method(session)
    source = add_source(session)

    series = Series()
    series.site = site
    series.site_code = site.code
    series.variable = var
    series.variable_code = var.code
    series.method = method
    series.source = source
    series.quality_control_level_id = qcl.id

    df = add_bulk_data_values(session, series, dvs_size)
    sorted_df = sorted(df['LocalDateTime'])
    series.begin_date_time = sorted_df[0]
    assert isinstance(series.begin_date_time, datetime.datetime)
    series.end_date_time = sorted_df[-1]
    assert isinstance(series.end_date_time, datetime.datetime)

    sorted_df = sorted(df['DateTimeUTC'])
    series.begin_date_time_utc = sorted_df[0]
    assert isinstance(series.begin_date_time_utc, datetime.datetime)
    series.end_date_time_utc = sorted_df[-1]
    assert isinstance(series.end_date_time_utc, datetime.datetime)

    session.add(series)
    session.commit()
    return series


# Create Series objects
def add_series(session):
    result = Results()
    var = add_variable(session)
    qcl = add_process_level(session)
    result.VariableObj = var
    result.ProcessingLevelObj = qcl
    result.ProcessingLevelID = qcl.ProcessingLevelID
    session.add(result)
    session.commit()
    return result


def add_data_values(session, series):
    dvs = []
    for i in range(10):
        timeseries = TimeSeriesResultValues()
        timeseries.DataValue = i
        timeseries.TimeAggregationInterval = datetime.datetime.now() - datetime.timedelta(days=i)
        timeseries.ValueDateTimeUTCOffset = 0
        timeseries.ValueDateTime = timeseries.TimeAggregationInterval
        timeseries.CensorCodeCV = "NC"
        timeseries.QualityCodeCV = series.quality_control_level
        dvs.append(timeseries)

    series.data_values = dvs
    session.add_all(dvs)
    session.commit()
    return dvs


def add_site(session):
    spatial_ref = add_spatial_reference(session)
    site = Sites("ABC123", "Test Site")
    site.Latitude = 10.0
    site.Longitude = 10.0
    site.lat_long_datum_id = spatial_ref.SpatialReferenceID
    site.local_projection_id = spatial_ref.SpatialReferenceID
    site.Elevation_m = 1000
    # site.local_x = 10.0
    # site.local_y = 10.0
    session.add(site)
    session.commit()
    return site


def add_variable(session):
    unit = add_unit(session)
    variable = Variables()
    variable.VariableCode = "ABC123"
    variable.VariableNameCV = "Test Variable"
    variable.SpeciationCV = "Test"
    variable.VariableID = unit.id
    variable.NoDataValue = -2000.0
    session.add(variable)
    session.commit()
    return variable


def add_method(session):
    method = Methods()
    method.MethodDescription = "This is a test"
    session.add(method)
    session.commit()
    return method


def add_process_level(session):
    proc_level = ProcessingLevels()
    proc_level.ProcessingLevelCode = "ABC123"
    proc_level.Definition = "This is a test"
    proc_level.Explanation = "A test is a thing that tests code"
    session.add(proc_level)
    session.commit()
    return proc_level


def add_source(session):
    organization = Organizations()
    affiliation = Affiliations()
    organization.OrganizationName = "Test Organization"
    organization.OrganizationDescription = "This is a test"
    affiliation.PersonLink = "Test Name"
    affiliation.PrimaryPhone = "555-1234"
    affiliation.PrimaryEmail = "source@example.com"
    affiliation.PrimaryAddress = "123 Test Street"
    affiliation.OrganizationObj = organization
    session.add(affiliation)
    session.commit()
    return affiliation


def add_iso_metadata(session):
    iso = ISOMetadata()
    iso.topic_category = "Test Topic"
    iso.title = "Test Title"
    iso.abstract = "Test Abstract"
    iso.profile_version = "1.0.0.0rc4"
    session.add(iso)
    session.commit()
    return iso


def add_spatial_reference(session):
    spatial_ref = SpatialReferences()
    spatial_ref.SRSName = "This is a test"
    session.add(spatial_ref)
    session.commit()
    return spatial_ref


# Create CVs #
def add_vertical_datum_cv(session):
    vert_dat = VerticalDatumCV()
    vert_dat.term = "Test"
    vert_dat.definition = "This is a test"
    session.add(vert_dat)
    session.commit()
    return vert_dat


def add_lab_method(session):
    lab_method = LabMethod()
    lab_method.name = "Test Lab"
    lab_method.organization = "Test Org"
    lab_method.method_name = "Test Method"
    lab_method.method_description = "Test Description"
    lab_method.method_link = "Test Link"
    session.add(lab_method)
    session.commit()
    return lab_method


def add_sample(session, lab_method_id):
    sample = Sample()
    sample.type = "Test"
    sample.lab_sample_code = "ABC123"
    sample.lab_method_id = lab_method_id
    session.add(sample)
    session.commit()
    return sample


def add_site_type_cv(session):
    st_cv = SiteTypeCV()
    st_cv.term = "Test"
    st_cv.definition = "This is a test"
    session.add(st_cv)
    session.commit()
    return st_cv


def add_variable_name_cv(session):
    var_name_cv = CVVariableName()
    var_name_cv.Term = "Test"
    var_name_cv.Definition = "This is a test"
    session.add(var_name_cv)
    session.commit()
    return var_name_cv


def add_unit(session):
    unit = Units()
    unit.UnitsName = "Test"
    unit.UnitsTypeCV = "Test"
    unit.UnitsAbbreviation = "T"
    session.add(unit)
    session.commit()
    return unit


def add_offset_type_cv(session, unit_id):
    offset = OffsetType()
    offset.unit_id = unit_id
    offset.description = "This is a test"
    session.add(offset)
    session.commit()
    return offset


def add_speciation_cv(session):
    spec = CVSpeciation()
    spec.Term = "Test"
    spec.Definition = "This is a test"
    session.add(spec)
    session.commit()
    return spec


def add_sample_medium_cv(session):
    samp_med = SampleMediumCV()
    samp_med.term = "Test"
    samp_med.definition = "This is a test"
    session.add(samp_med)
    session.commit()
    return samp_med


def add_value_type_cv(session):
    value_type = ValueTypeCV()
    value_type.term = "Test"
    value_type.definition = "This is a test"
    session.add(value_type)
    session.commit()
    return value_type


def add_data_type_cv(session):
    data_type = DataTypeCV()
    data_type.term = "Test"
    data_type.definition = "This is a test"
    session.add(data_type)
    session.commit()
    return data_type


def add_general_category_cv(session):
    gen_cat = GeneralCategoryCV()
    gen_cat.term = "Test"
    gen_cat.definition = "This is a test"
    session.add(gen_cat)
    session.commit()
    return gen_cat


def add_censor_code_cv(session):
    censor = CensorCodeCV()
    censor.term = "Test"
    censor.definition = "This is a test"
    session.add(censor)
    session.commit()
    return censor


def add_sample_type_cv(session):
    sample_type = SampleTypeCV()
    sample_type.term = "Test"
    sample_type.definition = "This is a test"
    session.add(sample_type)
    session.commit()
    return sample_type


def add_version(session):
    version = ODMVersion()
    version.version_number = "1.0.0.0.1alpha"
    session.add(version)
    session.commit()
    return version
