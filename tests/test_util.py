import datetime
import pandas as pd
from odmtools.odmdata import *
import os
import sys


def build_db(engine):
    Base.metadata.create_all(engine)


# Create DB objects #

def add_bulk_data_values(session, series, dvs_size):
    """
    Load up exampleData.csv into a series' datavalues field
    """
    assert 10000 >= dvs_size > 0
    filepath = os.path.join('.', 'example_files', 'exampleData.csv')
    df = pd.read_csv(filepath)
    df['LocalDateTime'] = pd.to_datetime(df['LocalDateTime']).astype(datetime.datetime)
    df['DateTimeUTC'] = pd.to_datetime(df['DateTimeUTC']).astype(datetime.datetime)
    dvs = []
    for record in df.to_dict('records')[:dvs_size]:
        dv = DataValue()
        dv.data_value = record['DataValue']
        dv.local_date_time = record['LocalDateTime']
        dv.utc_offset = record['UTCOffset']
        dv.date_time_utc = record['DateTimeUTC']
        dv.site_id = series.site_id
        dv.variable_id = series.variable_id
        dv.censor_code = record['CensorCode']
        dv.method_id = series.method_id
        dv.source_id = series.source_id
        dv.quality_control_level_id = series.quality_control_level_id
        dvs.append(dv)
    series.data_values = dvs
    session.add_all(dvs)
    session.commit()
    return df

def add_series_bulk_data(session, dvs_size=50):
    site = add_site(session)
    var = add_variable(session)
    qcl = add_qcl(session)
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
    site = add_site(session)
    var = add_variable(session)
    qcl = add_qcl(session)
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

    dvs = add_data_values(session, series)
    series.begin_date_time = dvs[0].local_date_time
    series.end_date_time = dvs[-1].local_date_time
    series.begin_date_time_utc = dvs[0].date_time_utc
    series.end_date_time_utc = dvs[-1].date_time_utc

    session.add(series)
    session.commit()
    return series


def add_data_values(session, series):
    dvs = []
    for i in range(10):
        dv = DataValue()
        dv.data_value = i
        dv.local_date_time = datetime.datetime.now() - datetime.timedelta(days=i)
        dv.utc_offset = 0
        dv.date_time_utc = dv.local_date_time
        dv.site_id = series.site_id
        dv.variable_id = series.variable_id
        dv.censor_code = "NC"
        dv.method_id = series.method_id
        dv.source_id = series.source_id
        dv.quality_control_level_id = series.quality_control_level_id
        dvs.append(dv)

    series.data_values = dvs
    session.add_all(dvs)
    session.commit()
    return dvs


def add_site(session):
    spatial_ref = add_spatial_reference(session)
    site = Site("ABC123", "Test Site")
    site.latitude = 10.0
    site.longitude = 10.0
    site.lat_long_datum_id = spatial_ref.id
    site.local_projection_id = spatial_ref.id
    site.elevation_m = 1000
    site.local_x = 10.0
    site.local_y = 10.0
    session.add(site)
    session.commit()
    return site


def add_variable(session):
    unit = add_unit(session)
    variable = Variable()
    variable.code = "ABC123"
    variable.name = "Test Variable"
    variable.speciation = "Test"
    variable.variable_unit_id = unit.id
    variable.sample_medium = "Test Medium"
    variable.value_type = "Test Val Type"
    variable.is_regular = True
    variable.time_support = 3.14
    variable.time_unit_id = unit.id
    variable.data_type = "Test Data Type"
    variable.general_category = "Test Category"
    variable.no_data_value = -2000.0
    session.add(variable)
    session.commit()
    return variable


def add_method(session):
    method = Method()
    method.description = "This is a test"
    session.add(method)
    session.commit()
    return method


def add_qcl(session):
    qcl = QualityControlLevel()
    qcl.code = "ABC123"
    qcl.definition = "This is a test"
    qcl.explanation = "A test is a thing that tests code"
    session.add(qcl)
    session.commit()
    return qcl


def add_source(session):
    source = Source()
    source.organization = "Test Organization"
    source.description = "This is a test"
    source.contact_name = "Test Name"
    source.phone = "555-1234"
    source.email = "source@example.com"
    source.address = "123 Test Street"
    source.city = "Metropolis"
    source.state = "NY"
    source.zip_code = "12345"
    source.citation = "Test Citation"

    iso = add_iso_metadata(session)
    source.iso_metadata_id = iso.id
    session.add(source)
    session.commit()
    return source


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
    spatial_ref = SpatialReference()
    spatial_ref.srs_name = "This is a test"
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
    var_name_cv = VariableNameCV()
    var_name_cv.term = "Test"
    var_name_cv.definition = "This is a test"
    session.add(var_name_cv)
    session.commit()
    return var_name_cv


def add_unit(session):
    unit = Unit()
    unit.name = "Test"
    unit.type = "Test"
    unit.abbreviation = "T"
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
    spec = SpeciationCV()
    spec.term = "Test"
    spec.definition = "This is a test"
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
