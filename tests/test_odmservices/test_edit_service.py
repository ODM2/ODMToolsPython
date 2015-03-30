from odmtools.odmdata import *
from odmtools.odmservices import SeriesService

from tests import test_util


class TestSeriesService:
    def setup(self):
        self.connection_string = "sqlite:///:memory:"
        self.series_service = SeriesService(self.connection_string, debug=False)
        self.session = self.series_service._session_factory.get_session()
        engine = self.series_service._session_factory.engine
        test_util.build_db(engine)



    ## TODO Unittest save_series, save_as, save_as_existing
    '''
    def test_save_series(self):
        series = Series()
        site = test_util.add_site(self.session)
        variable = test_util.add_variable(self.session)
        method = test_util.add_method(self.session)
        source = test_util.add_source(self.session)
        qcl = test_util.add_qcl(self.session)

        series.site_id = site.id
        series.variable_id = variable.id
        series.method_id = method.id
        series.source_id = source.id
        series.quality_control_level_id = qcl.id

        dvs = []
        for val in range(10):
            dv = DataValue()
            dv.data_value = val
            dv.site_id = site.id
            dv.variable_id = variable.id
            dv.method_id = method.id
            dv.source_id = source.id
            dv.quality_control_level_id = qcl.id
            dvs.append(dv)

        print series.variable_code
        assert self.series_service.save_series(series)
        assert self.series_service.series_exists(site.id, variable.id, method.id, source.id, qcl.id)
        assert not self.series_service.save_series(series)
    '''

