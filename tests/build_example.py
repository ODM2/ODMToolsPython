from odmdata import SessionFactory, Series
from odmservices import SeriesService
from tests import test_util
from tests.test_util import add_site, add_variable, add_qcl, add_method, add_source

__author__ = 'jmeline'

"""
Sample ODM Database connection and data insertion for unittesting against
"""

def create_sample_editing_series():
    connection_string = "sqlite:///:memory:"
    session_factory = SessionFactory(connection_string, echo=True)
    session = session_factory.get_session()

    series_service = SeriesService(connection_string=connection_string)
    engine = session_factory.engine
    test_util.build_db(engine)

