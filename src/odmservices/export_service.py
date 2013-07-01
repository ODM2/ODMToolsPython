import csv
import xml.etree.cElementTree as ET

class ExportService():

	'''
	Create with the Service Manager!!!
	'''
	def __init__(self, series_service):
		self._series_service = series_service

	def export_series_data(self, series_id, filename, utc=False, site=False, var=False, offset=False, qual=False, src=False, qcl=False):
		series = self._series_service.get_series_by_id(series_id)
		if series is None:
			return False

		writer = csv.writer(open(filename, 'wb'))
		self.write_data_header(writer, utc, site, var, offset, qual, src, qcl)
		for dv in series.data_values:
			self.write_data_row(writer, series, dv, utc, site, var, offset, qual, src, qcl)


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
			data.append(series.site.site_type)
			data.append(series.site.latitude)
			data.append(series.site.longitude)
			data.append(series.site.spatial_reference.srs_name)
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

	def export_series_metadata(self, series_ids, filename):
		if len(series_ids) == 0:
			return

		root = ET.Element("Metadata")
		list_root = ET.SubElement(root, "DataSeriesList")
		list_root.set("Total", len(series_ids))

		try:
			with open(filename): file_exists = True
		except IOError:
			file_exists = False

		if file_exists:
			# Read the file into the XML tree
			pass
		
		for series_id in series_ids:
			series = self._series_service.get_series_by_id(series_id)
			site = series.site
			variable = series.variable
			method = series.method
			source = series.source
			qcl = series.quality_control_level
			offsets = self._series_service.get_offset_types_by_series_id(series.id)
			
