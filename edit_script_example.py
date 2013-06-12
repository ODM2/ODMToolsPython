import edit_service
ser = edit_service(cnxn_string, series_id)

ser.filter_value(630, '>')
ser.filter_value(635, '<')

# make sure to initialize all variables
point_list = [
	#values
]
ser.add_points(point_list)

"""
Make new methods, whatever
if needed

new_method = whatever
"""

# either send series_id
# or 5 series identifiers (possibly created above)
ser.save(stuff, new_method.id)
ser.write_to_db()