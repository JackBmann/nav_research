# nav_research
## Navigation Algorithm Research
Jack Baumann and Micheal Bolot under supervision of Dr. David Andrews at The University of Dallas.

After setting up the Python dependencies (instructions below), run Test.py.  Test.py will create 
a graph from the specified shapefile.  To view the graph, open the specified file name in nav_research\graph_displays\generated\\.

The map data is sourced from OpenStreetMaps (an open-data portal for maps, OSM: <https://www.openstreetmap.org>).  We used QGIS (a free and open-source GIS tool found here: <https://qgis.org/en/site/>) to extract, view, and manipulate the GIS data.

---
##### To extract OSM Data via QGIS, do the following:
1) Install QGIS from <https://qgis.org/en/site/forusers/download.html>.  We used version 3.2.2.
2) Open QGIS and go to Plugins -> Manage and Install Plugins...
    1) Search for and install the following plugins:
        1) OpenLayers Plugin
        2) OSMDownloader
    2) Optional plugins that may be helpful:
        - OSM place search
        - OSM Tools
3) Go to Web -> OpenLayers Plugin -> OpenStreetMap -> OpenStreetMap.
4) Zoom in and navigate to the location you would like to extract.
5) Open the OSMDownloader Selector which should've been installed on the toolbar.
    1) Click and drag the cursor to select a rectangular area on the map
    2) Select a path and filename to save the .osm extract to.
    3) If you would like to view or manipulate the data, select: Load layer after download.
    4) Hit OK
6) The map extract will download to the specified location.  A path to this .osm file (or any of the extracts in nav_research\shapefiles\\) can be be passed to OSMParser.parse_osm() to convert it into a Graph.
---
##### Dependencies include:
Python 3,
GDAL,
plotly,
networkx
##### To set up the proper python environment:
1) Install Anaconda for Python 3 from <https://www.anaconda.com/download/>.
2) Open the Anaconda Prompt and run:
    1) `conda install gdal`
    2) `conda install plotly`
3) Anaconda will create a python environment with the required dependencies installed.
4) Run the project with the conda interpreter.  If you're using PyCharm do the following:
    1) Go to File -> Settings -> Project: nav_research -> Project Interpreter.
    2) Click the dropdown and Show All.
    3) Hit + to add a new environment.
    4) Choose Conda Environment -> Existing Environment.
    5) Navigate to the path of the installed conda environment.
    6) Hit "Okay" and back out of the menus and let PyCharm reconfigure before running the project.

If you have complications with pandas, feel free to uninstall it.  Pandas is not a dependency for this project.

