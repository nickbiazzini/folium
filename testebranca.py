import json
from textwrap import fill
from turtle import fillcolor
from types import LambdaType
import folium
import numpy as np
import pandas as pd
from branca.element import Element
import branca
import branca.colormap as cm
from branca.colormap import linear


url = ("c:/Users/Windows 10/Desktop/maps/arquivos")
mteste = f'{url}/mteste.json'
with open(mteste,'r',encoding='utf-8') as mapa_json:
 ler = json.loads(mapa_json.read())
 dados = pd.read_csv(f'{url}/populacao.csv', encoding="ISO-8859-1", sep=';')

dp = dados.set_index('Codigo_IBGE')['Populacao']

dados.Populacao = np.log10(dados.Populacao)

m = folium.Map([-14.240073, -53.180502], zoom_start=7)
colormap = linear.YlOrRd_09.scale(6,20)
folium.GeoJson(
    ler,
    name='mapa',
    style_function=lambda feature: {
        'fillColor': colormap(ler[feature[0]]),
        'color': 'black',
        'weight': 0.3,
    }
    
).add_to(m)


c = folium.Choropleth(
    geo_data=ler,
    name="choropleth",
    data=dados,
    columns=["Codigo_IBGE", "Populacao"],
     key_on='feature.properties.GEOCODIGO',
    # fill_color="RdPu",
    # style_function= style,
    # fill_color='OrRd',
    fill_opacity=0.4,
    # threshold_scale=[0,2,4,6,8],
    line_weight=0.5,
    highlight='True',
    legend_name='População'
) 
c.add_to(m)


e = Element("""
  var ticks = document.querySelectorAll('div.legend g.tick text')
  for(var i = 0; i < ticks.length; i++) {
    var value = parseFloat(ticks[i].textContent.replace(',', ''))
    var newvalue = Math.pow(10.0, value).toFixed(0).toString()
    ticks[i].textContent = newvalue
  }
""")

colormap.caption='População'
colormap.add_to(m)

# color = c.color_scale
html = c.get_root()
html.script.get_root().render()
html.script.add_child(e)

folium.LayerControl().add_to(m)

m.save('testebranca.html')