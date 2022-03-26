
import pandas as pd
from bokeh.io import output_notebook, output_file
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models.tools import HoverTool
import math
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.tile_providers import get_provider, Vendors
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
from pymongo import MongoClient

# Create a custom read function to read data from mongodb into a dataframe
#def read_mongo(host='127.0.0.1', port=27017, username=None, password=None, db='Quake', collection='pred_results'):
def read_mongo(host='mongo', port=27017, username='root', password='go2team', db='Quake', collection='pred_results'):
    
    mongo_uri = 'mongodb://{}:{}@{}:{}/{}.{}?authSource=admin'.format(username, password, host, port, db, collection)
    
    # Connect to mongodb
    conn = MongoClient(mongo_uri)
    db = conn[db]
    
    # Select all records from the collection
    cursor = db[collection].find()
    
    # Create the dataframe
    df = pd.DataFrame(list(cursor))
    
    # Delete the _id field
    del df['_id']
    
    return df


# Load the datasets from mongodb
df_quakes = read_mongo(collection='quakes')
df_quake_freq = read_mongo(collection='quake_freq')
df_quake_pred = read_mongo(collection='pred_results')
df_quakes_2016 = df_quakes[df_quakes['Year'] == 2016]


# Create custom style function to style our plots
def style(p):
    # Title
    p.title.align='center'
    p.title.text_font_size='20pt'
    p.title.text_font='serif'
    
    # Axis titles
    p.xaxis.axis_label_text_font_size='14pt'
    p.xaxis.axis_label_text_font_style='bold'
    p.yaxis.axis_label_text_font_size='14pt'
    p.yaxis.axis_label_text_font_style='bold'
    
    # Tick labels
    p.xaxis.major_label_text_font_size='12pt'
    p.yaxis.major_label_text_font_size='12pt'
    
    # Plot the legend in the top left corner
    p.legend.location='top_left'
    
    return p
    

# Create the Geo Map plot
def plotMap():
    lat = df_quakes_2016['Latitude'].values.tolist()
    lon = df_quakes_2016['Longitude'].values.tolist()
    
    pred_lat = df_quake_pred['Latitude'].values.tolist()
    pred_lon = df_quake_pred['Longitude'].values.tolist()
    
    lst_lat = []
    lst_lon = []
    lst_pred_lat = []
    lst_pred_lon = []
    
    i=0
    j=0
    
    # Convert Lat and Long values into merc_projection format
    for i in range(len(lon)):
        r_major = 6378137.000
        x = r_major * math.radians(lon[i])
        scale = x/lon[i]
        y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 +
            lat[i] * (math.pi/180.0)/2.0)) * scale
        
        lst_lon.append(x)
        lst_lat.append(y)
        i += 1
        
    # Convert predicted lat and long values into merc_projection format
    for j in range(len(pred_lon)):
        r_major = 6378137.000
        x = r_major * math.radians(pred_lon[j])
        scale = x/pred_lon[j]
        y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 +
            pred_lat[j] * (math.pi/180.0)/2.0)) * scale
        
        lst_pred_lon.append(x)
        lst_pred_lat.append(y)
        j += 1
    
    
    df_quakes_2016['coords_x'] = lst_lat
    df_quakes_2016['coords_y'] = lst_lon
    df_quake_pred['coords_x'] = lst_pred_lat
    df_quake_pred['coords_y'] = lst_pred_lon
    
    # Scale the circles
    df_quakes_2016['Mag_Size'] = df_quakes_2016['Magnitude'] * 4
    df_quake_pred['Mag_Size'] = df_quake_pred['Pred_Magnitude'] * 4
    
    # create datasources for our ColumnDataSource object
    lats = df_quakes_2016['coords_x'].tolist()
    longs = df_quakes_2016['coords_y'].tolist()
    mags = df_quakes_2016['Magnitude'].tolist()
    years = df_quakes_2016['Year'].tolist()
    mag_size = df_quakes_2016['Mag_Size'].tolist()
    
    pred_lats = df_quake_pred['coords_x'].tolist()
    pred_longs = df_quake_pred['coords_y'].tolist()
    pred_mags = df_quake_pred['Pred_Magnitude'].tolist()
    pred_year = df_quake_pred['Year'].tolist()
    pred_mag_size = df_quake_pred['Mag_Size'].tolist()
    
    # Create column datasource
    cds = ColumnDataSource(
        data=dict(
            lat=lats,
            lon=longs,
            mag=mags,
            year=years,
            mag_s=mag_size
        )
    )
    
    pred_cds = ColumnDataSource(
        data=dict(
            pred_lat=pred_lats,
            pred_long=pred_longs,
            pred_mag=pred_mags,
            year=pred_year,
            pred_mag_s=pred_mag_size
        )
    )
    
    # Tooltips
    TOOLTIPS = [
        ("Year", " @year"),
        ("Magnitude", " @mag"),
        ("Predicted Magnitude", " @pred_mag")
    ]
    
    # Create figure
    p = figure(title='Earthquake Map',
              plot_width=2300, plot_height=450,
              x_range=(-2000000, 6000000),
              y_range=(-1000000, 7000000),
              tooltips=TOOLTIPS)
    
    p.circle(x='lon', y='lat', size='mag_s', fill_color='#cc0000', fill_alpha=0.7,
            source=cds, legend='Quakes 2016')
    
    # Add circles for our predicted earthquakes
    p.circle(x='pred_long', y='pred_lat', size='pred_mag_s', fill_color='#ccff33', fill_alpha=7.0,
            source=pred_cds, legend='Predicted Quakes 2017')
    
    #p.add_tile(CARTODBPOSITRON)
    p.add_tile(get_provider('CARTODBPOSITRON'))
    
    # Style the map plot
    # Title
    p.title.align='center'
    p.title.text_font_size='20pt'
    p.title.text_font='serif'
    
    # Legend
    p.legend.location='bottom_right'
    p.legend.background_fill_color='black'
    p.legend.background_fill_alpha=0.8
    p.legend.click_policy='hide'
    p.legend.label_text_color='white'
    p.xaxis.visible=False
    p.yaxis.visible=False
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color=None
    
       
    # show(p)

    return p
    
