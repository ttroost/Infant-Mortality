# import packages
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import plotly.express as px
import plotly as plt
import seaborn as sns
import openpyxl


# import dataset 
data = pd.read_csv('Life_Expectancy_Data (1).csv')
countrie = gpd.read_file('countries.geojson')
mortality = pd.read_excel('mortality.xlsx')
df = pd.read_csv('WPP2019_Period_Indicators_Medium.csv')
infants = pd.read_excel('infants2.xlsx')
mortality_africa = pd.read_excel('mortality rate africa.xlsx')
data_url = 'http://bit.ly/2cLzoxH'
gapminder = pd.read_csv(data_url)

# rename admin to country so we can merge
countrie.rename(columns = {'ADMIN':'Country'}, inplace = True)
countrie.head()

# rename country name to country for merge
mortality.rename(columns = {'Country Name':'Country'}, inplace = True)
mortality.head()

# merge
merged_mortality = countrie.merge(mortality, on = 'Country')
merged_mortality.head()

# drop columns df
df2 = df.drop(['LocID', 'Location','VarID','Variant','Time', 'MidPeriod', 'Births','LExMale','LExFemale','CDR','Deaths','DeathsMale','DeathsFemale','CNMR','NetMigrations','NatIncr','SRB'], axis = 1)
df2.head()


# scatterplot
fig = px.scatter(df, y='IMR', x="TFR")
fig.update_layout(title = 'Infant mortality rate vs. amount of babies per woman', xaxis_title = 'Total fertility (live births per woman)', yaxis_title = 'Infant mortality rate')
fig.show()

# histogram
fig = px.histogram(infants, x="Country", y = 'infant mortality rate')
fig.update_layout(title = 'Top 10 countries with highest infant mortality rate (2021)', xaxis_title = 'Countries', yaxis_title = 'Infant mortality rate')
fig.show()

# lijndiagram
fig = px.line(mortality_africa, x = 'Year', y = 'mortality rate', title = 'Child mortality in Africa over the years')
fig.show()

#boxplot
gapminder_2019 = gapminder[gapminder['year']==2007]
gapminder_2019.shape

bplot = sns.boxplot(y='lifeExp', x='continent', 
                 data=gapminder_2019, 
                 width=0.5,
                 palette="colorblind")
bplot.set_title('Life expectancy per continent in 2019')

# matrix
matrix_df = pps.matrix(df2)[['x', 'y', 'ppscore']].pivot(columns='x', index='y', values='ppscore')
sns.heatmap(matrix_df, vmin=0, vmax=1, cmap="Blues", linewidths=0.5, annot=True)


