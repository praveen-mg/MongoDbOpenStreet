#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sys,re
import pprint
import codecs
import json
from collections import defaultdict
from shape_element import shape_element
#OSM_FILE = "chennai_india.osm"
OSM_FILE = "singapore.osm"
OUTPUT_FILE = "output.osm"
k = 15
street_type_re_number = re.compile(r'\b\S+[0-9]+?$', re.IGNORECASE)
number = re.compile(r'[0-9]+$',re.IGNORECASE)
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
#expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
#            "Trail", "Parkway", "Commons"]
singapore_list = ['Singapore', 'Changi Village', 'Singapore', 'Sembawang', 'Ang Mo Kio', 'Changi Village', 'Singapore', '01-169 Singapore', 'Woodlands Spectrum II', 'Holland Village']

mapping = { "St": "Street",
            "St.": "Street",
            "Ave" : "Avenue",
            "Rd"   : "Road",
            "Dr"   : "Drive",
            "Rd." : "Road",
            "Jl"  : "Jalan",
            "Jl." : "Jalan",
            "Jln." : "Jalan",
            "Jln" : "Jalan",
            "Cresent" : "Crescent"
            }
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def count_tags(filename):
        # YOUR CODE HERE
        tags = {}
        tags_set = set()
        context = ET.iterparse(filename, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        for event,elem in context:
            if not elem.tag in tags:
                tags[elem.tag] = 1
                print tags
            else:
                tags[elem.tag] = tags[elem.tag] + 1
                #print elem.tag
                
            
            #print tags_set
            root.clear()
            elem.clear()
            #pass
        """
            print elem.tag
            if not elem.tag in tags:
                tags[elem.tag] = 1
            else:
                tags[elem.tag] = tags[elem.tag] + 1
        """
                
       
        #print tags['way']
        return tags
def audit_street_type(street_types, street_name):
    m_number = street_type_re_number.search(street_name)
    m = street_type_re.search(street_name)
    street_list = street_name.split(" ")
    m_last_digit = number.search(street_list[len(street_list)-1])
    if 'jalan' in  street_name.lower():
        street_types['jalan'].add(street_name)
    elif m_number or m_last_digit:
        #list_word = street_name.split(" ")
        street_type = street_list[len(street_list)-2]
        #if street_type not in expected:
        street_types[street_type].add(street_name)
    elif m:
        street_type = m.group()
        #if street_type not in expected:
        street_types[street_type].add(street_name)
        

def is_street(tag):
    """
    if 'k' not in tag.attrib:
        print tag.attrib
        return False
    """
    
    return tag.attrib['k'] == "addr:street"

def is_city(tag):
    """
    if 'k' not in tag.attrib:
        print tag.attrib
        return False
    """
    
    return tag.attrib['k'] == "addr:city"

def is_post_code(tag):
    """
    if 'k' not in tag.attrib:
        print tag.attrib
        return False
    """
    
    return tag.attrib['k'] == "addr:postcode"



def is_singapore(elem):
    #pass
    for tag in elem.iter("tag"):
        if is_city(tag):
            if tag.attrib['v'] in singapore_list:
                return True
            else:
                return False

    return True
            
            
    

def update_name(name):

    # YOUR CODE HERE
    name_list = name.split(" ")
    #print name_list[len(name_list)-1]  
    #print mapping[name_list[len(name_list)-1]]
    if name_list[len(name_list)-1] in mapping:
        name_list[len(name_list)-1] = mapping[name_list[len(name_list)-1]]
    if name_list[0] in mapping:
        name_list[0] = mapping[name_list[0]]
    name = " "
    name = name.join(name_list)
    return name
    
def audit_name(osmfile):
    osm_file_name = open(osmfile,"r")
    street_types = defaultdict(set)
    #street_types = set()
    #context = ET.iterparse(osm_file_name, events=("start", "end"))
    context = ET.iterparse(osm_file_name, events=("start",))
    context = iter(context)
    event, root = context.next()
    
    for event,elem in context:
        if elem.tag == "node" or elem.tag == "way":
            #print elem.attrib['changeset']
            """
            if elem.attrib['id'] == "243059228":
                print "Inside Problem node"
                list_elem = list(elem)
                print list_elem
                
                for child in elem:
                    print "Inside Child"
                    print child.tag
                for tag in elem.iter("tag"):
                #for tag in elem.findall("tag"):
                    print "Printing Tag"
                    print tag.attrib
                
                sys.exit(0)
                """
                
            for tag in elem.iter("tag"):
                
                if is_street(tag):
                    
                    better_name = update_name(tag.attrib['v'])
                    if better_name != tag.attrib['v']:
                        print tag.attrib['v'], "=>", better_name
                    #street_types[tag.attrib['v']].add(tag.attrib['v'])
                    #street_types.add(tag.attrib['v'])
                    #audit_street_type(street_types, tag.attrib['v'])
                #else:
                    #print tag.attrib
        else:
             elem.clear()
        root.clear()
         
        #elem.clear()
    return street_types



def audit_city(osmfile):
    osm_file_name = open(osmfile,"r")
    street_types = defaultdict(set)
    #street_types = set()
    #context = ET.iterparse(osm_file_name, events=("start", "end"))
    context = ET.iterparse(osm_file_name, events=("start",))
    context = iter(context)
    event, root = context.next()
    city = set()
    post = []
    
    for event,elem in context:
        shape_element(elem)
        if elem.tag == "node" or elem.tag == "way":
            #print elem.attrib['changeset']
            """
            if elem.attrib['id'] == "243059228":
                print "Inside Problem node"
                list_elem = list(elem)
                print list_elem
                
                for child in elem:
                    print "Inside Child"
                    print child.tag
                for tag in elem.iter("tag"):
                #for tag in elem.findall("tag"):
                    print "Printing Tag"
                    print tag.attrib
                
                sys.exit(0)
                """
            city_now = ""   
            for tag in elem.iter("tag"):
                
                if is_city(tag):
                    city.add(tag.attrib['v'])
                    city_now = tag.attrib['v']
                    #audit_street_type(street_types, tag.attrib['v'])
                if is_post_code(tag):
                    m = number.match(tag.attrib['v']) 
                    if city_now == 'Singapore' or city_now == 'singapore' or city_now == 'Holland Village' or city == 'Sembawang':
                        if m:
                            pass
                        else:
                            post.append(tag.attrib['v'])
                        if len(tag.attrib['v'])  != 6:
                            post.append(tag.attrib['v'])
                
        else:
             elem.clear()
        root.clear()
         
        #elem.clear()
    print "strange postal codes"
    print post
    return city
def is_language(tag):
    values = tag.attrib['k'].split(":")
    if values[0] == "name":
        return True
    return False

def isEnglish(s):

    """
    Taken from http://stackoverflow.com/questions/27084617/detect-strings-with-non-english-characters-in-python
    """
    #print s
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    except :
        return False
    else:
        return True
def audit_language(osmfile):
    osm_file_name = open(osmfile,"r")
    language_types = defaultdict(set)
  
    context = ET.iterparse(osm_file_name, events=("start",))
    context = iter(context)
    event, root = context.next()
    
    for event,elem in context:
        #shape_element(elem)
        if elem.tag == "node" or elem.tag == "way":
            
            city_now = ""   
            for tag in elem.iter("tag"):
                
                if is_language(tag):
                    if isEnglish(tag.attrib['v']):
                        print tag.attrib['v']
                        language_types[tag.attrib['k']].add(tag.attrib['v'])
                    
                    
                
        else:
             elem.clear()
        root.clear()
    #pprint.pprint(language_types)
    
def create_small_file():
    with open(OUTPUT_FILE, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')

        # Write every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write('</osm>')
        print "File created"

def create_json(file_in, pretty = False):
    context = ET.iterparse(file_in, events=("start",))
    context = iter(context)
    event, root = context.next()
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in context:
            el = shape_element(element)
            if el:
                #data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
                del el
            
            
            element.clear()
            root.clear()
    print "Json file created"               
    return data

if __name__ == "__main__":
    #create_small_file()
    #audit_language(OUTPUT_FILE)
    #data = create_json(OUTPUT_FILE, True)
    create_json(OSM_FILE, True)
    #tags = count_tags(OSM_FILE)
    #city = audit_city(OUTPUT_FILE)
    #city = audit_city(OSM_FILE)
    #print city
    #street_types = audit_name(OSM_FILE)
    #street_types = audit_name(OUTPUT_FILE)
    #print "Total Number of Unique Street Names", len(street_types)
    #print street_types
    #for key, value in street_types.items():
       # print key
        #print len([ val for val in value if val])
        #print value
    
    #tree = ET.parse(OUTPUT_FILE)
    #root = tree.getroot()
    #print root.tag
    #print street_types
                
