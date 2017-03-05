import numpy as np
import pandas as pd
import csv
import os
import matplotlib as plt


# I removed these columns because they are not country-specific and so we don't
# want them for our general analysis, but they might be useful for later so
# I separated them into regions, classes, and other indicators that aren't
# specific country names. The only non-country name I left in the dataframe
# was 'World' because I felt like it could prove to be useful for visualizations.


regions = ['Central Europe and the Baltics', 'East Asia & Pacific (excluding high income)', 'East Asia & Pacific', 'Europe & Central Asia (excluding high income)', 'Europe & Central Asia', 'Euro area', 'European Union', 'Latin America & Caribbean (excluding high income)', 'Latin America & Caribbean', 'Middle East & North Africa (excluding high income)', 'North America', 'South Asia', 'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa', 'East Asia & Pacific (IDA & IBRD countries)', 'Europe & Central Asia (IDA & IBRD countries)', 'Latin America & the Caribbean (IDA & IBRD countries)', 'Middle East & North Africa (IDA & IBRD countries)', 'South Asia (IDA & IBRD)', 'Sub-Saharan Africa (IDA & IBRD countries)']
classes = ['Early-demographic dividend', 'Fragile and conflict affected situations', 'High income', 'Heavily indebted poor countries (HIPC)', 'Least developed countries: UN classification', 'Low income', 'Lower middle income', 'Low & middle income', 'Late-demographic dividend', 'Pre-demographic dividend', 'Post-demographic dividend', 'Upper middle income', 'IBRD only', 'IDA & IBRD total', 'IDA total', 'IDA blend', 'IDA only']
others = ['Not classified', 'OECD members', 'Other small states', 'Small states']

       
def read_CSV(filename):
    """Reads in a CSV file called filename and returns a pandas-formatted
    dataframe with the 'Country Name' column as the index (x-values) and
    each column of years 1990-2014 mapping to its respective float for that 
    country.
    
    Params: 
        filename, a CSV file         
    
    Returns: df, a pandas dataframe
    
    """
    
    data = pd.read_csv('Actual_Data/agro_land/agro_data2.csv', index_col="Country Name")

    year_cols = []
    for year in range(1990, 2015):
        string_year = str(year)
        year_cols.append(string_year)
        
    df = pd.DataFrame(data, columns = year_cols, dtype='float')
    
    df = df.drop(regions) 
    df = df.drop(classes)
    df = df.drop(others)
    
    return df
    



