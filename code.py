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

col1, col2 = st.columns(2)

with col1:
  fig = px.scatter(df, y='IMR', x="TFR").update_layout(title = 'Infant mortality rate vs. amount of babies per woman', xaxis_title = 'Total fertility (live births per woman)', yaxis_title = 'Infant mortality rate')
st.write(fig)
with col2:
  fig = px.histogram(infants, x="Country", y = 'infant mortality rate', title = 'Top 10 countries with highest infant mortality rate (2021)').update_layout(yaxis_title="Infant mortality rate")
st.write(fig)

# lijndiagram
fig = px.line(mortality_africa, x = 'Year', y = 'mortality rate', title = 'Child mortality in Africa over the years')
st.write(fig)

#boxplot
gapminder_2019 = gapminder[gapminder['year']==2007]

fig = px.box(gapminder_2019, y="lifeExp", x="continent")
st.write(fig)


