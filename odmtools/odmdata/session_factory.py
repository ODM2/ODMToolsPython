from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


class SessionFactory():
    def __init__(self, connection_string, echo):
        self.engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                    pool_size=20)
        self.psql_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                              connect_args={'connect_timeout': 1})
        self.ms_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                            connect_args={'timeout': 1})
        self.my_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                            connect_args={'connect_timeout': 1})

        # Create session maker
        self.Session = sessionmaker(bind=self.engine)
        self.psql_test_Session = sessionmaker(bind=self.psql_test_engine)
        self.ms_test_Session = sessionmaker(bind=self.ms_test_engine)
        self.my_test_Session = sessionmaker(bind=self.my_test_engine)


        # @event.listens_for(self.engine, "connect")
        # def do_connect(dbapi_connection, connection_record):
        #     # disable pysqlite's emitting of the BEGIN statement entirely.
        #     # also stops it from emitting COMMIT before any DDL.
        #     dbapi_connection.isolation_level = None
        #
        # @event.listens_for(self.engine, "begin")
        # def do_begin(conn):
        #     # emit our own BEGIN
        #     conn.execute("BEGIN")


    def get_session(self):
        return self.Session()

    def __repr__(self):
        return "<SessionFactory('%s')>" % (self.engine)

