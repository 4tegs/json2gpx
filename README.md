# json2gpx
Convert file from JSON to GPX

# Start
* Use a JSON from Traccar
* Output a GPX
* use given names - no query

---
## Prerequisites
There is a need to setup GEOPANDAAS before we can use the code:

Depending on your platform there are different ways to go.
### Windows
You first need to check your Python version:  
``python --version``  

There is a dependency for **fiona**, a package that provides binary wheels with the dependencies included for Mac and Linux, but not for Windows.  
Thus, we first need to download the Windows wheel for fiona. They have provided the source on the geopandas installation page: [Christopher Gohlke’s website](https://www.lfd.uci.edu/~gohlke/pythonlibs/).  

On this website, the unofficial wheel files for various packages are found. Search for fiona on this site, and download the whl file for your python version, and your Windows type. 

I’m using Python 3.9, and 64-bits Windows machine. Thus, I’ll go with Fiona-1.8.21-cp39-cp39-win_amd64.whl. Over here, 1.8.21 refers to the version of fiona. At the time of writing this Read.me, this is the latest version. Download that whl file, and note its location. On my machine, it is saved in the Downloads folder. The complete path is C:/Users/**/Downloads/Fiona-1.8.21-cp39-cp39-win_amd64.whl.

Next, search for gdal on the same website, and download the latest version matching your python version and Windows type. I downloaded GDAL-3.4.3-cp39-cp39-win_amd64.whl, in the same Downloads folder. GDAL is required for Fiona to get installed.

Now Copy both files to your working directory as pip doesn't like the windows pathes.

Now, within your working directory, install GDAL followed by Fiona using pip install
``
pip install GDAL-3.3.1-cp38-cp38-win_amd64.whl

pip install Fiona-1.8.19-cp38-cp38-win_amd64.whl
``
Both GDAL and Fiona should get installed. Now try installing geopandas.

``pip install geopandas``