#plotMap()  

# Create the Bar Chart
def plotBar():
    # Load the datasource 
    cds = ColumnDataSource(data=dict(
        yrs = df_quake_freq['Year'].values.tolist(),
        numQuakes = df_quake_freq['Counts'].values.tolist()
    ))
    
    # Tooltip
    TOOLTIPS = [
        ('Year', ' @yrs'),
        ('Number of earthquakes', ' @numQuakes')
    ]
    
    # Create a figure
    barChart = figure(title='Frequency of Earthquakes by Year',
                     plot_height=400,
                     plot_width=1150,
                     x_axis_label='Years',
                     y_axis_label='Number of Occurances',
                     x_minor_ticks=2,
                     y_range=(0, df_quake_freq['Counts'].max() + 100),
                     toolbar_location=None,
                     tooltips=TOOLTIPS)
    
    # Create a vertical bar 
    barChart.vbar(x='yrs', bottom=0, top='numQuakes',
                 color='#cc0000', width=0.75,
                 legend='Year', source=cds)
    
    # Style the bar chart
    barChart = style(barChart)
    
    # show(barChart)
    
    return barChart
    
    
# plotBar()
 


df_quake_freq.sort_values(by=['Year'], axis=0, ascending=True, inplace=True)

df_quake_freq.head()

df_quake_freq.reset_index(drop=True)

# Create a magnitude plot
def plotMagnitude():
    # Load the datasource
    cds = ColumnDataSource(data=dict(
        yrs = df_quake_freq['Year'].values.tolist(),
        avg_mag = df_quake_freq['Avg_Magnitude'].round(1).values.tolist(),
        max_mag = df_quake_freq['Max_Magnitude'].values.tolist()
    ))
    
    # Tooltip
    TOOLTIPS = [
        ('Year', ' @yrs'),
        ('Average Magnitude', ' @avg_mag'),
        ('Maximum Magnitude', ' @max_mag')
    ]
    
    # Create the figure
    mp = figure(title='Maximum and Average Magnitude by Year',
               plot_width=1150, plot_height=400,
               x_axis_label='Years',
               y_axis_label='Magnitude',
               x_minor_ticks=2,
               y_range=(5, df_quake_freq['Max_Magnitude'].max() + 1),
               toolbar_location=None,
               tooltips=TOOLTIPS)
    
    # Max Magnitude
    mp.line(x='yrs', y='max_mag', color='#cc0000', line_width=2, legend='Max Magnitude', source=cds)
    mp.circle(x='yrs', y='max_mag', color='#cc0000', size=8, fill_color='#cc0000', source=cds)
    
    # Average Magnitude 
    mp.line(x='yrs', y='avg_mag', color='yellow', line_width=2, legend='Avg Magnitude', source=cds)
    mp.circle(x='yrs', y='avg_mag', color='yellow', size=8, fill_color='yellow', source=cds)
    
    mp = style(mp)
    
    show(mp)
    
    return mp

plotMagnitude()    

# Display the visuals directly in the browser
output_file('dashboard.html')
# Change to a dark theme
curdoc().theme = 'dark_minimal'

import bokeh
print(bokeh.__version__)

# Build the grid plot
from bokeh.layouts import gridplot, grid

# Make the grid
grid = grid( [ plotMap(), [plotBar(), plotMagnitude()]])

# Show the grid
show(grid)
