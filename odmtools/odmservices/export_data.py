import csv
import xml.etree.cElementTree as ET
import datetime

class ExportData():

    def __init__(self, series_service):
        self._series_service = series_service
        self.dt_format_str = "%m/%d/%Y %I:%M:%S %p"

    def export_series_data(self, series_id, filename, utc=False, site=False, var=False, offset=False, qual=False,
                           src=False, qcl=False):
        #series = self._series_service.get_series_by_id(series_id)
        series = self._series_service.get_series(series_id)

        if series is None:
            return False

        writer = csv.writer(open(filename, 'wb'))
        plainWriter = open(filename, 'w')
        print "filename: "
        print filename
        self.write_data_header(plainWriter, series, utc, site, var, offset, qual, src, qcl)
        # for dv in series.data_values:
        #    self.write_data_row(writer, series, dv, utc, site, var, offset, qual, src, qcl)

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

    def write_data_header(self, plainWriter, series, utc, site, var, offset, qual, src, qcl):
        self.write_warning_header(plainWriter)
        self.write_site_information(plainWriter, series, site)
        self.write_variable_and_method_information(plainWriter, series)


    def write_site_information(self, plainWriter, series, site):
        plainWriter.write('# Site Information\n')
        plainWriter.write('# ----------------------------------\n')
        plainWriter.write('# Network: TBD\n')
        plainWriter.write('# SiteCode: '+str(series.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode)+'\n')
        plainWriter.write('# SiteName: ' + str(series.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName) + '\n')
        plainWriter.write('# Latitude: ' + str(series.FeatureActionObj.SamplingFeatureObj.Latitude) + '\n')
        plainWriter.write('# Longitude: ' + str(series.FeatureActionObj.SamplingFeatureObj.Longitude) + '\n')
        plainWriter.write('# LatLonDatum: ' + 'TBD' + '\n') #FIX
        plainWriter.write('# Elevation_m: ' + str(series.FeatureActionObj.SamplingFeatureObj.Elevation_m) + '\n')
        plainWriter.write('# ElevationDatum: ' + str(series.FeatureActionObj.SamplingFeatureObj.ElevationDatumCV) + '\n')
        plainWriter.write('# State: ' + 'TBD' + '\n')  # FIX
        plainWriter.write('# County: ' + 'TBD' + '\n')  # FIX
        plainWriter.write('# Comments: ' + 'TBD' + '\n')  # FIX
        plainWriter.write(
            '# SiteType: ' + str(series.FeatureActionObj.SamplingFeatureObj.SiteTypeCV) + '\n')
        plainWriter.write('#\n')

    def write_variable_and_method_information(self, plainWriter, series):
        plainWriter.write('# Variable and Method Information\n')
        plainWriter.write('# ----------------------------------\n')
        plainWriter.write('# VariableCode: ' + str(series.VariableObj.VariableCode) + '\n')
        plainWriter.write('# VariableName: ' + str(series.VariableObj.VariableName) + '\n')

    def write_warning_header(self, plainWriter):
        plainWriter.write(
            '# ------------------------------------------------------------------------------------------\n')
        plainWriter.write('# WARNING: The data are released on the condition that neither iUTAH nor any of its \n')
        plainWriter.write('# participants may be held liable for any damages resulting from their use. The following \n')
        plainWriter.write('# metadata describe the data in this file:\n')
        plainWriter.write(
            '# ------------------------------------------------------------------------------------------\n')
        plainWriter.write('#\n')
        plainWriter.write('# Quality Control Level Information\n')
        plainWriter.write('# -----------------------------------------------\n')
        plainWriter.write('# These data have passed QA/QC procedures such as sensor calibration and\n')
        plainWriter.write('# visual inspection and removal of obvious errors. These data are approved\n')
        plainWriter.write('# by Technicians as the best available version of the data. See published\n')
        plainWriter.write('# script for correction steps specific to this data series.\n')
        plainWriter.write('#\n')