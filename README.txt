Description:

This project contains three visualizations of global temperature change. 
It has a world map showing countries' surface temperature changes since 1962,
a bar chart showing temperature change by year for each world region, and 
a map of sea ice temperature in the Arctic. 

Each visualization is interactive and made in Python's plotly module.
More information on plotly can be found at https://plotly.com/

Requirements:

Python Version: 3.7
Operating System: Windows 10
Recommended Browser: Firefox

Please use the following steps to view the visualizations.


Preparing the Virtual Environment

1. Navigate to this project's directory in the command line
2. Create a Python virtual environment using the following command:
	
	python -m venv venv

3. Activate the virtual environment using the following command:

	.\venv\Scripts\activate

4. Install the required packages using the following command:

	pip install -r Requirements.txt


Running the Scripts

1. Navigate to the "src" folder in the command line
2. Navigate to the folder corresponding to the script that you would like
   to run using the command line
3. Run the script using the following command:

	python [script_name_here]

4. The visualization will load and appear in your browser where it can be
   interacted with.

Exiting Virtual Enviroment

1. When done viewing visualizations, exit the virtual environment by typing
   "deactivate" on the command line.
2. If you would like the delete the virtual environment from your machine,
   delete the "venv" folder in this project's directory.

Data Sources

Global temperature data by region and country is from the Food and Agriculture
Organization of the United Nations 
(http://www.fao.org/faostat/en/#data/ET/visualize)

Sea ice extent/temperature data is from NASA MODIS/Aqua data 
(dates/times used: 2002-2021, 09-01, 00:00-23:59). 
The data was converted into TIFF format using the Python pymodis module.

