import numpy as np
import pandas as pd
import csv
import os
import matplotlib as plt
#import statsmodels.formula.api as sm

################################################################################
#Part 0: Import the Data
################################################################################


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
  
################################################################################
#Part 1: Format and Create DataFrames
################################################################################

def pivot_data_frame_row_to_df_column(year, column_names, source_list):
    """Selects a row from each of the source data frames and augments a new 
        dataframe with those rows as its columns.
    
    Parameters: year (the row of the source dataframe); column_names (a list of 
    names that will correspond to the name of the pivoted row in the target 
    dataframe; source_list (a list of the data frames from which you select the 
    rows).
    
    Returns: Returns and augmented data frame
    
    Cautions: If the source_list and column_names lists are not the same 
    length it will print an error and return 0. The column names and source 
    dataframes MUST BE COMPATIBALY INDEXED, otherwise the data will be assigned
    an improper name."""
    
    if len(column_names) != len(source_list):
        print "Column names and source dataframes lists are of incompatible"+ \
                "length."   
    else:
        target_df = pd.DataFrame() 
        for index in range(len(source_list)):
            target_df[column_names[index]] = source_list[index].loc[year]
    return target_df


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


def finalize_data_frames(dataframes, dummy_df):
    """Add dummy variable columns to any DataFrame in dataframes and removes 
        countries for which there is not complete data.
        
        Parameters: dataframes (a list of DataFrames that will be finalized)
                    dummy_df (a DataFrame comprised of appropriately indexed 
                        countries based on their GDP/N bracket
        Returns: None. It merely adds D.V. columns to pre-exosting DataFrames
        Cautions: If no DataFrames are passed in, the function will reuturn None
                    and print an error message."""
    
    for dataframe in dataframes:
        dataframe["Devlpng"] = dummy_df["Developing"]
        dataframe["Underdev"] = dummy_df["Under-Developed"]
     
            
    
  
################################################################################
#Part 1: Show how land use has changed#
################################################################################

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
    
################################################################################
#Part X: Main Function
################################################################################

def main():
    
    #input files to be used
    agro_input = raw_input("Enter Agriculture File:")
    forest_input = raw_input("Enter Forestlands File:")
    gdp_input = raw_input("Enter GDP per Capita File:")
    meta_input = raw_input("Enter Metadata File:") 
    
    # create DataFrames
    agro_df = create_df(agro_input)
    forest_df = create_df(forest_input)
    gdp_df = create_df(gdp_input)
    other_df = 100 - agro_df - forest_df
    
    #create Dummy Variable DataFrame
    dv_df = econ_class_dummy_var_df(meta_input)
    
    #create master DataFrames
    country_attributes = ["% Agro", "% Forest", "% Other", "GDP_N"]
    source_dfs = [agro_df, forest_df, other_df, gdp_df ]
    
    master_90 = pivot_data_frame_row_to_df_column(1990, country_attributes, source_dfs)
    master_02 = pivot_data_frame_row_to_df_column(2002, country_attributes, source_dfs)
    master_14 = pivot_data_frame_row_to_df_column(2014, country_attributes, source_dfs)
    
    #add D.V. columns
    data_f_list = [master_90, master_02, master_14]
    finalize_data_frames(data_f_list, dv_df) 
    
    print master_14.describe()
    master_14.plot.scatter(x = '% Agro', y = 'GDP_N')
    plt.show()
 
    
    #plot magnitueds of differnce in land use
    #plot_df(agro_df, y_label='Agriculture', sliced=True, years=1990)
    #plot_df(forest_df, y_label='Forest', sliced=True, years=1990)
    #plot_df(other_df, y_label='Other', sliced=True, years=1990)
    
    
            
if __name__ == "__main__":
    main()

########################################################################################################
"""NICOLE'S CODE BEGINS HERE"""
################################################################################
import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

################################################################################
#Part 0: Import the Data
################################################################################


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
  
################################################################################
#Part 1: Format and Create DataFrames
################################################################################

