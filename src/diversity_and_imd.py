import pandas as pd
import os, sys
from utils import proportion_and_entropy_score_for_whole_dataset, restructure_data, set_up_altair_browser 
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
    df = df.reset_index()
    df.columns = ['area','entropy']
    return df

def get_imd():
    data = pd.read_csv(os.getcwd() + "/data/imd_2025.csv") 
    df = data.iloc[:,[0,1,2,4,6]]
    df.columns =['area','area_name','imd_ave_rank','imd_ave_score','imd_proportion_in_most_deprived']
    return df

def scatterplot(data):
    chart = alt.Chart(data).mark_point(filled=True).encode(
        alt.X('entropy:Q').axis(title='Diversity'),
        # alt.Y('imd_ave_score:Q'),
        # alt.Y('imd_ave_rank:Q'),
        alt.Y('imd_proportion_in_most_deprived:Q'),
        tooltip=alt.Tooltip(field='area_name', title=None),
      ).interactive()
    return chart

def main():
    set_up_altair_browser()
    entropy_df = entropy_data()
    imd_df = get_imd()
    data = pd.merge(entropy_df, imd_df)
    scatterplot(data).show()
    print(data.iloc[:,[1,3,4,5,]].corr(method='pearson'))
    print('finish')
main()
