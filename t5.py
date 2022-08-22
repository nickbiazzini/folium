from encodings import utf_8
from turtle import fillcolor
from urllib import request
import requests
import json
import folium
import pandas as pd 
import branca



url = ("c:/Users/Windows 10/Desktop/maps")

# arquivo_json = f'{url}/mteste.json'
mteste = f'{url}/mteste.json'
with open(mteste,'r',encoding='utf-8') as mapa_json:
 ler = json.loads(mapa_json.read())

dados = pd.read_csv(f'{url}/populacao.csv', encoding="ISO-8859-1", sep=';')

populacao = dados.set_index("Codigo_IBGE")["Populacao"]
colorscale = branca.colormap.linear.YlOrRd_09.scale(0, 50e3)
def style_function(feature):
    colorir = populacao.get(int(feature["Codigo_IBGE"][-7:]), None)
    return {
        "fillOpacity": 0.5,
        "weight": 0,
        "fillColor": "#black" if colorir is None else colorscale(colorir),
    }

m = folium.Map([-14.240073, -53.180502], zoom_start=7)
# tiles='Stamen Toner'


folium.raster_layers.TileLayer(
    tiles="http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    attr="google",
    name="google street view",
    max_zoom=20,
    subdomains=["mt0", "mt1", "mt2", "mt3"],
    overlay=False,
    control=True,
).add_to(m)

folium.Choropleth(
    geo_data=ler,
    data=dados,
    name='choropleth',
    columns=['Codigo_IBGE','Populacao'],
    key_on='feature.properties.GEOCODIGO',
    # bins=9,
    # style_function=style_function,
    # fill_color='YlOrRd_09',
    fill_color='Set1',
    # fill_color='RdYlGn',
    fill_opacity=0.4,
    line_weight=0.5,
    highlight='True',
    legend_name='População'
).add_to(m)



m.save(f'{url}/google.html')
