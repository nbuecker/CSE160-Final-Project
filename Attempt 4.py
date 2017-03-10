import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt

regions = ['Central Europe and the Baltics', 'East Asia & Pacific (excluding high income)', 'East Asia & Pacific', 'Europe & Central Asia (excluding high income)', 'Europe & Central Asia', 'Euro area', 'European Union', 'Latin America & Caribbean (excluding high income)', 'Latin America & Caribbean', 'Middle East & North Africa (excluding high income)', 'North America', 'South Asia', 'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa', 'East Asia & Pacific (IDA & IBRD countries)', 'Europe & Central Asia (IDA & IBRD countries)', 'Latin America & the Caribbean (IDA & IBRD countries)', 'Middle East & North Africa (IDA & IBRD countries)', 'South Asia (IDA & IBRD)', 'Sub-Saharan Africa (IDA & IBRD countries)', 'Arab World']
classes = ['Early-demographic dividend', 'Fragile and conflict affected situations', 'High income', 'Heavily indebted poor countries (HIPC)', 'Least developed countries: UN classification', 'Low income', 'Lower middle income', 'Low & middle income', 'Late-demographic dividend', 'Pre-demographic dividend', 'Post-demographic dividend', 'Upper middle income', 'IBRD only', 'IDA & IBRD total', 'IDA total', 'IDA blend', 'IDA only']
others = ['Not classified', 'OECD members', 'Other small states', 'Small states', 'World']

       
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
    
def econ_class_dummy_var_df(metadata_file):
    """Takes metadata file listing countries to their respective income group,
    designated as High Income (proxy for economic class level "Developed"), 
    Middle Income (combination of Upper Middle Income & Lower Middle Income in
    metadata; proxy for economic class level "Developing"), and Low Income
    (proxy for economic class level "Under-Developed"). Creates DataFrame with
    Country Name serving as the index column and containing two new columns
    representing the economic class level dummy variables (DV2 for developing
    countries and DV1 for underdeveloped countries). In these dummy variable
    columns, [0, 0] would represent a Developed country, [1, 0] would represent
    a Devloping country, and [0, 1] would represent an Under-Developed country.
    
    Params:
        metadata_file, a filepath to metadata
        
    Returns:
        a DataFrame mapping each country to its respective values for the dummy
        variable columns based on its income level economic classification
    """
    
    data = pd.read_csv(metadata_file, usecols=['TableName', 'IncomeGroup'])
    
    df = pd.DataFrame(data)
    df.astype(str)
    df.set_index('TableName', inplace=True)
    df.index.names = ['Country Name']
    
    df = df.dropna(0)    #drops rows with NaN values for IncomeGroup column
    df['Developing'] = 0
    df['Under-Developed'] = 0
    
    for country in df.index.values:
        if df.loc[country, 'IncomeGroup'] == 'Upper middle income':
            df.set_value(country, 'Developing', 1)
        elif df.loc[country, 'IncomeGroup'] == 'Lower middle income':
            df.set_value(country, 'Developing', 1)
        elif df.loc[country, 'IncomeGroup'] == 'Low income':  
            df.set_value(country, 'Under-Developed', 1)
    
    df = df.drop('IncomeGroup', 1)    
    
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


#def main():
#    
#    agro_input = create_df('Actual_Data/gdp_data/gdp_data.csv')
#    gdp_input = raw_input('Enter GDP Data:')
#        
#    print agro_input)
#    gdp_df = create_df(gdp_input)
#    #plot_df(agro_df, y_label='Agriculture', sliced=True, years=1990)
#
#    #plot_df(gdp_df, y_label='GDP', sliced=True, years=1990)
#    
#if __name__ == '__main__':
#    main()