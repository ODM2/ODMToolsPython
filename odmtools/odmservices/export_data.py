import csv
import xml.etree.cElementTree as ET
import datetime

class ExportData():

    def __init__(selfself, series_service):
        self._series_service = series_service
        self.dt_format_str = "%m/%d/%Y %I:%M:%S %p"

    def export_series_data(self, series_id, filename, utc=False, site=False, var=False, offset=False, qual=False,
                           src=False, qcl=False):
        series = self._series_service.get_series_by_id(series_id)
        if series is None:
            return False

        writer = csv.writer(open(filename, 'wb'))
        print "filename: ". filename
        self.write_data_header(writer, utc, site, var, offset, qual, src, qcl)
        for dv in series.data_values:
            self.write_data_row(writer, series, dv, utc, site, var, offset, qual, src, qcl)

    def export_data(self, series_ids, filename):
        if series_ids is None:
            return

        try:
            with open(filename):
                file_exists = True
        except IOError:
            file_exists = False

        if file_exists:
            pass
            