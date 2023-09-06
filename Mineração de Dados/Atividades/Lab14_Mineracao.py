#!/usr/bin/env python
# coding: utf-8

# Pontifícia Universidade Católica de São Paulo 
# 
# `Ciência de Dados e Inteligência Artificial`
# 
# ## Laboratório 14 - DBSCAN
# 
# 
# ---
# > 👨‍🏫*Professor Dr. Rooney Coelho (rracoelho@pucsp.br)*
# ---

# A maioria das técnicas tradicionais de agrupamento, como k-means, agrupamento hierárquico e agrupamento difuso, podem ser usadas para agrupar dados sem supervisão.
# 
# No entanto, quando aplicadas a tarefas com clusters de formato arbitrário, ou clusters dentro de cluster, as técnicas tradicionais podem não conseguir bons resultados. Ou seja, os elementos no mesmo cluster podem não compartilhar similaridade suficiente ou o desempenho pode ser ruim.
# Além disso, o agrupamento baseado em densidade localiza regiões de alta densidade que são separadas umas das outras por regiões de baixa densidade. Densidade, neste contexto, é definida como o número de pontos dentro de um raio especificado.
# 
# 
# 
# ### Modelagem
# DBSCAN significa Density-Based Spatial Clustering of Applications with Noise (Agrupamento Espacial Baseado em Densidade de Aplicativos com Ruído). Esta técnica é um dos algoritmos de agrupamento mais comuns que funciona com base na densidade do objeto.
# A ideia é que, se um determinado ponto pertence a um cluster, ele deve estar próximo a muitos outros pontos desse cluster.
# 
# Funciona com base em dois parâmetros: Epsilon e Pontos Mínimos
# __Epsilon__ determina um raio especificado que, se incluir um número suficiente de pontos, chamamos de área densa
# __minimumSamples__ determinam o número mínimo de pontos de dados que queremos em uma vizinhança para definir um cluster.

# In[2]:


import numpy as np 
import pandas as pd

from sklearn.cluster import DBSCAN 
from sklearn.preprocessing import StandardScaler 
import matplotlib.pyplot as plt 

from mpl_toolkits.basemap import Basemap


# ## Agrupamento de estações meteorológicas usando DBSCAN e scikit-learn
# 
# DBSCAN é especialmente muito bom para tarefas como identificação de classes em um contexto espacial. O atributo maravilhoso do algoritmo DBSCAN é que ele pode descobrir qualquer cluster de forma arbitrária sem ser afetado pelo ruído. Por exemplo, este exemplo a seguir agrupa a localização das estações meteorológicas no Canadá.
# 
# O DBSCAN pode ser usado aqui, por exemplo, para encontrar o grupo de estações que apresentam a mesma condição meteorológica. Como você pode ver, ele não apenas encontra diferentes clusters de formas arbitrárias, mas também pode encontrar a parte mais densa de amostras centradas em dados, ignorando áreas ou ruídos menos densos.
# 
# vamos começar a brincar com os dados. Estaremos trabalhando de acordo com o seguinte fluxo de trabalho: 
# 
# 1. Carregando dados
# 2. Dados de visão geral
# 3. Limpeza de dados
# 4. Seleção de dados
# 5. Agrupamento

