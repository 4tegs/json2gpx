# ##########################################################################################
# traccar2gpx
# Hans Straßgütl
#
# Konvertiere JSON nach GPX
# ..........................................................................................
#
#	Argumente:	keine
#
#	Abhängigkeiten:
#				traccar-get.json			JSON File für Testzwecke
#		Python:
#				pip install requests
#               Doesn't work under Windows - IN SEQUENCE: geopy, pyproj, shapely, pyogrio geopandas
#
#	Begleitinformationen:
#				https://www.programiz.com/python-programming/json
#
#				GPX Converter
#				https://pypi.org/project/gpx-converter/
#				https://github.com/nidhaloff/gpx-converter
#				https://gpx-converter.readthedocs.io/en/latest/gpx_converter.html
#
#				GPX_Pi
#				https://pypi.org/project/gpxpy/
#
#               Menüs
#               https://tkdocs.com/tutorial/firstexample.html
#
# ------------------------------------------------------------------------------------------
# Stand:
#	2022 10 01	Start Programmierung
#
# ##########################################################################################

# ------------------------------------------------------------------------------------------
# My imports
# ------------------------------------------------------------------------------------------
import os
import geopandas as gpd

# ------------------------------------------------------------------------------------------
# Convert Logic
# ------------------------------------------------------------------------------------------
def convert_json2gpx(filename,trackname):
    work_dir, work_file = os.path.split(filename)								# split the file from path. As working path we use the parameters path set in the Batch file.
    filename = work_file															# Now we have the bare name
    if os.path.exists(filename):    
        filename_tup = os.path.splitext(filename)
        filename = filename_tup[0]
        json_filename = filename + '.json'
        gpx_filename = filename + '.gpx'
        gdf = gpd.read_file(json_filename)
        gdf.to_file(gpx_filename, 'GPX')
    else: 
        print("Die Datei gibt es nicht")
        exit

if __name__ == "__main__":
	convert_json2gpx(traccar-get.json,"Test")

