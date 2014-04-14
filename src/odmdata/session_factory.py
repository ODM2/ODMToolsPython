from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SessionFactory():
    def __init__(self, connection_string, echo):
        self.engine = create_engine(connection_string, encoding='utf-8', echo=echo,
                                    #pool_size=20,
                                    pool_recycle=3600,
                                    pool_timeout=5,
                                    max_overflow=0)

        # Create session maker
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def __repr__(self):
        return "<SessionFactory('%s')>" % (self.engine)
