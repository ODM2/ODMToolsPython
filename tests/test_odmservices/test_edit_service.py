from odmtools.odmdata import *
from odmtools.odmservices import SeriesService, EditService

from tests import test_util


class TestSeriesService:
    def setup(self):

        self.connection_string = "sqlite:///:memory:"
        self.series_service = SeriesService(connection_string=self.connection_string, debug=False)

        engine = self.series_service._session_factory.engine
        test_util.build_db(engine)

        self.memory_database = MemoryDatabase()
        self.memory_database.set_series_service(self.series_service)
        self.session = self.memory_database.series_service._session_factory.get_session()

        self.series = test_util.add_series_bulk_data(self.session)
        #assert len(self.series.data_values) == 100

        self.edit_service =EditService(1, connection= self.memory_database)


        """
        @pytest.fixture(scope="class", autouse=True)
    def build_db(self):
        """
        #Builds an empty sqlite (in-memory) database for testing
        #:return: None
        """
        # path to the ddl script for building the database
        ddlpath= abspath(join(dirname(__file__), 'data/empty.sql'))

        # create and empty sqlite database for testing
        db = dbconnection.createConnection('sqlite', ':memory:')

        # read the ddl script and remove the first (BEGIN TRANSACTION) and last (COMMIT) lines
        ddl = open(ddlpath, 'r').read()
        ddl = ddl.replace('BEGIN TRANSACTION;','')
        ddl = ddl.replace('COMMIT;','')

        # execute each statement to build the odm2 database
        for line in ddl.split(');')[:-1]:
            try:
                db.engine.execute(line + ');')
            except Exception as e:
                print e

        self.write = CreateODM2(db)
        self.engine= db.engine

        globals['write'] = self.write
        globals['engine'] = self.engine
        globals['db'] = db
        # return self.write, self.engine

    def setup(self):

        self.writer = globals['write']
        self.engine = globals['engine']
        self.db = globals['db']
        """



    def test_save_series(self):
        stlen = len(self.series.data_values)
        assert self.edit_service.save()
        val = self.series_service.get_series_by_id(self.series.id)
        assert len(val.data_values)==stlen

    def test_save_as_series(self):
        var = test_util.add_variable(self.session)
        print var
        stlen = len(self.series.data_values)
        assert self.edit_service.save_as(var= var)
        assert self.edit_service.memDB.series_service.series_exists_quint(self.series.site_id, var.id, self.series.method_id, self.series.source_id, self.series.quality_control_level_id)

    def test_save_as_existing_series(self):
        var = test_util.add_variable(self.session)
        assert self.edit_service.save_existing(var = var)

    def test_save_append_keep(self):
        #TODO add custon test

        len1= len(self.series.data_values)
        # keep data from original series if overlap:


        svalue = self.series.data_values[0]

        self.edit_service.memDB.updateValue([svalue.local_date_time],'+', 5 )
        news= self.edit_service.memDB.series_service.get_series_by_id(self.series.id)
        result = self.edit_service.save_appending(overwrite = False)
        len2= len(self.series.data_values)
        assert len1 == len2
        assert news.data_values[0].data_value == svalue.data_value
        assert result

    def test_save_append_overwrite(self):
        len1= len(self.series.data_values)
        svalue = self.series.data_values[0]

        self.edit_service.memDB.updateValue([svalue.local_date_time],'+', 5 )
        news= self.edit_service.memDB.series_service.get_series_by_id(self.series.id)
        result = self.edit_service.save_appending(overwrite = True)
        len2= len(self.series.data_values)
        assert len1 == len2
        assert news.data_values[0].data_value == svalue.data_value + 5
        assert result





