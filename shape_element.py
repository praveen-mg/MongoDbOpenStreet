#from cleanOpenStreet import is_city, is_singapore
import re
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
number = re.compile(r'[0-9]+$',re.IGNORECASE)
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
def is_city(tag):
    """
    if 'k' not in tag.attrib:
        print tag.attrib
        return False
    """
    
    return tag.attrib['k'] == "addr:city"
def is_singapore(elem):
    #pass
    for tag in elem.iter("tag"):
        if is_city(tag):
            if tag.attrib['v'] in singapore_list:
                return True
            else:
                return False

    return True

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
                        #print tag.attrib['v']
                        language_types[tag.attrib['k']].add(tag.attrib['v'])

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
    
def shape_element(element):
    node = {}
    pos = []
    created = {}
    
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        if element.tag == "node":
            node["type"] = "node"
        else:
            node["type"] = "way"
        attrib = element.attrib
        
        created_content = ["version","changeset","timestamp","user","uid"]
        created = {}
        pos = []
        node_refs = []
        #print attrib
        for refVal in element.findall("nd"):
            if refVal  != None:
                refValAttrib = refVal.attrib
                
            for key,val in refValAttrib.iteritems():
                node_refs.append(val)
        address = {}
        prev = False
        prev_address = False
        otherExt = False
        Name = False
        other = {}
        other_list = []
        k_val = None
        
        for kVal in element.findall("tag"):
        
            if kVal  != None:
                kValAttrib = kVal.attrib
                
                for key,val in kValAttrib.iteritems():
                    #print key
                    #print val
                    
                    
                    if key == "k":
                        #print val
                        #if is_singapore:
                            #pass
                        #else:
                            #return None
                        if not problemchars.findall(val):
                            val_list = val.split(":")
                            #print val_list
                            if len(val_list) == 1:
                                k_val = val
                                #print val
                                prev = True
                            elif len(val_list) == 2:
                                #print val_list
                                if val_list[0] == "addr":
                                    k_val = val_list[1]
                                    #print val
                                    prev_address = True
                                elif val_list[0] == "name":
                                    #k_val = val
                                    Name = True
                                else:
                                    #pass
                                    otherExt = True
                                    other["name"] = val_list[0]
                                    other["attribute"] = val_list[1]
                                    
                    elif key == "v":
                        if prev_address:
                            prev_address = False
                            #if k_val == "city":
                                #address[k_val] = "Singapore"
                            if k_val == "street":
                                better_name = update_name(val)
                                address[k_val] = better_name
                            elif k_val == "postcode":
                                m = number.match(val)
                                if m:
                                    if len(val) == 6:
                                        address[k_val] = val
                            else:
                                address[k_val] = val
                            #print k_val,val
                        elif prev:
                            prev = False
                            
                            node[k_val] = val
                        elif Name:
                            Name = False
                            if isEnglish(val):
                                node["name"] = val
                        elif otherExt:
                            #pass
                            otherExt = False
                            other["value"] = val
                            other_list.append(other)
                            other = {}
                    
                                
                            
                            
                        
        
        
        for key,val in attrib.iteritems():
            #print key
            if key in created_content:
                created[key] = val
            elif key == "lon" or key == "lat":
                pos.append(float(val))
            else:
                node[key] = val
        pos = list(reversed(pos))
        node["created"] = created
        node["pos"] = pos
        if bool(address):
            node["address"] = address
        if other_list:
            node["other"] = other_list
        if node_refs:
            node["node_refs"] = node_refs
            
                
                #print val
        #print "print node"
        #print node
        return node
        element.clear()
    else:
        element.clear()
        return None

