import folium
from folium.plugins import FastMarkerCluster, MarkerCluster
import csv
import pyproj

from collections import namedtuple
from utils import coords, data

web_mercator_proj = pyproj.CRS("EPSG:3857")
wgs84_proj = pyproj.CRS("EPSG:4326")
transformer = pyproj.Transformer.from_crs(web_mercator_proj, wgs84_proj, always_xy=True)

utah_center = [39.30417422299321, -111.63898333979608]
spring_map = folium.Map(location=utah_center, zoom_start=7)

springs = []
Spring = namedtuple('Spring', ['x', 'y', 'name'])

with open('data/springs.csv', encoding='utf-8-sig') as f:
  reader = csv.DictReader(f)
  for line in reader:
    springs.append(Spring(*transformer.transform(line['x'], line['y']), line['GNIS_Name']))

marker_cluster = MarkerCluster(
    overlay=True,
    control=False,
    icon_create_function=None
)

for spring in springs:
    location = spring.y, spring.x
    marker = folium.Marker(location=location)
    popup = ''
    if spring.name:
        popup += f'<b>{spring.name}</b>\n'
    popup += f'{spring.y}, {spring.x}'.format(spring.y, spring.x)
    folium.Popup(popup).add_to(marker)
    marker_cluster.add_child(marker)

marker_cluster.add_to(spring_map)

spring_map.save("springs.html")
