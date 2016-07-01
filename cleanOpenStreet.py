#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from collections import defaultdict
OSM_FILE = "chennai_india.osm"
OUTPUT_FILE = "output.osm"
k = 10

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

def is_street(tag):
    
    if 'k' not in tag.attrib:
        print tag.attrib
        return False
    return tag.attrib['k'] == "addr:street"


def audit_name(osmfile):
    osm_file_name = open(osmfile,"r")
    #street_types = defaultdict(set)
    street_types = set()
    #context = ET.iterparse(osm_file_name, events=("start", "end"))
    context = ET.iterparse(osm_file_name, events=("start",))
    context = iter(context)
    event, root = context.next()
    for event,elem in context:
        if elem.tag == "node" or elem.tag == "way":
            print elem.attrib['changeset']
            for tag in elem.iter("tag"):
                
                if is_street(tag):
                    #street_types[tag.attrib['v']].add(tag.attrib['v'])
                    street_types.add(tag.attrib['v'])
                else:
                    print tag.attrib
        root.clear()
         
        elem.clear()
    print street_types

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

if __name__ == "__main__":
    #create_small_file()
    #tags = count_tags(OSM_FILE)
    audit_name(OUTPUT_FILE)
    #print street_types
                
