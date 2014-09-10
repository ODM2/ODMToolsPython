from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SessionFactory():
    def __init__(self, connection_string, echo):
        self.engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                    pool_timeout=5, pool_size=20, max_overflow=0)
        self.psql_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                              pool_timeout=5, max_overflow=0, connect_args={'connect_timeout': 1})
        self.ms_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                            pool_timeout=5, max_overflow=0, connect_args={'timeout': 1})
        self.my_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600,
                                            pool_timeout=5, max_overflow=0, connect_args={'connect_timeout': 1})


        # Create session maker
        self.Session = sessionmaker(bind=self.engine)
        self.psql_test_Session = sessionmaker(bind=self.psql_test_engine)
        self.ms_test_Session = sessionmaker(bind=self.ms_test_engine)
        self.my_test_Session = sessionmaker(bind=self.my_test_engine)

    def get_session(self):
        return self.Session()

    def __repr__(self):
        return "<SessionFactory('%s')>" % (self.engine)

'''
class SessionFactory():
    def __init__(self, connection_string, echo):
        self.engine = create_engine(connection_string, encoding='utf-8', echo=echo,
                                    #pool_size=20,
                                    pool_recycle=3600)

        # Create session maker
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def __repr__(self):
        return "<SessionFactory('%s')>" % (self.engine)
'''