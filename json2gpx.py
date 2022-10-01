# ##########################################################################################
# json 2 gpx
# Hans Straßgütl
#
# Konvertiere JSON nach GPX
# ..........................................................................................
#
#   Argumente:  keine
#
#   Anmerkungen:
#               Ich hatte zuerst versucht GEOPANDAS zu installieren und zu nutzen. Das kann jedoch nur GeoJson, Traccar exportiert nur JSON
#               Somit hat das nicht geklappt.
#           
#
#   Begleitinformationen:
#               https://www.programiz.com/python-programming/json
#
#               GPX Converter
#               https://pypi.org/project/gpx-converter/
#               https://github.com/nidhaloff/gpx-converter
#               https://gpx-converter.readthedocs.io/en/latest/gpx_converter.html
#
#               GPX_Pi
#               https://pypi.org/project/gpxpy/
#
#               Menüs
#               https://tkdocs.com/tutorial/firstexample.html
#
# ------------------------------------------------------------------------------------------
# Stand:
#   2022 10 01  Start Programmierung
#
# ##########################################################################################

# ------------------------------------------------------------------------------------------
# My imports
# ------------------------------------------------------------------------------------------
import json
import argparse
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import sys
from gpx_converter import Converter
import os
import openpyxl
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

# ------------------------------------------------------------------------------------------
# Errorsections
#   1       Configuration file is missing
#   2       JSON inputfile is missing
# ------------------------------------------------------------------------------------------
def config_error(error):
    # get the current path of where the program is started
    path = os.getcwd()
    root = Tk()
    root.title("Error!!")
    root.eval('tk::PlaceWindow . center')

    mainframe = ttk.Frame(root, padding="25 25 25 25")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    quitbutton = ttk.Button(mainframe, text='Exit', command=quitme)
    quitbutton.grid(column=1, row=3, sticky="S")

    if error == 1:
        ttk.Label(mainframe, text="The configuration file is missing.").grid(
            column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="It should say here: " +
                  path).grid(column=1, row=2, sticky=W)

    if error == 2:
        ttk.Label(mainframe, text="The JSON Inputfile is missing.").grid(
            column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Choose right filename").grid(
            column=1, row=2, sticky=W)

    if error == 3:
        ttk.Label(mainframe, text="The JSON File has been converted").grid(
            column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Check your directory").grid(
            column=1, row=2, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    quitbutton.focus()
    root.bind("<Return>", quitme)
    root.protocol("WM_DELETE_WINDOW", quitme)
    root.mainloop()

# ------------------------------------------------------------------------------------------
# End Program
# ------------------------------------------------------------------------------------------
def quitme():
    print("Tschüss!")
    quit()

# ------------------------------------------------------------------------------------------
# delete a file if it exists
# ------------------------------------------------------------------------------------------
def delete_file(a):                                                                     # Delete Files no longer needed. Called by main routine
    if os.path.exists(a):
        os.remove(a)

# ------------------------------------------------------------------------------------------
# Cleaning the GPX so that it can be imported by any Garmin product
#   - setting the right header - the one provided by GPX Converter is wrong!
#   - providing names to tracks
#   - setting track color
# ------------------------------------------------------------------------------------------
def clean_my_gpx(gpx_filename,trackname,trackcolor):
    # work_dir, work_file = os.path.split(gpx_filename)
    # gpx_filename = gpx_filename + ".gpx"                                            # Erstelle den GPX Dateinamen
    lines = []                                                                      # Initialisiere die Liste der Strings für das spätere einlesen
    Track_Counter = 0
    # Öffne die GPX Datei. Stelle sicher, dass sie im UTF-8 Format gelesen wird. Gut erklärt hier: https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open(gpx_filename, encoding='utf8') as f:
        # Lese alle Zeilen in eine Liste von Strings (lines)
        lines = f.readlines()
                                                                                    # Wenn du die Datei mit with geöffnet hast, so schliesst das die Datei direkt im Anschluß
    with open(gpx_filename, 'w') as f:                                              # Öffne die Datei zum schreiben. Gut erklärt hier: https://www.pythontutorial.net/python-basics/python-write-text-file/
        for line in lines:                                                          # Nun gehe Zeile für Zeile (Liste von lines) 
            search = line.strip()                                               
            search_item = search.find('<gpx xmlns=')
            if search_item > -1: line = '<gpx creator="mail@hs58.de" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">\n'
            f.write(line)                                                           # Schreibe die Zeile raus
            if line.strip() == '<trk>':                                             # Wenn die Zeile den <trk> eröffnet, 
                Track_Counter += 1
                f.write("    <name>" + trackname + "-" + str(Track_Counter) + "</name>\n")  # dann schreibe den Tracknamen hinterher!                
                f.write("    <extensions>\n")
                f.write("      <gpxx:TrackExtension>\n")
                f.write("        <gpxx:DisplayColor>" + trackcolor + "</gpxx:DisplayColor>\n")
                f.write("      </gpxx:TrackExtension>\n")
                f.write("    </extensions>\n")

# ------------------------------------------------------------------------------------------
# Convert Logic JSON -> GPX
#   Converts a JSON from Traccar to a valid GPX V1.1 format
# ------------------------------------------------------------------------------------------
def convert_json2gpx(filename, trackname, trackcolor):
    # split the file from path. As working path we use the parameters path set in the Batch file.
    work_dir, work_file = os.path.split(filename)
    filename = work_file                                                            # Now we have the bare name
    if os.path.exists(filename):
        filename_tup = os.path.splitext(filename)
        filename = filename_tup[0]
        json_filename = filename + '.json'
        gpx_filename = filename + '.gpx'
        delete_file(gpx_filename)
        Converter(input_file=json_filename).json_to_gpx(
                                                lats_colname='latitude',
                                                longs_colname='longitude',
                                                times_colname='deviceTime',
                                                alts_colname='altitude',
                                                output_file=gpx_filename)
        clean_my_gpx(gpx_filename,trackname,trackcolor)
        config_error(3)
    else:
        # print("Die Datei gibt es nicht")
        config_error(2)
        # exit




# ------------------------------------------------------------------------------------------
# Hauptprogram
# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    trackcolor = "Magenta"
    trackcolor = "Blue"
    MyFileName = "traccar-get.json"
    MyTrackname = "TestMe"
    convert_json2gpx(MyFileName,MyTrackname,trackcolor)


