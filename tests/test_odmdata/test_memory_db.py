import pytest

from odmtools.odmdata import MemoryDatabase
from odmtools.odmservices import SeriesService
from tests import test_util
import datetime


class TestMemoryDB:
    def setup(self):
        self.connection_string = "sqlite:///:memory:"
        self.series_service = SeriesService(connection_string=self.connection_string, debug=False)
        self.session = self.series_service._session_factory.get_session()
        engine = self.series_service._session_factory.engine
        test_util.build_db(engine)

        self.memory_db = MemoryDatabase()

        self.memory_db.set_series_service(self.series_service)
        self.series = test_util.add_series(self.session)
        self.memory_db.initEditValues(self.series.id)
        sorted_df = sorted(self.memory_db.df['LocalDateTime'])
        self.sdate = sorted_df[0]

    def test_get_data_values(self):
        dvs = self.memory_db.getDataValuesDF()
        assert len(dvs) == 10

    def test_build_series(self):
        dvs = 100
        self.series = test_util.add_series_bulk_data(self.session, dvs_size=dvs)
        assert self.series
        assert len(self.series.data_values) == dvs

    def test_rollback_single(self):

        self.memory_db.update([{"value":15,"id":self.sdate}])
        dvs = self.memory_db.getDataValuesDF()
        print dvs["DataValue"]
        assert dvs["DataValue"][0] == 15

        self.memory_db.mem_service._edit_session.begin_nested()

        self.memory_db.update([{"value":50,"id":self.sdate}])
        dvs = self.memory_db.getDataValuesDF()

        assert dvs["DataValue"][0] == 50


        self.memory_db.mem_service._edit_session.rollback()
        #make sure not everythin was rolled back
        dvs = self.memory_db.getDataValuesDF()

        assert dvs["DataValue"][0] == 15

    def test_rollback(self):
        dvs = self.memory_db.getDataValuesDF()
        startval = dvs["DataValue"][0]

        #make a change
        self.memory_db.update([{"value":15,"id":self.sdate}])
        dvs = self.memory_db.getDataValuesDF()
        #test if it was successful
        assert dvs["DataValue"][0] == 15
        #undo the change
        self.memory_db.rollback()
        dvs = self.memory_db.getDataValuesDF()

        assert dvs["DataValue"][0] == startval




    def test_update_points(self):

        self.memory_db.update([{"value":15,"id":self.sdate}])
        dvs = self.memory_db.getDataValuesDF()
        print dvs["DataValue"]
        assert dvs["DataValue"][0] == 15

    def test_update_value(self):
        self.memory_db.updateValue([self.sdate],'+', 5 )
        dvs = self.memory_db.getDataValuesDF()
        assert dvs["DataValue"][0] == 14

    def test_add_points(self):
        #with pytest.raises(NotImplementedError):
        assert len(self.memory_db.getDataValuesDF().index)==10
        point = [('-9999', None, datetime.datetime(2011, 3, 25, 0, 0), '-7', datetime.datetime(2015, 3, 25, 7, 0), None,
                  None, u'nc', None, None, self.series.site_id, self.series.variable_id, self.series.method_id,
                  self.series.source_id, self.series.quality_control_level_id)]
        self.memory_db.addPoints(point)
        dvs = self.memory_db.getDataValuesDF()

        assert len(dvs.index) == 11
        assert dvs["DataValue"][0] == -9999

    def test_update_flag(self):
        self.memory_db.updateFlag([self.sdate], '50')
        dvs=self.memory_db.getDataValuesDF()
        assert dvs["QualifierID"][0] == '50'


    def test_delete_points(self):
        stlen= len(self.memory_db.df.index)

        self.memory_db.delete(self.memory_db.df["LocalDateTime"].tolist()[0:10])
        dvs = self.memory_db.getDataValuesDF()
        assert len(dvs.index) == stlen-10

