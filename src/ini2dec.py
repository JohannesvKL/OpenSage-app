import xml.etree.ElementTree as ET

def ini2dict(path: str, sections: list):
    # Parse the XML configuration
    tree = ET.parse(path)
    root = tree.getroot()
    
    # Initialize an empty dictionary to store the extracted information
    config_dict = {}
    
    
    precursor_mass_tolerance = {}
    fragment_mass_tolerance = {}
    precursor_mass_tolerance_unit = {}
    fragment_mass_tolerance_unit = {}
    
    # Iterate through sections and store information in the dictionary
    for section_name in sections:

        for node in root.findall(f".//ITEMLIST[@name='{section_name}']") or root.findall(f".//ITEM[@name='{section_name}']"):
            node_name = str(node.get("name"))
            node_default = str(node.get("value"))
            node_desc = str(node.get("description"))
            node_rest = str(node.get("restrictions"))

            # change the string representation to list of strings
            restrictions_list = node_rest.split(',') if node_rest else []
                
            entry = {
                "name": node_name,
                "default": node_default,
                "description": node_desc,
                "restrictions": restrictions_list
            }
            
            if "Precursor mass tolerance" in node_desc:  
                entry["name"] = "precursor_mass_tolerance"
                precursor_mass_tolerance = entry
                
            if "Fragment mass tolerance" in node_desc: 
                entry["name"] = "fragment_mass_tolerance"
                fragment_mass_tolerance = entry

            if "Unit of precursor mass tolerance" in node_desc:  
                entry["name"] = "precursor_mass_tolerance_unit"
                precursor_mass_tolerance_unit = entry
                
            if "Unit of fragment mass tolerance" in node_desc: 
                entry["name"] = "fragment_mass_tolerance_unit"
                fragment_mass_tolerance_unit = entry
                
        # Store the entry in the section dictionary
        config_dict[section_name] = entry

        if "mass_tolerance" in section_name:
            config_dict["precursor_mass_tolerance"] = precursor_mass_tolerance
            config_dict["fragment_mass_tolerance"] = fragment_mass_tolerance
            
        if "mass_tolerance_unit" in section_name:
            config_dict["precursor_mass_tolerance_unit"] = precursor_mass_tolerance_unit
            config_dict["fragment_mass_tolerance_unit"] = fragment_mass_tolerance_unit
        
    return config_dict