def pivot_data_frame_row_to_df_column(year, column_names, source_list):
    """Selects a row from each of the source data frames and augments a new 
        dataframe with those rows as its columns.
    
    Parameters: year (the row of the source dataframe); column_names (a list of 
    names that will correspond to the name of the pivoted row in the target 
    dataframe; source_list (a list of the data frames from which you select the 
    rows).
    
    Returns: Returns and augmented data frame
    
    Cautions: If the source_list and column_names lists are not the same 
    length it will print an error and return 0. The column names and source 
    dataframes MUST BE COMPATIBALY INDEXED, otherwise the data will be assigned
    an improper name."""
    
    if len(column_names) != len(source_list):
        print "Column names and source dataframes lists are of incompatible"+ \
                "length."   
    else:
        target_df = pd.DataFrame() 
        for index in range(len(source_list)):
            target_df[column_names[index]] = source_list[index].loc[year]
    return target_df


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


def finalize_data_frames(dataframes, dummy_df):
    """Add dummy variable columns to any DataFrame in dataframes and removes 
        countries for which there is not complete data.
        
        Parameters: dataframes (a list of DataFrames that will be finalized)
                    dummy_df (a DataFrame comprised of appropriately indexed 
                        countries based on their GDP/N bracket
        Returns: None. It merely adds D.V. columns to pre-exosting DataFrames
        Cautions: If no DataFrames are passed in, the function will reuturn None
                    and print an error message."""
    
    for dataframe in dataframes:
        dataframe["Devlpng"] = dummy_df["Developing"]
        dataframe["Underdev"] = dummy_df["Under-Developed"] 
        dataframe = dataframe.dropna(0, how= 'any', subset = ["Agro", \
        "Forest", "GDP_N", "Underdev", "Devlpng"], inplace = True)          

  
################################################################################
#Part 2: Show how land use has changed#
################################################################################

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

################################################################################
# Part 3: Run Regressions and Compute Test Statistics
################################################################################    

     
                
################################################################################
#Part X: Main Function
################################################################################

def main():
    """DOC STRING"""
    
    #input files to be used
    agro_input = "data/agro_data/agro_csv.csv"
    #raw_input("Enter Agriculture File:")
    forest_input = "data/forest_data/forest_csv.csv"
    # raw_input("Enter Forestlands File:")
    gdp_input = "data/gdp_data/gdp_csv.csv"
    #raw_input("Enter GDP per Capita File:")
    meta_input = "data/agro_data/metadata.csv"
    #raw_input("Enter Metadata File:") 
    
    # create DataFrames
    agro_df = create_df(agro_input)
    agro_df = agro_df.drop("World", 1)
    
    forest_df = create_df(forest_input)
    forest_df = forest_df.drop("World", 1)
    
    gdp_df = create_df(gdp_input)
    gdp_df = gdp_df.drop("World", 1)
    
    
    #create Dummy Variable DataFrame
    dv_df = econ_class_dummy_var_df(meta_input)
    
    #create master DataFrames
    country_attributes = ["Agro", "Forest", "GDP_N"]
    source_dfs = [agro_df, forest_df, gdp_df ]
    
    master_90 = pivot_data_frame_row_to_df_column(1990, country_attributes, source_dfs)
    master_02 = pivot_data_frame_row_to_df_column(2002, country_attributes, source_dfs)
    master_14 = pivot_data_frame_row_to_df_column(2014, country_attributes, source_dfs)
    
    #add D.V. columns
    data_f_list = [master_90, master_02, master_14]
    finalize_data_frames(data_f_list, dv_df)
  
    # run un-restricted (main) regressions
    master_90_reg = smf.ols(formula = "GDP_N ~ Agro + Agro*Devlpng + Agro*Underdev + Forest + Forest*Devlpng + Forest*Underdev", data = master_90).fit()
    retsrict_f_reg = smf.ols(formula = "GDP_N ~ Agro + Agro*Devlpng + Agro*Underdev", data = master_90).fit()
    restrict_a_reg = smf.ols(formula = "GDP_N ~ Forest + Forest*Devlpng + Forest*Underdev", data = master_90).fit()
    
    
    #master_02_reg = smf.ols(formula="GDP_N ~ Agro + + Agro*Devlpng + Agro*Underdev + Forest + Forest*Devlpng + Forest*Underdev", data = master_02).fit()
    #master_14_reg = smf.ols(formula="GDP_N ~ Agro + + Agro*Devlpng + Agro*Underdev + Forest + Forest*Devlpng + Forest*Underdev", data = master_14).fit()
    
    summary_table = master_90_reg.summary()
    print master_90_reg.rsquared

    # run restricted regressions
    
    # compute F-statistic
    
    # report results to user

    
 
    
    
    
            