# ### Sobre o conjunto de dados
# 
# 		
# <h4 align = "center">
# Meio Ambiente Canadá
# Valores Mensais de Julho - 2015
# </h4>
# <html>
# <head>
# <style>
# table {
#     font-family: arial, sans-serif;
#     border-collapse: collapse;
#     width: 100%;
# }
# 
# td, th {
#     border: 1px solid #dddddd;
#     text-align: left;
#     padding: 8px;
# }
# 
# tr:nth-child(even) {
#     background-color: #dddddd;
# }
# </style>
# </head>
# <body>
# 
# <table>
#   <tr>
#     <th>Nome na tabela</th>
#      <th>Significado</th>
#   </tr>
#   <tr>
#     <td><font color = "green"><strong>Stn_Name</font></td>
#     <td><font color = "green"><strong>Station Name</font</td>
#   </tr>
#   <tr>
#     <td><font color = "green"><strong>Lat</font></td>
#     <td><font color = "green"><strong>Latitude (North+, degrees)</font></td>
#   </tr>
#   <tr>
#     <td><font color = "green"><strong>Long</font></td>
#     <td><font color = "green"><strong>Longitude (West - , degrees)</font></td>
#   </tr>
#   <tr>
#     <td>Prov</td>
#     <td>Province</td>
#   </tr>
#   <tr>
#     <td>Tm</td>
#     <td>Mean Temperature (°C)</td>
#   </tr>
#   <tr>
#     <td>DwTm</td>
#     <td>Days without Valid Mean Temperature</td>
#   </tr>
#   <tr>
#     <td>D</td>
#     <td>Mean Temperature difference from Normal (1981-2010) (°C)</td>
#   </tr>
#   <tr>
#     <td><font color = "blue">Tx</font></td>
#     <td><font color = "blue">Highest Monthly Maximum Temperature (°C)</font></td>
#   </tr>
#   <tr>
#     <td>DwTx</td>
#     <td>Days without Valid Maximum Temperature</td>
#   </tr>
#   <tr>
#     <td><font color = "blue">Tn</font></td>
#     <td><font color = "blue">Lowest Monthly Minimum Temperature (°C)</font></td>
#   </tr>
#   <tr>
#     <td>DwTn</td>
#     <td>Days without Valid Minimum Temperature</td>
#   </tr>
#   <tr>
#     <td>S</td>
#     <td>Snowfall (cm)</td>
#   </tr>
#   <tr>
#     <td>DwS</td>
#     <td>Days without Valid Snowfall</td>
#   </tr>
#   <tr>
#     <td>S%N</td>
#     <td>Percent of Normal (1981-2010) Snowfall</td>
#   </tr>
#   <tr>
#     <td><font color = "green"><strong>P</font></td>
#     <td><font color = "green"><strong>Total Precipitation (mm)</font></td>
#   </tr>
#   <tr>
#     <td>DwP</td>
#     <td>Days without Valid Precipitation</td>
#   </tr>
#   <tr>
#     <td>P%N</td>
#     <td>Percent of Normal (1981-2010) Precipitation</td>
#   </tr>
#   <tr>
#     <td>S_G</td>
#     <td>Snow on the ground at the end of the month (cm)</td>
#   </tr>
#   <tr>
#     <td>Pd</td>
#     <td>Number of days with Precipitation 1.0 mm or more</td>
#   </tr>
#   <tr>
#     <td>BS</td>
#     <td>Bright Sunshine (hours)</td>
#   </tr>
#   <tr>
#     <td>DwBS</td>
#     <td>Days without Valid Bright Sunshine</td>
#   </tr>
#   <tr>
#     <td>BS%</td>
#     <td>Percent of Normal (1981-2010) Bright Sunshine</td>
#   </tr>
#   <tr>
#     <td>HDD</td>
#     <td>Degree Days below 18 °C</td>
#   </tr>
#   <tr>
#     <td>CDD</td>
#     <td>Degree Days above 18 °C</td>
#   </tr>
#   <tr>
#     <td>Stn_No</td>
#     <td>Climate station identifier (first 3 digits indicate   drainage basin, last 4 characters are for sorting alphabetically).</td>
#   </tr>
#   <tr>
#     <td>NA</td>
#     <td>Not Available</td>
#   </tr>
# 
# 
# </table>
# 
# </body>
# </html>
# 
#  

# ### Carregar o Dataset
# 
# Vamos importar o .csv e depois criar as colunas para ano, mês e dia.

# In[3]:


df = pd.read_csv('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/weather-stations20140101-20141231.csv')
df


# ### Limpeza
# 
# Remova as linhas que não possuem nenhum valor no campo __Tm__.

# In[ ]:

df = df.dropna(subset=['Tm'])

# ### Visualização
# 
# Visualização de estações no mapa usando o pacote basemap. O kit de ferramentas de mapa base matplotlib é uma biblioteca para plotar dados 2D em mapas em Python. O Basemap não faz nenhuma plotagem por conta própria, mas fornece as facilidades para transformar coordenadas em projeções de mapa.
# 
# Observe que o tamanho de cada ponto de dados representa a média da temperatura máxima para cada estação em um ano.

# In[ ]:


llon=-140
ulon=-50
llat=40
ulat=65

df = df[(df['Long'] > llon) & (df['Long'] < ulon) & (df['Lat'] > llat) & (df['Lat'] < ulat)]

my_map = Basemap(projection='merc',
            resolution = 'l', area_thresh = 1000.0,
            llcrnrlon=llon, llcrnrlat=llat, #min longitude (llcrnrlon) and latitude (llcrnrlat)
            urcrnrlon=ulon, urcrnrlat=ulat) #max longitude (urcrnrlon) and latitude (urcrnrlat)

plt.figure(figsize=(14,10))
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'white', alpha = 0.3)
my_map.shadedrelief()

# Para coletar dados com base em estações   
xs,ys = my_map(np.asarray(df.Long), np.asarray(df.Lat))
df['xm']= xs.tolist()
df['ym'] =ys.tolist()

#Visualização
for index,row in df.iterrows():
   x,y = my_map(row.Long, row.Lat)
   my_map.plot(row.xm, row.ym, markerfacecolor = 'red',  marker='o', markersize= 5, alpha = 0.75)
plt.show()


# ### Agrupamento de estações com base em sua localização, ou seja, Lat & Lon
# 
# A biblioteca __DBSCAN__ do sklearn pode executar clustering DBSCAN a partir de uma
# matriz vetorial ou matriz de distância. No nosso caso, passamos o array Numpy
# `Clus_dataSet` para encontrar amostras centrais de alta densidade e expandir os
# clusters a partir delas.

