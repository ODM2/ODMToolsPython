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

        print "filename: "
        print filename
        plainWriter = open(filename, 'w')
        self.write_text_header(plainWriter, series, utc, site, var, offset, qual, src, qcl)
        plainWriter.close()
        writer = csv.writer(open(filename, 'a'))
        self.write_data_header(writer, utc, site, var, offset, qual, src, qcl)
        # for dv in self._series_service.get_values(series.ResultID):
        #     self.write_data_row(writer, series, dv, utc, site, var, offset, qual, src, qcl)
        vals = self._series_service.get_values(series.ResultID)
        vals.to_csv(filename, ',',
                    columns = ['valuedatetime', 'valuedatetimeutcoffset', 'datavalue', 'censorcodecv', 'qualifiercodecv'],
                    header = ['LocalDateTime', 'UTCOffset', series.VariableObj.VariableCode, 'CensorCode', 'QualifierCode'],
                    mode = 'a',
                    index = False)

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

    def write_data_header(self, writer, utc, site, var, offset, qual, src, qcl):
        # Build header list
        header = []
        header.append("SeriesId")
        header.append("ValueId")
        header.append("DataValue")
        header.append("ValueAccuracy")
        header.append("LocalDateTime")
        if utc:
            header.append("UTCOffset")
            header.append("DateTimeUTC")
        header.append("SiteCode")
        if site:
            header.append("SiteName")
            header.append("SiteType")
            header.append("Latitude")
            header.append("Longitude")
            header.append("SRSName")
        header.append("VariableCode")
        if var:
            header.append("VariableName")
            header.append("Speciation")
            header.append("VariableUnitsName")
            header.append("VariableUnitsAbbreviation")
            header.append("SampleMedium")
        header.append("OffsetValue")
        header.append("OffsetTypeID")
        if offset:
            header.append("OffsetDescription")
            header.append("OffsetUnitsName")
        header.append("CensorCode")
        header.append("QualifierID")
        if qual:
            header.append("QualifierCode")
            header.append("QualifierDescription")
        if src:
            header.append("Organization")
            header.append("SourceDescription")
            header.append("Citation")
        if qcl:
            header.append("QualityControlLevelCode")
            header.append("Definition")
            header.append("Explanation")
        header.append("SampleID")

        writer.writerow(header)

    def write_data_row(self, writer, series, dv, utc, site, var, offset, qual, src, qcl):
        data = []
        data.append(series.id)
        data.append(dv.id)
        data.append(dv.data_value)
        data.append(dv.value_accuracy)
        data.append(dv.local_date_time)
        if utc:
            data.append(dv.utc_offset)
            data.append(dv.date_time_utc)
        data.append(series.site_code)
        if site:
            data.append(series.site_name)
            data.append(series.site.type)
            data.append(series.site.latitude)
            data.append(series.site.longitude)
            data.append(series.site.spatial_ref.srs_name)
        data.append(series.variable_code)
        if var:
            data.append(series.variable_name)
            data.append(series.speciation)
            data.append(series.variable_units_name)
            data.append(series.variable.variable_unit.abbreviation)
            data.append(series.sample_medium)
        data.append(dv.offset_value)
        data.append(dv.offset_type_id)
        if offset:
            if dv.offset_type is not None:
                data.append(dv.offset_type.description)
                data.append(dv.offset_type.unit.name)
            else:
                data.append('')
                data.append('')
        data.append(dv.censor_code)
        data.append(dv.qualifier_id)
        if qual:
            if dv.qualifier is not None:
                data.append(dv.qualifier.code)
                data.append(dv.qualifier.description)
            else:
                data.append('')
                data.append('')
        if src:
            data.append(series.organization)
            data.append(series.source_description)
            data.append(series.citation)
        if qcl:
            data.append(series.quality_control_level_code)
            data.append(series.quality_control_level.definition)
            data.append(series.quality_control_level.explanation)
        data.append(dv.sample_id)

        writer.writerow(data)

    def write_text_header(self, plainWriter, series, utc, site, var, offset, qual, src, qcl):
        self.write_warning_header(plainWriter)
        self.write_site_information(plainWriter, series, site)
        self.write_variable_and_method_information(plainWriter, series)
        self.write_source_information(plainWriter, series)
        self.write_qualifier_information(plainWriter, series)


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
        plainWriter.write('# VariableName: ' + str(series.VariableObj.VariableNameCV) + '\n')
        plainWriter.write('# ValueType: ' + 'TBD' + '\n')
        plainWriter.write('# DataType: ' + 'TBD' + '\n')
        plainWriter.write('# GeneralCategory: ' + 'TBD' + '\n')
        plainWriter.write('# SampleMedium: ' + 'TBD' + '\n')
        plainWriter.write('# VariableUnitsName: ' + str(series.UnitsObj.UnitsName) + '\n')
        plainWriter.write('# VariableUnitsType: ' + str(series.UnitsObj.UnitsTypeCV) + '\n')
        plainWriter.write('# VariableUnitsAbbreviation: ' + str(series.UnitsObj.UnitsAbbreviation) + '\n')
        plainWriter.write('# NoDataValue: ' + str(series.VariableObj.NoDataValue) + '\n')
        plainWriter.write('# TimeSupport: ' + 'TBD' + '\n')
        plainWriter.write('# TimeSupportUnitsAbbreviation: ' + 'TBD' + '\n')
        plainWriter.write('# TimeSupportUnitsType: ' + 'TBD' + '\n')
        plainWriter.write('# TimeSupportUnitsName: ' + 'TBD' + '\n')
        plainWriter.write('# MethodDescription: ' +
                          str(series.FeatureActionObj.ActionObj.MethodObj.MethodDescription) + '\n')
        plainWriter.write('# MethodLink: ' +
                          str(series.FeatureActionObj.ActionObj.MethodObj.MethodLink) + '\n')
        plainWriter.write('#\n')

    def write_source_information(self, plainWriter, series):
        plainWriter.write('# Source Information\n')
        plainWriter.write('# ----------------------------------\n')
        if(series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj != None):
            plainWriter.write('# Organization: ' +
                              str(series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName) + '\n')
            plainWriter.write('# SourceDescription: ' +
                              str(series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationDescription) +
                              '\n')
            plainWriter.write('# SourceLink: ' +
                              str(series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationLink) + '\n')
            plainWriter.write('# ContactName: ' +
                              str(series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.
                                  AffiliationObj.PersonObj.PersonFirstName) + ' ' + (
                                  series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.
                                  AffiliationObj.PersonObj.PersonLastName
                                  ) + '\n')
            plainWriter.write('# SourceLink: ' +
                              str(series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.AffiliationObj.PrimaryPhone) + '\n')
            plainWriter.write('# SourceLink: ' +
                              str(
                                  series.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.AffiliationObj.PrimaryEmail) + '\n')
            plainWriter.write('# Citation: ' + 'TBD' + '\n')

        plainWriter.write('#\n')

    def write_qualifier_information(self, plainWriter, series):
        plainWriter.write('# Qualifier Information\n')
        plainWriter.write('# ----------------------------------\n')
        plainWriter.write('# Code   Description\n')
        plainWriter.write('# LI     Linear Interpolation\n')
        plainWriter.write('# SM     Sensor Malfunction\n')
        plainWriter.write('# PF     Power Failure\n')
        plainWriter.write('# S      Suspicious Values\n')
        plainWriter.write('# MNT    Erroneous or missing data due to maintenance\n')
        plainWriter.write('#\n')
        plainWriter.write('#\n')
