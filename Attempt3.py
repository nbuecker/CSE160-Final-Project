import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt

regions = ['Central Europe and the Baltics', 'East Asia & Pacific (excluding high income)', 'East Asia & Pacific', 'Europe & Central Asia (excluding high income)', 'Europe & Central Asia', 'Euro area', 'European Union', 'Latin America & Caribbean (excluding high income)', 'Latin America & Caribbean', 'Middle East & North Africa (excluding high income)', 'North America', 'South Asia', 'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa', 'East Asia & Pacific (IDA & IBRD countries)', 'Europe & Central Asia (IDA & IBRD countries)', 'Latin America & the Caribbean (IDA & IBRD countries)', 'Middle East & North Africa (IDA & IBRD countries)', 'South Asia (IDA & IBRD)', 'Sub-Saharan Africa (IDA & IBRD countries)', 'Arab World']
classes = ['Early-demographic dividend', 'Fragile and conflict affected situations', 'High income', 'Heavily indebted poor countries (HIPC)', 'Least developed countries: UN classification', 'Low income', 'Lower middle income', 'Low & middle income', 'Late-demographic dividend', 'Pre-demographic dividend', 'Post-demographic dividend', 'Upper middle income', 'IBRD only', 'IDA & IBRD total', 'IDA total', 'IDA blend', 'IDA only']
others = ['Not classified', 'OECD members', 'Other small states', 'Small states']

       
def create_df(filename):
    """Reads in CSV file and returns a pandas DataFrame with years as the index
    column and country names as the rest of the columns, and the land percentage
    for country as the value (type: numpy array) for each index/column pair.
    
    Params:
        filename, a CSV filepath
    Returns:
        df, a pandas DataFrame
    """
    year_cols = []
    for year in range(1990, 2015):
        string_year = str(year)
        year_cols.append(string_year)
    
    cols = list(year_cols)
    cols.append('Country Name')
    data = pd.read_csv(filename, skiprows=4, usecols=cols)
    df = pd.DataFrame(data)
    df.set_index('Country Name', inplace=True)
    
    df.dropna(how='any')
    
    df = df.drop(regions) 
    df = df.drop(classes)
    df = df.drop(others)
    df = df.T
    df.columns.names = ['Country Name']

    years = []
    for year in df.index:
        years.append(int(year))            
    
    df['Years'] = years

    df = df.set_index('Years')

    
    return df
    


def plot_df(df, y_label='', sliced=False, years=None, country=None):
    """Takes a DataFrame and plots each Country Name against each year, if
    nothing is passed for sliced and years. If sliced=True and years is given
    an integer value, then only the years given will be plotted for each Country
    Name.
    
    Params:
        df, a pandas DataFrame
        y_label, a string to give the y-axis a label
        slice, a boolean, when True expects argument passed in for years & country
        years, a list of years passed in to be plotted
        country, a string 
    
    Returns:
        a plot of Country Names against years with the respective percentages
        of land designation for the given CSV data file
    """

    df_year = df.loc[years]
    
    labels = list(df_year.index)
            
    ax = df_year.plot(kind='area', fontsize=10)
    ax.set_xlabel("Country Name", fontsize=10)
    ylabel = "% Land Area Designated for " + y_label
    ax.set_ylabel(str(ylabel), fontsize=10)
    ax.set_xticklabels(labels)
    df_year.plot(kind='area', rot='vertical', legend=False, ax=ax) #or: xticks=df_year[labels],
    
    plt.tight_layout()
    plt.show()


def main():
    
    agro_df = create_df('Actual_Data/agro_land/agro_data.csv')
    forest_df = create_df('Actual_Data/forest_land/forest_data.csv')
    total_df = create_df('Actual_Data/land_areas/land_area_data.csv')
    agro_for_df = agro_df.add(forest_df)
    other_df = abs(total_df - agro_for_df)
        
    #plot_df(agro_df, y_label='Agriculture', sliced=True, years=1990)
    #plot_df(forest_df, y_label='Forest', sliced=True, years=1990)
    #plot_df(other_df, y_label='Other', sliced=True, years=1990)
    
if __name__ == '__main__':
    main()
    