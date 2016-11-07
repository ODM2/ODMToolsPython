import logging
import os
import sys

import urllib


from sqlalchemy.exc import SQLAlchemyError
from series_service import  SeriesService
from edit_service import EditService
from export_service import ExportService


from odmtools.controller import EditTools
from odmtools.lib.Appdirs.appdirs import user_config_dir

from odmtools.odmdata import dbconnection #ODM



# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')


class ServiceManager():
    def __init__(self, debug=False, conn_dict=None):
        self.debug = debug
        f = self._get_file('r')
        self._conn_dicts = []
        #self.version = 0
        self._connection_format = "%s+%s://%s:%s@%s/%s"

        # Read all lines (connections) in the connection.cfg file

        if conn_dict is None:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    line = line.split()
                    #logger.debug(line)

                    if len(line) >= 5:
                        line_dict = {}

                        line_dict['engine'] = line[0]
                        line_dict['user'] = line[1]
                        line_dict['password'] = line[2]
                        line_dict['address'] = line[3]
                        line_dict['db'] = line[4]
                        line_dict['version']= float(line[5]) if len(line)>5 else 1.1
                        self._conn_dicts.append(line_dict)
        else:
            self._conn_dicts.append(conn_dict)



        if len(self._conn_dicts) is not 0:
            # The current connection defaults to the most recent (i.e. the last written to the file)
            self._current_conn_dict = self._conn_dicts[-1]
        else:
            self._current_conn_dict = None

        f.close()

    def get_all_conn_dicts(self):
        return self._conn_dicts

    def get_current_conn_dict(self):
        return self._current_conn_dict

    def set_current_conn_dict(self, dict):
        self._current_conn_dict = dict

    def add_connection(self, conn_dict):
        """conn_dict must be a dictionary with keys: engine, user, password, address, db"""

        # remove earlier connections that are identical to this one
        self.delete_connection(conn_dict)


        #assume connection has already been tested
        # if self.test_connection(conn_dict):
        # write changes to connection file
        self._conn_dicts.append(conn_dict)
        self._current_conn_dict = self._conn_dicts[-1]
        self._save_connections()

        return True
        # else:
        #     logger.error("Unable to save connection due to invalid connection to database")
        #     return False

    def test_connection(self, conn_dict):

        try:
            if dbconnection.isValidConnection(
                    dbconnection.buildConnectionString(conn_dict['engine'], conn_dict['address'], conn_dict['db'],
                                                       conn_dict['user'],
                                                       conn_dict['password']), dbtype=conn_dict['version']):
                return self.get_current_conn_dict()
        # except Exception as e:
        #     logger.fatal(
        #         "The previous database for some reason isn't accessible, please enter a new connection %s" % e.message)
        #     return None
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy Error: %s" % e.message)
            raise e
        except Exception as e:
            logger.error("The database is not accessible please enter a new connection. Error: %s" % e.message)
            raise e


    def is_valid_connection(self):
        # conn_string = self._build_connection_string(self._current_conn_dict)
        # logger.debug("Conn_string: %s" % conn_string)

        if self.get_current_conn_dict():
            conn_dict = self.get_current_conn_dict()
            return self.test_connection(conn_dict)

        return None


    def delete_connection(self, conn_dict):
        self._conn_dicts[:] = [x for x in self._conn_dicts if x != conn_dict]

    def get_series_service(self, conn_dict=None, conn_string=""):
        if not conn_dict:
            conn_dict = self.get_current_conn_dict()

        if conn_string:
            #todo how to get version from a connection string
            conn = dbconnection.createConnectionFromString(conn_string, 2.0)#float(self.get_current_conn_dict()["version"]))
        else:
            conn = dbconnection.createConnection(conn_dict['engine'], conn_dict['address'], conn_dict['db'], conn_dict['user'],
                                      conn_dict['password'], conn_dict['version'])


        # version = 1.1
        # if conn_dict:
        #     conn_string = self._build_connection_string(conn_dict)
        #     #self._current_conn_dict = conn_dict
        #
        #     version = float(conn_dict['version'])
        # elif not conn_dict and not conn_string:
        #     conn_string = self._build_connection_string(self._current_conn_dict)
        #     version = float(self._current_conn_dict['version'])
        #
        # sf = SessionFactory(conn_string, self.debug, version = version)
        ss= SeriesService(conn)
        return ss

    def get_edit_service(self, series_id, connection):
        return EditService(series_id, connection=connection,  debug=self.debug)

    # todo: Not using build_connection_string. Need to update this
    def get_record_service(self, script, series_id, connection):
        return EditTools(self, script, self.get_edit_service(series_id, connection),
                             connection)

    def get_export_service(self):
        return ExportService(self.get_series_service())

    ## ###################
    # private variables
    ## ###################

    def _get_file(self, mode):
        #fn = util.resource_path('connection.config')
        fn = os.path.join(user_config_dir("ODMTools", "UCHIC"), 'connection.config')

        config_file = None
        try:

            if os.path.exists(fn):
                config_file = open(fn, mode)
            else:
                os.makedirs(user_config_dir("ODMTools", "UCHIC"))
                open(fn, 'w').close()
                config_file = open(fn, mode)
        except:
            open(fn, 'w').close()
            config_file = open(fn, mode)


        return config_file


    def _save_connections(self):
        f = self._get_file('w')
        for conn in self._conn_dicts:
            f.write("%s %s %s %s %s %s\n" % (conn['engine'], conn['user'], conn['password'], conn['address'], conn['db'], conn['version']))
        f.close()