# Tendo como base `xm` e `ym`, crie um Dataset chamado `Clus_dataSet`.
# Faça a padronização dos dados através do StandardScaler e calcule o DBSCAN para este Dataset.
# 
# ```python
# eps=0.15 
# min_samples=10
# ```
# 
# Depois de processado, crie uma coluna chamada `Clus_Db` para informar a numeração do cluster.
# 

# In[ ]:
scaler = StandardScaler()

Clus_dataSet = df[['xm','ym']]

Clus_dataSet = scaler.fit_transform(Clus_dataSet)
clus_db = DBSCAN(eps=0.15, min_samples=10).fit_predict(Clus_dataSet)
df['Clus_Db'] = clus_db


# Escreve um código para mostrar os valores únicos para a numeração dos clusters.

# In[ ]:

unique = df['Clus_Db'].unique()
clusterNum = len(unique)
unique


# Como você pode ver para outliers, o rótulo do cluster é -1

# ### Visualização de clusters com base na localização
# 
# Agora, podemos visualizar os clusters usando o base map:

# In[ ]:


my_map = Basemap(projection='merc',
            resolution = 'l', area_thresh = 1000.0,
            llcrnrlon=llon, llcrnrlat=llat, #min longitude (llcrnrlon) and latitude (llcrnrlat)
            urcrnrlon=ulon, urcrnrlat=ulat) #max longitude (urcrnrlon) and latitude (urcrnrlat)


plt.figure(figsize=(14,10))
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'white', alpha = 0.3)
my_map.shadedrelief()

# To create a color map
colors = plt.get_cmap('jet')(np.linspace(0.0, 1.0, clusterNum))

#Visualization1
for clust_number in unique:
    c=(([0.4,0.4,0.4]) if clust_number == -1 else colors[int(clust_number)])
    clust_set = df[df.Clus_Db == clust_number]
    my_map.scatter(clust_set.xm, clust_set.ym, color =c,  marker='o', s= 20, alpha = 0.85)
    if clust_number != -1:
        cenx=np.mean(clust_set.xm) 
        ceny=np.mean(clust_set.ym) 
        plt.text(cenx,ceny,str(clust_number), fontsize=25, color='red',)
        print ("Cluster "+str(clust_number)+', Avg Temp: '+ str(np.mean(clust_set.Tm)))


# ### Agrupamento de estações com base em sua localização, temperatura média, máxima e mínima
# 
# Executamos novamente o DBSCAN, mas desta vez em um conjunto de dados de 5 dimensões.
# 
# Use as colunas `'xm','ym','Tx','Tm','Tn'` do DataFrame original e ajuste o DBSCAN para: 
# 
# ```python
# eps=0.15, min_samples=10
# ```

# In[ ]:



Clus_dataSet = df[['Tx','Tm','Tn']].dropna()

# Clus_dataSet = scaler.fit_transform(Clus_dataSet)
for col in Clus_dataSet.columns:
    scaler = StandardScaler()
    Clus_dataSet[col] = scaler.fit_transform(Clus_dataSet[col].values.reshape(-1,1))


clus_db = DBSCAN(eps=0.15, min_samples=10).fit_predict(Clus_dataSet)
df['Clus_Db'] = clus_db


unique = df['Clus_Db'].unique()
clusterNum = len(unique)
unique


# ### Visualização de clusters com base na localização e temperatura
# 
# Ajuste o código da figura anterior para ter o que se pede.

# In[ ]:

my_map = Basemap(projection='merc',
                 resolution = 'l', area_thresh = 1000.0,
                 llcrnrlon=llon, llcrnrlat=llat, #min longitude (llcrnrlon) and latitude (llcrnrlat)
                 urcrnrlon=ulon, urcrnrlat=ulat) #max longitude (urcrnrlon) and latitude (urcrnrlat)


plt.figure(figsize=(14,10))
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'white', alpha = 0.3)
my_map.shadedrelief()

# To create a color map
colors = plt.get_cmap('jet')(np.linspace(0.0, 1.0, clusterNum))

#Visualization1
for clust_number in unique:
    c=(([0.4,0.4,0.4]) if clust_number == -1 else colors[int(clust_number)])
    clust_set = df[df.Clus_Db == clust_number]
    my_map.scatter(clust_set.xm, clust_set.ym, color =c,  marker='o', s= 20, alpha = 0.85)
    if clust_number != -1:
        cenx=np.mean(clust_set.xm)
        ceny=np.mean(clust_set.ym)
        plt.text(cenx,ceny,str(clust_number), fontsize=25, color='red',)
        print ("Cluster "+str(clust_number)+', Avg Temp: '+ str(np.mean(clust_set.Tm)))



#%%
df