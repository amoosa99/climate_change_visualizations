import plotly.express as px
import rasterio as rio
import numpy as np
import os

"""A script that creates an equal-area map showing the surface temperature
of Arctic sea ice over time. The ice surface temperature data is taken from
the NASA MODIS/Aqua data (MYD29P1D) and each year's data was taken on Sept. 1
of that year"""

class SeaIceMODIS():

    """A map showing the temperature of sea ice in the Arctic region, defined
    as above the 60th parallel. Data obtained from MODIS Aqua Ice Surface
    Temperature (IST) data"""

    def __init__(self):

        #gets sea ice temperature data for each year
        self.tiffs = self.get_tiffs()

        #creates plot
        self.make_plot()

    #gets sea ice temperatures for each year from geoTIFF files
    def get_tiffs(self):

        #a dictionary containing each geoTIFF file indexed by year
        tiff_dict = {}

        #adds each files contents to dictionary
        for subdir, dirs, files in os.walk(".\\modis\\IST"):

            for filename in files:

                #checks for TIFF file
                ext = filename.split(".")[-1]

                if ext == "tif":

                    #gets year from filename
                    year = int(filename.split(".")[0])
                    
                    #reads in data from the file into the dictionary
                    with rio.open(".\\modis\\IST\\"+filename) as tiff:

                        tiff_dict[year] = self.get_tiff_data(tiff)
                        
        return tiff_dict

    #processes data from an opened sea ice temperature geoTIFF file
    def get_tiff_data(self, tiff):

        #reads the first band in the file
        data = tiff.read(1)

        #removes invalid measurements (5000 or below)
        data = np.where(data > 5000, data, np.NaN)

        #multplies by 0.01 to convert temperatures to Kelvins
        data = data*0.01

        return data

    #creates plot of sea ice temperatures over time
    def make_plot(self):

        #computes axis values for the x and y axis
        axis = self.compute_axis()

        #constructs the figure
        sea_ice_temp = px.imshow(self.tiffs[2002], x=axis, y=axis,
                                 color_continuous_scale="RdBu_r",
                                 color_continuous_midpoint=273)

        #a slider to change the year displayed
        sea_ice_temp.update_layout(sliders=[dict(
                                active=2002,
                                currentvalue= {"prefix": "September 1, "},
                                pad = {"t": 50},
                                steps = [dict(label=i,method='restyle',
                                              args=[{"z": [self.tiffs[i]]}]) 
                                              for i in range(2002,2021)]
        )])

        #adds labels to the plot
        self.add_labels(sea_ice_temp)

        #displays the figure
        sea_ice_temp.show()

    #calculates values for the x and y axis based on the files' resolution
    #same list for both x and y axis since the plot is a square
    def compute_axis(self):

        #the number of points in the TIFF files
        #the first one is used since all of them have the same resolution
        length = len(self.tiffs[2002][:])

        #offsets the axes to place the origin in the center
        offset = length//2

        #the resolution of the TIFFs in kilometers
        #set when converting HDF data to TIFF format
        res = 20

        #computes axis values based on resolution
        axis = [res*num for num in range(-offset, length-offset)]

        return axis
    
    #adds labels to the plot such as titles, axis labels, and hover text
    def add_labels(self, plot):

        #adds axis and colorbar labels
        plot.update_xaxes({'type': "linear", 
                                   'title': "Distance from North Pole (km)",
                                   'side': "top"})
        plot.update_yaxes({'type': "linear",
                                   'title': "Distance from North Pole (km)"})
        plot.update_coloraxes(colorbar_title={
                                        'text': "Temperature (K)"})

        #adds plot title
        plot.update_layout(title={'text': "Arctic Sea Ice " + \
                                                  "Surface Temperature " + \
                                                  "(September 1)",
                                          'x': 0.5,
                                          'y': 0.12,
                                          'xanchor': "center"})
        
        #formats tooltip text
        hover = "X: %{x} <br>Y: %{y} <br>Temp (K): %{z}<extra></extra>"
        plot.update_traces(hovertemplate=hover)

if __name__ == "__main__":

    sea_ice_temp = SeaIceMODIS()

