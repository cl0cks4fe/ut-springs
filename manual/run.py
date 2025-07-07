import folium
import csv

from collections import namedtuple
from utils import coords, data

springs = []
Spring = namedtuple('Spring', ['location', 'name'])

# with open('springs.csv') as f:
#   reader = csv.DictReader(f)
#   for line in reader:
#     springs.append(Spring(**line))

utah_center = [39.30417422299321, -111.63898333979608]
spring_map = folium.Map(location=utah_center, zoom_start=7)

# springs = [Spring('(D-40-24)30c', 'hot'), Spring('(C-22-6)35d', 'Crystal (Madden) Hot Springs')]
springs = [Spring('(D-1-2)19dd', 'tarpie hollow'), Spring('(D-1-2)9aaa', 'boundry'), Spring('(D-1-2)9aac', 'fairmont')]
for spring in springs:
  loc = coords.parse_code(spring.location)
  print(loc)
  section = data.get_section(loc)
  spring_coords = data.get_coords_for_section(section)
  for l in loc.location:
    spring_coords = data.approximate_quadrant(spring_coords, l)

  polygon = folium.Polygon(
      locations=spring_coords,
      color='blue',
      weight=2,
      fill=True,
      fill_color='blue',
      fill_opacity=0.4,
      tooltip=spring.name if spring.name else None
  )
  polygon.add_to(spring_map)

spring_map.save("map.html")
