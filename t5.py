from encodings import utf_8
import requests
import json
import folium
import pandas as pd 
import branca
import numpy as np


url = ("c:/Users/Windows 10/Desktop/maps/arquivos")
mteste = f'{url}/mteste.json'
with open(mteste,'r',encoding='utf-8') as mapa_json:
 ler = json.loads(mapa_json.read())


dados = pd.read_csv(f'{url}/populacao.csv', encoding="ISO-8859-1", sep=';')
dados.Populacao = np.log10(dados.Populacao)

colorscale = branca.colormap.linear.YlOrRd_09.scale(0, 10000, 5000000)
populacao = dados.set_index("Codigo_IBGE")["Populacao"]
def style_function(feature):
    colorir = populacao.get(int(feature["Codigo_IBGE"]), None)
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
bins = [0, 10.000, 50.000, 150.000, 500.000, 10000000]
nbbins = len(bins)
folium.Choropleth(
    geo_data=ler,
    data=dados,
    name='choropleth',
    columns=['Codigo_IBGE','Populacao'],
    key_on='feature.properties.GEOCODIGO',
    # style_function=style_function,
    # fill_color='YlOrRd_09',
    bins=nbbins,
    fill_color='RdPu',
    # fill_color='RdYlGn',
    fill_opacity=0.4,
    line_weight=0.5,
    highlight='True',
    legend_name='População'
).add_to(m)

# folium.TopoJson(
#     json.load(requests.head(keys_json)),"objects.mteste",
#     style_function=style_function,
# ).add_to(m)


m.save(f'c:/Users/Windows 10/Desktop/maps/google.html')
