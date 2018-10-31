# nav research
## Navigation Algorithm Research
Jack Baumann and Micheal Bolot under supervision of Dr. David Andrews at The University of Dallas.

After setting up the Python dependencies (instructions below), run Test.py.  Test.py will create 
a graph from the specified shapefile.  To view the graph open nav_research/GraphDisplay.html.

The data is sourced from USGS.  We used QGIS to view and manipulate the shapefile data.

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
