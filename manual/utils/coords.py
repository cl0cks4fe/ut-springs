import pyproj
import re

from collections import namedtuple

SpringLocation = namedtuple('SpringLocation', ['quandrant', 'quandrant_number', 'township', 'range', 'section', 'location'])

def parse_code(location_code):
  location_code = location_code.replace(' ', '')
  pattern = r"\((\w)-(\d+)-(\d+)\)(\d+)(\w*)"
  match = re.match(pattern, location_code)

  if not match:
    return None

  q = match.group(1)
  qn = 1 + ord(q) - ord('A')
  ts = int(match.group(2))
  r = int(match.group(3))
  s = int(match.group(4))
  l = match.group(5)

  return SpringLocation(q, qn, ts, r, s, l)
