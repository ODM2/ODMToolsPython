import csv

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
		self.write_header(writer, utc, site, var, offset, qual, src, qcl)
		for dv in series.data_values:
			self.write_row(writer, dv, utc, site, var, offset, qual, src, qcl)


	def write_row(self, writer, dv, utc, site, var, offset, qual, src, qcl):
		row = []
		row.append(dv.series.id)
		row.append(dv.id)
		row.append(dv.data_value)
		row.append(dv.value_accuracy)
		row.append(dv.local_date_time)
		if utc:
			row.append(utc_offset)
			row.append(date_time_utc)
		row.append(dv.site.site_code)
		if site:
			row.append(dv.site.site_name)
			row.append(dv.site.site_type)
			row.append(dv.site.latitude)
			row.append(dv.site.longitude)
			row.append(dv.site.spatial_reference.srs_name)
		row.append(dv.variable.code)
		if var:
			row.append(dv.variable.name)
			row.append(dv.variable.speciation)
			row.append(dv.variable.variable_unit.name)
			row.append(dv.variable.variable_unit.abbreviation)
			row.append(dv.variable.sample_medium)
		row.append(dv.offset_value)
		row.append(dv.offset_type_id)
		if offset:
			row.append(dv.offset_type.description)
			row.append(dv.offset_type.unit.name)
		row.append(dv.censor_code)
		row.append(dv.qualifier_id)
		if qual:
			row.append(dv.qualifier.code)
			row.append(dv.qualifier.description)
		if src:
			row.append(dv.source.organization)
			row.append(dv.source.description)
			row.append(dv.source.citation)
		if qcl:
			row.append(dv.quality_control_level.code)
			row.append(dv.quality_control_level.definition)
			row.append(dv.quality_control_level.explanation)
		row.append(dv.sample_id)

		writer.writerow(row)



	def write_header(self, writer, utc, site, var, offset, qual, src, qcl):
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