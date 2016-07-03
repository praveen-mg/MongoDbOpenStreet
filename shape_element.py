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
                        if not problemchars.findall(val):
                            val_list = val.split(":")
                            #print val_list
                            if len(val_list) == 1:
                                k_val = val
                                #print val
                                prev = True
                            elif len(val_list) == 2:
                                print val_list
                                if val_list[0] == "addr":
                                    k_val = val_list[1]
                                    #print val
                                    prev_address = True
                                else:
                                    #pass
                                    otherExt = True
                                    other["name"] = val_list[0]
                                    other["attribute"] = val_list[1]
                                    
                    elif key == "v":
                        if prev_address:
                            prev_address = False
                            address[k_val] = val
                            print k_val,val
                        elif prev:
                            prev = False
                            node[k_val] = val
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
        print "print node"
        print node
        return node
    else:
        return None

