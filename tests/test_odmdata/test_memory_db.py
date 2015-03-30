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

    def test_get_data_values(self):
        dvs = self.memory_db.getDataValuesDF()
        assert len(dvs) == 10

    def test_update_points(self):
        self.memory_db.update([{"value":15,"id":1}])
        dvs = self.memory_db.getDataValuesDF()
        print dvs["DataValue"]
        assert dvs["DataValue"][1-1] == 15

    def test_update_value(self):
        self.memory_db.updateValue([1],'+', 5 )
        dvs = self.memory_db.getDataValuesDF()
        assert dvs["DataValue"][1-1] == 5

    def test_add_points(self):
        #with pytest.raises(NotImplementedError):
        point = [('-9999', None, datetime.datetime(2011, 3, 25, 0, 0), '-7', datetime.datetime(2015, 3, 25, 7, 0), None,
                  None, u'nc', None, None, self.series.site_id, self.series.variable_id, self.series.method_id,
                  self.series.source_id, self.series.quality_control_level_id)]
        self.memory_db.addPoints(point)
        dvs = self.memory_db.getDataValuesDF()

        assert len(dvs) == 11
        assert dvs["DataValue"][-1] == -9999

    def test_update_flag(self):
        self.memory_db.updateFlag([5], '50')
        dvs=self.memory_db.getDataValuesDF()
        assert dvs["QualifierID"][5-1]=='50'

    def test_save(self):
        pass

    def test_delete_points(self):
        stlen= len(self.memory_db.getDataValuesDF())
        self.memory_db.delete([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        dvs = self.memory_db.getDataValuesDF()
        assert len(dvs) == stlen-10