if __name__ == "__main__":
    main()


######################################################################
import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

################################################################################
#Part 0: Import the Data
################################################################################


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
  
################################################################################
#Part 1: Format and Create DataFrames
################################################################################

def pivot_data_frame_row_to_df_column(year, column_names, source_list):
    """Selects a row from each of the source data frames and augments a new 
        dataframe with those rows as its columns.
    
    Parameters: year (the row of the source dataframe); column_names (a list of 
    names that will correspond to the name of the pivoted row in the target 
    dataframe; source_list (a list of the data frames from which you select the 
    rows).
    
    Returns: Returns and augmented data frame
    
    Cautions: If the source_list and column_names lists are not the same 
    length it will print an error and return 0. The column names and source 
    dataframes MUST BE COMPATIBALY INDEXED, otherwise the data will be assigned
    an improper name."""
    
    if len(column_names) != len(source_list):
        print "Column names and source dataframes lists are of incompatible"+ \
                "length."   
    else:
        target_df = pd.DataFrame() 
        for index in range(len(source_list)):
            target_df[column_names[index]] = source_list[index].loc[year]
    return target_df


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


def finalize_data_frames(dataframes, dummy_df):
    """Add dummy variable columns to any DataFrame in dataframes and removes 
        countries for which there is not complete data.
        
        Parameters: dataframes (a list of DataFrames that will be finalized)
                    dummy_df (a DataFrame comprised of appropriately indexed 
                        countries based on their GDP/N bracket
        Returns: None. It merely adds D.V. columns to pre-exosting DataFrames
        Cautions: If no DataFrames are passed in, the function will reuturn None
                    and print an error message."""
    
    for dataframe in dataframes:
        dataframe["Devlpng"] = dummy_df["Developing"]
        dataframe["Underdev"] = dummy_df["Under-Developed"] 
        dataframe = dataframe.dropna(0, how= 'any', subset = ["Agro", \
        "Forest", "GDP_N", "Underdev", "Devlpng"], inplace = True)          

  
################################################################################
#Part 2: Show how land use has changed#
################################################################################

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

################################################################################
# Part 3: Run Regressions and Compute Test Statistics
################################################################################    

def run_reg(complete_list, dependent, data):
    """Computes a regression.
        Parameters: complete_list: (a string of covariates for the regression - 
                        formatting specified below)
                    dependent: (the dependent variable formatted as a string)
                    data: (the DataFrame to be used for the regression) 
        String formatting: The complete_list and restricted_list should be 
                        formatted EXACTLY this way:
                            "Var1 + Var2 + Var3" etc. 
        Returns: Returns an OLS formatted unrestricted regressions.
        """
    unrestricted_input = dependent + "~" + complete_list                   
    regression = smf.ols(unrestricted_input, data)
    return regression


