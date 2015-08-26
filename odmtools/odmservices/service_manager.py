import logging
import os
import sys

import urllib

from sqlalchemy.exc import SQLAlchemyError
from odmtools.odmservices import SeriesService, CVService, EditService, ExportService
from odmtools.controller import EditTools
from odmtools.lib.Appdirs.appdirs import user_config_dir
from odmtools.odmdata import SessionFactory, Variable

from odmtools.common.logger import LoggerTool
tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


class ServiceManager():
    def __init__(self, debug=False):
        self.debug = debug
        f = self._get_file('r')
        self._conn_dicts = []
        self.version = 0
        self._connection_format = "%s+%s://%s:%s@%s/%s"

        # Read all lines (connections) in the connection.cfg file
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
                    self._conn_dicts.append(line_dict)

        if len(self._conn_dicts) is not 0:
            # The current connection defaults to the most recent (i.e. the last written to the file)
            self._current_conn_dict = self._conn_dicts[-1]
        else:
            self._current_conn_dict = None

        f.close()

    def get_all_conn_dicts(self):
        return self._conn_dicts

    def is_valid_connection(self):
        if self._current_conn_dict:
            conn_string = self._build_connection_string(self._current_conn_dict)
            logger.debug("Conn_string: %s" % conn_string)
            try:
                if self.testEngine(conn_string):
                    return self.get_current_conn_dict()
            except Exception as e:
                logger.fatal("The previous database for some reason isn't accessible, please enter a new connection %s" % e.message)
                return None
        return None

    def get_current_conn_dict(self):
        return self._current_conn_dict

    def set_current_conn_dict(self, dict):
        self._current_conn_dict = dict

    def add_connection(self, conn_dict):
        """conn_dict must be a dictionary with keys: engine, user, password, address, db"""

        # remove earlier connections that are identical to this one
        self.delete_connection(conn_dict)

        if self.test_connection(conn_dict):
            # write changes to connection file
            self._conn_dicts.append(conn_dict)
            self._current_conn_dict = self._conn_dicts[-1]
            self._save_connections()
            return True
        else:
            logger.error("Unable to save connection due to invalid connection to database")
            return False


    @classmethod
    def testEngine(self, connection_string):
        s = SessionFactory(connection_string, echo=False)

        s.test_Session().query(Variable.code).limit(1).first()

        return True

    def test_connection(self, conn_dict):
        try:
            conn_string = self._build_connection_string(conn_dict)
            if self.testEngine(conn_string) and self.get_db_version(conn_string) == '1.1.1':
                return True
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy Error: %s" % e.message)
            raise e
        except Exception as e:
            logger.error("Error: %s" % e)
            raise e
        return False

    def delete_connection(self, conn_dict):
        self._conn_dicts[:] = [x for x in self._conn_dicts if x != conn_dict]

    # Create and return services based on the currently active connection
    def get_db_version_dict(self, conn_dict):
        conn_string = self._build_connection_string(conn_dict)
        self.get_db_version(conn_string)

    def get_db_version(self, conn_string):
        if isinstance(conn_string, dict):
            conn_string = self._build_connection_string(conn_string)
        service = SeriesService(conn_string)
        #if not self.version:
        try:
            self.version = service.get_db_version()
        except Exception as e:
            logger.error("Exception: %s" % e.message)
            return None
        return self.version

    def get_series_service(self, conn_dict="", conn_string = ""):

        if conn_dict:
            conn_string = self._build_connection_string(conn_dict)
            self._current_conn_dict = conn_dict
        elif not conn_string:
            conn_string = self._build_connection_string(self._current_conn_dict)
        return SeriesService(SessionFactory(conn_string, self.debug))

    def get_cv_service(self):
        conn_string = self._build_connection_string(self._current_conn_dict)
        return CVService(SessionFactory(conn_string, self.debug))

    def get_edit_service(self, series_id, connection):
        
        return EditService(series_id, connection,  debug=self.debug)

    def get_record_service(self, script, series_id, connection):
        return EditTools(self, script, self.get_edit_service(series_id, connection),
                             self._build_connection_string(self.is_valid_connection()))

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

    def _build_connection_string(self, conn_dict):
        driver = ""
        if conn_dict['engine'] == 'mssql' and sys.platform != 'win32':
            driver = "pyodbc"
            quoted = urllib.quote_plus('DRIVER={FreeTDS};DSN=%s;UID=%s;PWD=%s;' % (conn_dict['address'], conn_dict['user'], conn_dict['password']))
            conn_string = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
        
        else:
            if conn_dict['engine'] == 'mssql':
                driver = "pyodbc"
            elif conn_dict['engine'] == 'mysql':
                driver = "pymysql"
            elif conn_dict['engine'] == 'postgresql':
                driver = "psycopg2"
            else:
                driver = "None"

            conn_string = self._connection_format % (
                conn_dict['engine'], driver, conn_dict['user'], conn_dict['password'], conn_dict['address'],
                conn_dict['db'])
        return conn_string

    def _save_connections(self):
        f = self._get_file('w')
        for conn in self._conn_dicts:
            f.write("%s %s %s %s %s\n" % (conn['engine'], conn['user'], conn['password'], conn['address'], conn['db']))
        f.close()

