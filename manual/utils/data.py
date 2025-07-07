import sqlite3
import json

_data = []
def data():
  global _data
  if not _data:
    with open('data/plss_utah.geojson') as f:
      _data = json.loads(f.read())['features']
  return _data


def get_section(loc):
  last = None
  for section in data():
    s_prop = section['properties']
    if float(s_prop['TOWNSHIP']) == loc.township and float(s_prop['RANGE']) == loc.range and float(s_prop['SECTION']) == loc.section and s_prop['QNUM'] == loc.quandrant_number:
      # return section
      print(section)
      last = section
  return last


def get_coords_for_section(section):
  return [c[::-1] for c in section['geometry']['coordinates'][0]]


def approximate_quadrant(coords, quadrant):
  quadrant = quadrant.lower()
  if quadrant not in {'a', 'b', 'c', 'd'}:
    raise ValueError('quadrant must be one of "a", "b", "c", or "d"')

  # approximate shape with four corners
  x_coords, y_coords = zip(*coords)
  min_x, max_x = min(x_coords), max(x_coords)
  min_y, max_y = min(y_coords), max(y_coords)

  # Compute midpoints
  mid_x = (min_x + max_x) / 2
  mid_y = (min_y + max_y) / 2

  # Define the corner points for each quadrant
  quadrant_points = {
      'a': [[max_x, max_y], [mid_x, max_y], [mid_x, mid_y], [max_x, mid_y]],
      'b': [[max_x, mid_y], [mid_x, mid_y], [mid_x, min_y], [max_x, min_y]],
      'c': [[mid_x, mid_y], [min_x, mid_y], [min_x, min_y], [mid_x, min_y]],
      'd': [[mid_x, max_y], [min_x, max_y], [min_x, mid_y], [mid_x, mid_y]],
  }

  return quadrant_points[quadrant]
