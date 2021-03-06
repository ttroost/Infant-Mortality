# import packages
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import plotly.express as px
import plotly as plt
import openpyxl
from streamlit_folium import folium_static
from statsmodels.formula.api import ols
import ppscore as pps
import seaborn as sns
import plotly.graph_objects as go


# import dataset 
data = pd.read_csv('Life_Expectancy_Data (1).csv')
countrie = gpd.read_file('countries.geojson')
mortality = pd.read_excel('mortality.xlsx')
df = pd.read_csv('WPP2019_Period_Indicators_Medium.csv')
infants = pd.read_excel('infants2.xlsx')
mortality_africa = pd.read_excel('mortality rate africa.xlsx')
data_url = 'http://bit.ly/2cLzoxH'
gapminder = pd.read_csv(data_url)
household = pd.read_excel('household.xlsx')



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
df2 = df.drop(['LocID', 'Location','VarID','Variant','Time', 'MidPeriod', 'Births','LExMale','LExFemale','CDR','Deaths','DeathsMale','DeathsFemale','CNMR','NetMigrations','NatIncr','SRB', 'GrowthRate', 'MAC', 'NRR', 'Q5'], axis = 1)


# interactive onderdelen
with st.sidebar:
  sidebar_keuze= st.radio('Chapters:', ['Infant mortality analysis','Sources'])

if sidebar_keuze == 'Infant mortality analysis':
  st.markdown('***')
  st.markdown("<h3 style='text-align: center; color: black;'>Infant mortality analysis</h3>", unsafe_allow_html=True)
  st.markdown('***')
  
  gapminder_2019 = gapminder[gapminder['year']==2007]
  fig = px.box(gapminder_2019, y="lifeExp", x="continent").update_layout(title = 'Life expectancy per continent', xaxis_title = 'Continents', yaxis_title = 'Life expectancy')
  st.write(fig)
     

      
  kaart_opties = st.selectbox('Choose a year:', ['1985','2019'])
  style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000', 'fillOpacity': 0.1, 'weight': 0.1}
  highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity': 0.50, 'weight': 0.1}
  if kaart_opties == '1985':
    a = folium.Map(zoom_start= 10,tiles='cartodbpositron')
    folium.Choropleth(geo_data= merged_mortality,
                      name= 'geometry',
                      data= merged_mortality,
                      columns=['Country', '1985'],
                      key_on='feature.properties.Country',
                      fill_color= 'PuBuGn',
                      fill_opacity= 0.5,
                      line_opacity= 0.8,
                      legend_name= 'Infant mortality rate per country per 1000 live births').add_to(a)
    folium_static(a)
  if kaart_opties == '2019':
    b = folium.Map(zoom_start= 7,tiles='cartodbpositron')
    folium.Choropleth(geo_data= merged_mortality,
                      name= 'geometry',
                      data= merged_mortality,
                      columns=['Country', '2019'],
                      key_on='feature.properties.Country',
                      fill_color= 'PuBuGn',
                      fill_opacity= 0.5,
                      line_opacity= 0.8,
                      legend_name= 'Infant mortality rate per country per 1000 live births').add_to(b)
    folium_static(b)
    
  col1, col2 = st.columns(2)
  
  with col1:
    fig = px.line(mortality_africa, x = 'Year', y = 'mortality rate', title = 'Infant mortality in Africa over the years').update_layout(yaxis_title = 'Infant mortality rate')
    st.write(fig)
  with col2:
    fig = px.histogram(infants, x="Country", y = 'infant mortality rate', title = 'Top 10 countries with highest infant mortality rate').update_layout(yaxis_title="Infant mortality rate")
    st.write(fig)

  col1, col2 = st.columns(2)
  
  with col1:
    fig = px.scatter(df, y='IMR', x="TFR", trendline = 'ols', trendline_color_override = 'red').update_layout(title = 'Infant mortality rate vs. amount of babies per woman', xaxis_title = 'Total fertility (live births per woman)', yaxis_title = 'Infant mortality rate')
    fig3 = px.scatter(df, y='IMR', x="TFR").update_layout(title = 'Infant mortality rate vs. amount of babies per woman', xaxis_title = 'Total fertility (births per woman)', yaxis_title = 'Infant mortality rate')
    if st.checkbox('Show trendline'):
      st.write(fig)
    else:
      st.write(fig3)
  with col2:
    fig = px.histogram(household, x="Region", y = 'Household size').update_layout(title = 'Household size per region', xaxis_title = 'Regions', yaxis_title = 'Household size')
    st.write(fig)
    
  col1, col2 = st.columns(2)
  
  with col1:
    st.image("matrix.png")
  with col2:
    st.write('''
    TFR = Total fertility (live births per woman)
    
    CBR = Crude birth rate (per 1000 population)
    
    LEx = Life expectancy at birth for both sexes combined (years)
    
    IMR = Infant mortality rate (infant deaths per 1000 live births)''')
    
    
  
 

elif sidebar_keuze == 'Sources':
  st.markdown('***')
  st.markdown("<h3 style='text-align: center; color: black;'>Sources</h3>", unsafe_allow_html=True)
  st.markdown('***')
  
  st.write('''
           https://www.kaggle.com/kumarajarshi/life-expectancy-who
           
           https://data.worldbank.org/indicator/SP.DYN.IMRT.IN
           
           https://datahub.io/core/geo-countries
           
           https://population.un.org/wpp2019/Download/Standard/CSV/
           
           https://www.statista.com/statistics/264714/countries-with-the-highest-infant-mortality-rate/
           
           https://www.statista.com/statistics/1072803/child-mortality-rate-africa-historical/
           
           https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/master/data/gapminder-FiveYearData.csv
           
           https://www.pewforum.org/2019/12/12/religion-and-living-arrangements-around-the-world/''')
           
