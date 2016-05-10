# -*- coding: utf-8 -*-
from odmtools.odmdata import SessionFactory, variable, series
from odmtools.odmservices import SeriesService
from tests import test_util

from tests.test_util import build_db
import urllib
import sqlalchemy
from sqlalchemy.orm import sessionmaker

class TestFreeTDS:
    def setup(self):
        # connection string
        
        # create engine
        #quoted = urllib.quote_plus('DRIVER={FreeTDS};Server=iutahqc.uwrl.usu.edu;Database=iUTAH_Logan_OD;UID=qc;PWD=iUTAH123!!;TDS_Version=8.0;Port=1433;')
        quoted = urllib.quote_plus('DRIVER={FreeTDS};DSN=iutahqc;UID=qc;PWD=iUTAH123!!;')
        engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
        # conn = engine.connect()
        # q = conn.execute("select * from variables")
        print "engine:", engine
        assert engine 
        Session = sessionmaker(bind=engine)
        assert Session
        session = Session()
        assert session
        q= session.query(variable.Variable).all()
        print "q:", type(q), dir(q)
        for i in q:
            print i
        #conn.close()
        q= session.query(series.Series).all()
        for i in q[:10]:
            print i
        assert q
        print engine

    def test_connection(self):
        pass
