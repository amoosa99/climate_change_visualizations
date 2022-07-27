import plotly.express as px
import pandas as pd
import numpy as np

"""A script that creates a bar plot of average temperature change over time
for different regions of the world. The data is taken from the FAO website,
and all temperature change values are relative to a baseline established from
1951-1980"""

class TempBarPlot():

    """A histogram showing global average temperature rise over time.
    Also shows temperature change per continent"""

    def __init__(self):

        #retrieves the temperature data by world region
        self.frame = self.get_region_data()

        #cleans up the data
        self.cleanup_data()

        #creates the chart
        self.make_plot()

    #loads a CSV file containing temperature data by world region
    def get_region_data(self):

        frame = pd.read_csv("Temp_Change_Regions.csv", encoding='cp1252')
        return frame

    #removes irrelevant rows
    #formats dataframe for easier plotting
    def cleanup_data(self):

         #keeps only rows corresponding to temperature change
        keep_temp = self.frame['Element Code'] == 7271

        #keeps rows that represent an entire year
        keep_years = self.frame['Months Code'] == 7020

        self.frame = self.frame[keep_temp & keep_years]

        #removes the 'Y' in the year column names
        remove_y_dict = {}
        for year in self.frame.columns[7:]:

            remove_y_dict[year] = year[1:]

        self.frame = self.frame.rename(columns=remove_y_dict)

        #converts year columns into a year variable
        self.frame = pd.melt(self.frame,id_vars=["Area"],
                             value_vars=self.frame.columns[7:],
                             var_name="Year",value_name="Temp_Change")

        year_series = self.frame["Year"].unique()

        #convert areas into columns
        self.frame = pd.pivot_table(self.frame, index="Year", columns="Area", values="Temp_Change")

        #add back year column
        self.frame.insert(0, "Year", year_series)

    
    #creates the bar chart
    def make_plot(self):

        #creates bar plot
        temp_bar = px.bar(self.frame, x="Year",
                        y="World",
                        color="World",
                        color_continuous_scale="RdBu_r",
                        color_continuous_midpoint=0)

        #creates a list of buttons
        button_list = self.make_buttons()

        #creates a dropdown menu to select world region
        temp_bar.update_layout(
            updatemenus=[
                dict(
                    buttons = button_list,
                    active = len(button_list)-1,
                    y=0.95
                )
            ]
        )

        #add labels to plot
        self.add_labels(temp_bar)

        temp_bar.show()

    #creates a list of buttons for each world region in the data file
    def make_buttons(self):

        button_list = []

        for area in self.frame.columns[1:]:

            button = {}

            button['label'] = area
            button['method'] = "restyle"
            button['args'] = [{"y": [self.frame[area]],
                               "marker.color": [self.frame[area]]}]

            button_list.append(button)

        return button_list
    
    #adds labels to the plot such as titles, axis labels, and hover text
    def add_labels(self, plot):

        #adds axes and colorbar labels
        plot.update_yaxes({'type': "linear",
                                   'title': "Temperature Change from " + \
                                            "Baseline (C)"})
        plot.update_coloraxes(colorbar_title={
                                        'text': "Temp. Change (C)"})

        #adds plot title
        plot.update_layout(title={'text': "Temperature Change " + \
                                                  "Over Time " + \
                                                  "(Compared to 1951-1980 " + \
                                                  "Baseline)",
                                          'x': 0.55,
                                          'xanchor': "center"})

        #adds annotation to dropdown menu
        plot.update_layout(annotations = [
            dict(text="World Region:", x=-0.2, y=0.98,
                 xref="paper", yref="paper",
                 showarrow=False)
        ])
        
        #formats tooltip text
        hover = "Year: %{x} <br>Temp Change (C): %{y}<extra></extra>"
        plot.update_traces(hovertemplate=hover)

if __name__ == "__main__":

    temp_bar_plot = TempBarPlot()