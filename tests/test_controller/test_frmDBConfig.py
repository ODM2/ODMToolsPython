from odmtools.controller import frmDBConfig
from odmtools.odmservices.service_manager import ServiceManager

__author__ = 'Jacob'

class TestFrmDBConfig:
    def setup(self):

        self.service_manager = ServiceManager()
        conn_dict = {'engine': 'mysql',
                     'password': 'passwd',
                     'db': 'odm',
                     'user': 'root',
                     'address': '127.0.0.1'}
        self.service_manager.add_connection(conn_dict)
        self.frame = frmDBConfig.frmDBConfig(None, self.service_manager)
        assert self.frame

    '''
    def test_form(self):
        """test form"""
        assert self.bulkInsertCtrl.panel.choices == {
            "Microsoft SQL Server": 'mssql', "MySQL": 'mysql', "PostgreSQL":"postgresql"
        }
    '''


