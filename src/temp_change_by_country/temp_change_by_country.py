import plotly.express as px
import pandas as pd
import numpy as np
import json

"""A script that creates a choropleth map using temperature change data
by country from the FAO website. Temperature change values are relative
to a baseline established from 1951-1980"""

class TempChangeChoropleth():

    """A choropleth plot showing surface temperatures across different
    countries over time"""

    def __init__(self):

        #retrieves geoJSON data for countries
        self.geo = self.get_geo()

        #retrieves the temperature data for each country
        self.frame = self.get_country_data()

        #adds country IDs to dataframe
        self.add_country_ids()

        #cleans up data
        self.cleanup_data()

        #creates the map
        self.make_plot()

    #loads geoJSON data
    def get_geo(self):
        
        geo_file = open("countries.geojson")
        countries = json.loads(geo_file.read())
        return countries

    #loads a CSV file containing temperature data by country
    def get_country_data(self):

        frame = pd.read_csv("Temp_Change_Countries.csv", encoding='cp1252')
        return frame

    #adds country ID column to dataframe to match geoJSON file
    def add_country_ids(self):

        #dictionary of country IDs from geoJSON file
        country_ids = {}

        #populates dictionary with country IDs
        for feature in self.geo["features"]:

            country_name = feature["properties"]["ADMIN"]
            country_id = feature["properties"]["ISO_A3"]

            country_ids[country_name] = country_id

        #countries not in geoJSON get a NaN ID
        for country in self.frame["Area"].unique():

            if country not in country_ids.keys():

                country_ids[country] = np.NaN

        #function to map rows in dataframe to ID value
        def map_ids(row, country_ids):

            return country_ids[row]
            
        #creates country ID series
        country_id_series = self.frame['Area'].apply(map_ids, \
                                                     args = (country_ids,))

        #inserts country IDs into dataframe
        self.frame.insert(0, 'Country_ID', country_id_series)

    #removes irrelevant rows
    #formats dataframe for easier plotting
    def cleanup_data(self):

        #keeps rows that represent an entire year
        keep_years = self.frame['Months Code'] == 7020

        #keeps only rows corresponding to temperature change
        keep_temp = self.frame['Element Code'] == 7271

        #keeps rows that have a country ID in the geoJSON file
        keep_country_id = self.frame['Country_ID'].notnull()

        #applies conditions to dataframe
        self.frame = self.frame[keep_years & keep_temp & keep_country_id]

        #drops irrelevant columns
        cols_to_drop = ['Area Code','Months Code','Months','Element Code', \
                        'Element', 'Unit']
        self.frame = self.frame.drop(columns=cols_to_drop)

        #removes the 'Y' in the year column names
        remove_y_dict = {}
        for year in self.frame.columns[2:]:

            remove_y_dict[year] = year[1:]

        self.frame = self.frame.rename(columns=remove_y_dict)

    #makes the choropleth map based on temperature data
    def make_plot(self):
        
        #generates choropleth map
        temp_map = px.choropleth(self.frame, geojson=self.geo,
                                 locations='Country_ID',
                                 featureidkey="properties.ISO_A3",
                                 color=self.frame["1962"],
                                 color_continuous_scale="RdBu_r",
                                 color_continuous_midpoint=0,
                                 projection="equirectangular")

        #adds a slider to change year
        temp_map.update_layout(sliders=[dict(
                                active=1962,
                                currentvalue= {"prefix":"Year: "},
                                pad = {"t": 50},
                                steps = [dict(label=i,method='restyle',
                                              args=[{"z": [self.frame[str(i)]]}]) 
                                              for i in range(1962,2020)]
        )])

        #adds menu to change projection of the map
        temp_map.update_layout(
            updatemenus=[
                dict(
                    buttons = list([
                        dict(
                        label="Equirectangular",
                        method="relayout",
                        args=[{"geo.projection.type": "equirectangular"}]
                        ),
                        dict(
                            label="Robinson",
                            method="relayout",
                            args=[{"geo.projection.type": "robinson"}],
                        )
                    ]),
                    y=0.95
                )
            ]
        )

        #adds labels to plot
        self.add_labels(temp_map)

        temp_map.show()
    
    #adds labels to the plot such as titles, axis labels, and hover text
    def add_labels(self, plot):

        #adds colorbar label
        plot.update_coloraxes(colorbar_title={
                                        'text': "Temp. Change (C)"})

        #adds plot title
        plot.update_layout(title={'text': "Temperature Change " + \
                                                  "by Country " + \
                                                  "(from 1951-1980 Baseline)",
                                          'x': 0.5,
                                          'xanchor': "center"})

        #adds annotation to dropdown menu
        plot.update_layout(annotations = [
            dict(text="Map Projection", x=-0.13, y=0.98,
                 showarrow=False)
        ])
        
        #formats tooltip text
        hover = "Country: %{location} <br>Temp Change (C): %{z}<extra></extra>"
        plot.update_traces(hovertemplate=hover)

if __name__ == "__main__":

    choropleth = TempChangeChoropleth()