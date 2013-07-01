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
		list_root.set("Total", str(len(series_ids)))

		try:
			with open(filename): file_exists = True
		except IOError:
			file_exists = False

		if file_exists:
			# Read the file into the XML tree
			pass
		
		for series_id in series_ids:
			series = self._series_service.get_series_by_id(series_id)
			self.append_series_node(series, list_root)

		tree = ET.ElementTree(root)
		tree.write(filename)

	def append_series_node(self, series, parent):
		series_node = ET.SubElement(parent, "DataSeries")
		series_node.set("ID", str(series.id))
		self.append_general_info(series, series_node)
		self.append_site_info(series, series_node)
		self.append_var_info(series, series_node)

		return series_node
		
	def append_general_info(self, series, parent):
		meta = series.source.iso_metadata
		general_node = ET.SubElement(parent, "GeneralInformation")
		topic = ET.SubElement(general_node, "TopicCategory")
		topic.text = meta.topic_category
		title = ET.SubElement(general_node, "Title")
		title.text = meta.title
		abstract = ET.SubElement(general_node, "Abstract")
		abstract.text = meta.abstract
		prof_version = ET.SubElement(general_node, "ProfileVersion")
		prof_version.text = meta.profile_version
		metadata_link = ET.SubElement(general_node, "MetadataLink")
		metadata_link.text = meta.metadata_link
		date = ET.SubElement(general_node, "MetadataCreationDate")
		# 7/1/2013 12:17:16 PM
		import datetime
		date.text = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")

	def append_site_info(self, series, parent):
		site = series.site
		site_node = ET.SubElement(parent, "SiteInformation")
		site_code = ET.SubElement(site_node, "SiteCode")
		site_code.text = site.code
		site_name = ET.SubElement(site_node, "SiteName")
		site_name.text = site.name
		site_type = ET.SubElement(site_node, "SiteType")
		site_type.text = site.type

		geo_coords = ET.SubElement(site_node, "GeographicCoordinates")
		latitude = ET.SubElement(geo_coords, "Latitude")
		latitude.text = str(site.latitude)
		longitude = ET.SubElement(geo_coords, "Longitude")
		longitude.text = str(site.longitude)
		srs_id = ET.SubElement(geo_coords, "SRSID")
		srs_id.text = str(site.spatial_ref.srs_id)
		srs_name = ET.SubElement(geo_coords, "SRSName")
		srs_name.text = site.spatial_ref.srs_name
		is_geo = ET.SubElement(geo_coords, "IsGeographic")
		is_geo.text = str(site.spatial_ref.is_geographic)
		notes = ET.SubElement(geo_coords, "Notes")
		notes.text = site.spatial_ref.notes
		
		local_coords = ET.SubElement(site_node, "LocalCoordinates")
		local_x = ET.SubElement(local_coords, "LocalX")
		local_x.text = str(site.local_x)
		local_y = ET.SubElement(local_coords, "LocalY")
		local_y.text = str(site.local_y)
		local_srs_id = ET.SubElement(local_coords, "SRSID")
		local_srs_id.text = str(site.local_spatial_ref.srs_id)
		local_srs_name = ET.SubElement(local_coords, "SRSName")
		local_srs_name.text = site.local_spatial_ref.srs_name
		local_is_geo = ET.SubElement(local_coords, "IsGeographic")
		local_is_geo.text = str(site.local_spatial_ref.is_geographic)
		local_notes = ET.SubElement(local_coords, "Notes")
		local_notes.text = site.local_spatial_ref.notes
		elevation = ET.SubElement(local_coords, "Elevation_m")
		if site.elevation_m: elevation.text = str(site.elevation_m)
		vert_datum = ET.SubElement(local_coords, "VerticalDatum")
		if site.vertical_datum_id: vert_datum.text = str(site.vertical_datum_id)

		pos_accuracy = ET.SubElement(site_node, "PosAccuracy_m")
		pos_accuracy.text = str(site.pos_accuracy_m)
		state = ET.SubElement(site_node, "State")
		state.text = site.state
		county = ET.SubElement(site_node, "County")
		county.text = site.county
		comments = ET.SubElement(site_node, "Comments")
		comments.text = site.comments

	def append_var_info(self, series, parent):
		variable = series.variable 
		var_node = ET.SubElement(parent, "VariableInformation")

		var_code = ET.SubElement(var_node, "VariableCode")
		var_code.text = variable.code
		var_name = ET.SubElement(var_node, "VariableName")
		var_name.text = variable.name
		speciation = ET.SubElement(var_node, "Speciation")
		speciation.text = variable.speciation

		var_units = ET.SubElement(var_node, "VariableUnits")
		units_name = ET.SubElement(var_units, "UnitsName")
		units_name.text = variable.variable_unit.name
		units_type = ET.SubElement(var_units, "UnitsType")
		units_type.text = variable.variable_unit.type
		units_abbrev = ET.SubElement(var_units, "UnitsAbbreviation")
		units_abbrev.text = variable.variable_unit.abbreviation

		sample_medium = ET.SubElement(var_node, "SampleMedium")
		sample_medium.text = variable.sample_medium
		val_type = ET.SubElement(var_node, "ValueType")
		val_type.text = variable.value_type
		is_reg = ET.SubElement(var_node, "IsRegular")
		is_reg.text = str(variable.is_regular)
		time_support = ET.SubElement(var_node, "TimeSupport")
		time_support.text = str(variable.time_support)

		time_support_units = ET.SubElement(var_node, "TimeSupportUnits")
		ts_units_name = ET.SubElement(time_support_units, "UnitsName")
		ts_units_name.text = variable.time_unit.name
		ts_units_type = ET.SubElement(time_support_units, "UnitsType")
		ts_units_type.text = variable.time_unit.type
		ts_units_abbrev = ET.SubElement(time_support_units, "UnitsAbbreviation")
		ts_units_abbrev.text = variable.time_unit.abbreviation

		data_type = ET.SubElement(var_node, "DataType")
		data_type.text = variable.data_type
		gen_cat = ET.SubElement(var_node, "GeneralCategory")
		gen_cat.text = variable.general_category
		no_dv = ET.SubElement(var_node, "NoDataValue")
		no_dv.text = str(variable.no_data_value)
		 