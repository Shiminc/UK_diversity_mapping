import math
import warnings
import pandas as pd
import folium

warnings.filterwarnings("ignore")

def restructure_data(data: pd.DataFrame, variable: str, geo_id: str):
    """Clean the variable of concern and pivot the data to be wide format

    Args:
        data (pd.DataFrame): data format churned out by the ONS websites containing at least a column `geo_id`, `variable`, `Observation` which is the count of each category of the variable of concern.
        variable (str): variable that users want to visualise
        geo_id: the variable name that references the geographic level used in the data
      
    
    Returns:
        pd.DataFrame: dataframe in the wide format with columns corresponding to the categories of the variable in concern, with geo_id being the index 
    """   

    data[variable] = data[variable].str.strip(' ')
    df = data[[geo_id, variable, 'Observation']]
    df = pd.DataFrame(df.groupby([geo_id, variable]).Observation.sum()).reset_index()
    df = df.pivot(index = geo_id, columns = variable, values = 'Observation')
    return df


def create_basemap(data: pd.DataFrame, latitude: str, longitude: str):
    """create a basemap with folium.Map centering on the country centre and prevent users going beyond the country boundary

    Args:
        data (pd.DataFrame): A dataframe containing columns for latitude and longitude for the country in concern
        latitude (str): the column name for the latitude
        longitude (str): the column name for the longitude

    Returns:
        folium.Map: a basemap with the boundary, center and zooming set.
    """    
    lat_mean = data[latitude].mean() 
    long_mean = data[longitude].mean()


    lat_min = data[latitude].min()
    lat_max = data[latitude].max()
    long_min = data[longitude].min()
    long_max = data[longitude].max()

    m = folium.Map(
        location=[lat_mean, long_mean],
        zoom_start=6,
        min_zoom= 6,
        max_zoom= 18,
        control_scale=True,
        max_bounds=True,
        min_lat=lat_min - 2,
        max_lat=lat_max + 5,
        min_lon=long_min - 4,
        max_lon=long_max + 5
    )

    m.fit_bounds([[lat_min, long_min], [lat_max, long_max]])


    return m



def entropy_score(row):
    """calculate entropy_score of one row in the data_frame

    Args:
        row (panda_series): one row corresponding to one geographic area, with each value corresponding to one category of the variable in question
        
    Returns:
        float: the entropy score
    """
    entropy_score = 0
    for i in row:
        if i != 0:
            entropy_score =+ i*math.log(1/i) 
    return entropy_score

def calculate_proportion(data):
    """calculate the proportion of each category in the variable in concern

    Args:
        data (panda_datafroam): the whole dataframe with each row corresponding to each geographic area, and each column corresponding to the count of each category of the variable in concern

    Returns:
        data (panda_datafroam): the dataframe containing the proportion of each category. 
    """    
    #calculate the total observation in each geographic area
    Total = data.sum(axis = 1)
    return data.div(Total, axis=0)

def proportion_and_entropy_score_for_whole_dataset(data):
    """Return the entropy_score in the dataframe as well as the proportion of each category of the variable in concern

    Args:
        data (panda_datafroam): the whole dataframe with each row corresponding to each geographic area, and each column corresponding to the count of each category of the variable in concern. Non-relevant columns are not allowed

    Returns:
        data (panda_datafroam): the dataframe containing the proportion of each category and the entropy score in a new column named 'Entropy'
    """    
    data_proportion = calculate_proportion(data)
    data_proportion['Entropy'] = data_proportion.apply(entropy_score, axis = 1)
    return data_proportion