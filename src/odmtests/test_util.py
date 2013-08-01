from odmdata import *

def build_db(engine):
	Base.metadata.create_all(engine)