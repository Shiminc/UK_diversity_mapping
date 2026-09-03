import pandas as pd
import os, sys
from utils import proportion_and_entropy_score_for_whole_dataset, restructure_data 
import geopandas as gpd
import altair as alt
import numpy as np

# read the data on country of birth and calculate the entropy/diversity
def entropy_data():

    data = pd.read_csv(os.getcwd() + "/data/country_of_birth_processed.csv") 
    data = data.replace(r"^ +| +$", r"", regex=True)

    data_cleaned = restructure_data(data, 'Analysis_region', 'Lower tier local authorities Code')
    data_entropy = proportion_and_entropy_score_for_whole_dataset(data_cleaned)
    df = data_entropy[['Entropy']]
    return df.reset_index()

def get_imd():
    data = pd.read_csv(os.getcwd() + "/data/imd_2025.csv") 
    
    return data

def main():
    entropy_df = entropy_data()
    imd_df = get_imd()
    print('finish')

main()
