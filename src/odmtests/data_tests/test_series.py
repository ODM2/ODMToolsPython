from odmdata import *
# from odmservices import 
from odmdata import copy_series

class TestSeries:
	def setup(self):
		self.connection_string = "sqlite:///:memory:"
		