def compute_f_stat(regression, dataframe):
    """Computes the F-statistic of a regression.
    Parameters: regression (a statsmodels formatted OLS object regression)
                dataframe (the DataFrame your regression was computed from)
    Returns: A tuple of three F-stats
    Cautions: the reg_tuple must be in the EXACT order of restricted then 
                unrestricted. Otherwise the code will calculate it wrong and no
                error message will be printed."""
    
    reg_results = regression.fit()
    # locate coefficients 
    ag_coeff = reg_results.params["Agro"]
    ag_under_coeff = reg_results.params["Agro:Underdev"]
    ag_devlpng_coeff = reg_results.params["Agro:Devlpng"]
    # locate S.E.s
    ag_se = reg_results.bse["Agro"]
    ag_under_se = reg_results.bse["Agro:Underdev"]
    ag_devlpng_se = reg_results.bse["Agro:Devlpng"]
    # compute covariances
    ag_under_cv = reg_results.normalized_cov_params.loc["Agro", "Agro:Underdev"]
    devlpng_under_cv = reg_results.normalized_cov_params.loc["Agro:Devlpng", "Agro:Underdev"]
    ag_devlpng_cv = reg_results.normalized_cov_params.loc["Agro", "Agro:Devlpng"]
    # compute F-stats
    agunder_f_stat = ((ag_under_coeff - ag_coeff) / sqrt(ag_se**2 + ag_under_se**2 - 2*(ag_under_cv)))**2
    dev_under_f_stat = ((ag_under_coeff - ag_devlpng_coeff) / sqrt(ag_under_se**2 + ag_devlpng_se**2 - 2*(devlpng_under_cv)))**2
    agdev_f_stat = ((ag_devlpng_coeff - ag_coeff) / sqrt(ag_se**2 + ag_devlpng_se**2 - 2*(ag_devlpng_cv)))**2
    
    return (float(agunder_f_stat), float(dev_under_f_stat), float(agdev_f_stat)) 
    
    

################################################################################
#Part X: Main Function
################################################################################

def main():
    """DOC STRING"""
    
    #input files to be used
    agro_input = "data/agro_data/agro_csv.csv"
    #raw_input("Enter Agriculture File:")
    forest_input = "data/forest_data/forest_csv.csv"
    # raw_input("Enter Forestlands File:")
    gdp_input = "data/gdp_data/gdp_csv.csv"
    #raw_input("Enter GDP per Capita File:")
    meta_input = "data/agro_data/metadata.csv"
    #raw_input("Enter Metadata File:") 
    
    # create DataFrames
    agro_df = create_df(agro_input)
    agro_df = agro_df.drop("World", 1)
    
    forest_df = create_df(forest_input)
    forest_df = forest_df.drop("World", 1)
    
    gdp_df = create_df(gdp_input)
    gdp_df = gdp_df.drop("World", 1)
    
    
    #create Dummy Variable DataFrame
    dv_df = econ_class_dummy_var_df(meta_input)
    
    # create master DataFrames
    country_attributes = ["Agro", "Forest", "GDP_N"]
    source_dfs = [agro_df, forest_df, gdp_df ]
    
    master_90 = pivot_data_frame_row_to_df_column(1990, country_attributes, source_dfs)
    master_02 = pivot_data_frame_row_to_df_column(2002, country_attributes, source_dfs)
    master_14 = pivot_data_frame_row_to_df_column(2014, country_attributes, source_dfs)
    
    # add D.V. columns
    data_f_list = [master_90, master_02, master_14]
    finalize_data_frames(data_f_list, dv_df)
  
    # run regressions
    full_reg_90 = run_reg("Agro + Agro*Devlpng + Agro*Underdev + Forest + Forest*Devlpng + Forest*Underdev","GDP_N", master_90)
    
    
    
    ####tests here
    full_90_stats = full_reg_90.fit()
    #print full_90_stats.summary()
    #print full_90_stats.params['Agro']
    #print full_90_stats.bse
    print master_90.cov
    print dir(full_90_stats)
    
    print full_90_stats.normalized_cov_params
    
    # compute F-statistic
    print compute_f_stat(full_reg_90, master_90)
    
    
    #f_stat_forest = compute_f_stat(forest_reg_tuple, 149, 6, 3)
    #f_stat_agro = compute_f_stat(agro_reg_tuple, 149, 6, 3)

    
    # report results to user


    
 
    
    
    
            
if __name__ == "__main__":
    main()



