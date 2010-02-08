# Copyright (C) 2008 Laurence Tratt http://tratt.net/laurie/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# Use lxml if it is available since it is faster
import json
try:
    from lxml import etree
except ImportError:
    import xml.etree.cElementTree as etree

class Result:

    def __init__(self, ri, dangling):
    
        self.ri = ri
        self.dangling = dangling

    def to_xml(self):
        result = etree.Element('result')
        result.append(self.ri.to_xml())
        etree.SubElement(result, 'dangling').text = self.dangling
        
        return etree.tostring(result, pretty_print=True)


class RCountry:

    def __init__(self, id, name, pp):
    
        self.id = id
        self.name = name
        self.pp = pp

    def to_xml(self):
        country = etree.Element('country')
        etree.SubElement(country, 'id').text = str(self.id)
        etree.SubElement(country, 'name').text = self.name
        etree.SubElement(country, 'pp').text = self.pp
        
        return country


class RPlace:

    def __init__(self, id, name, location, country_id, parent_id, population, pp):

        self.id = id
        self.name = name
        self.location = json.loads(location) # could potentially use eval()
        self.country_id = country_id
        self.parent_id = parent_id
        self.population = population
        self.pp = pp

    def to_xml(self):
        place = etree.Element("place")
        etree.SubElement(place, 'id').text = str(self.id)
        etree.SubElement(place, 'name').text = self.name
        etree.SubElement(place, 'country_id').text = str(self.country_id)
        etree.SubElement(place, 'parent_id').text = str(self.parent_id)
        etree.SubElement(place, 'population').text = str(self.population)
        etree.SubElement(place, 'pp').text = self.pp

        location_xml = etree.SubElement(place, 'location')
        if self.location['type'] == 'Point':
            location_xml.append(geopoint_xml(self.location['coordinates'][0],
                self.location['coordinates'][1]))
        elif self.location['type'] == 'LineString':
            location_xml.append(geoline_xml(self.location['coordinates']))
        elif self.location['type'] == 'Polygon':
            location_xml.append(geoarea_xml(self.location['coordinates']))    
        
        return place
    

class RPost_Code:

    def __init__(self, id, country_id, location, pp):

        self.id = id
        self.country_id = country_id
        self.location = json.loads(location)
        self.pp = pp
        self.dangling = ""

    def to_xml(self):
        postcode = etree.Element("postcode")
        etree.SubElement(postcode, 'id').text = str(self.id)
        etree.SubElement(postcode, 'country_id').text = str(self.country_id)
        etree.SubElement(postcode, 'pp').text = str(self.pp)
        
        location_xml = etree.SubElement(postcode, 'location')
        if self.location['type'] == 'Point':
            location_xml.append(geopoint_xml(self.location['coordinates'][0],
                self.location['coordinates'][1]))
        elif self.location['type'] == 'LineString':
            location_xml.append(geoline_xml(self.location['coordinates']))
        elif self.location['type'] == 'Polygon':
            location_xml.append(geoarea_xml(self.location['coordinates']))
        
        return postcode

# Location type helper functions
def geopoint_xml(lat, long, seq=None):
    point = etree.Element('point')
    etree.SubElement(point, 'lat').text = str(lat)
    etree.SubElement(point, 'long').text = str(long)
    if seq is not None:
        etree.SubElement(point, 'seq').text = str(seq)
    
    return point
    
def geoline_xml(coords=[]):
    line = etree.Element('line')
    for i, coord in enumerate(coords):
        line.append(geopoint_xml(coord[0], coord[1], i+1))
        
    return line
        
def geoarea_xml(coords=[]):
    area = etree.Element('area')
    for i, coord in enumerate(coords):
        area.append(geopoint_xml(coord[0], coord[1], i+1))
        
    return area
