import xml.etree.ElementTree as ET


root = ET.Element('programming', {'id': '0'})

item = ET.SubElement(root, 'item', {'id': '1.0'})
item.text = 'Research'

item = ET.SubElement(root, 'item', {'id': '1.1'})
item.text = 'Projects'

item = ET.SubElement(root, 'item', {'id': '1.2'})
item.text = 'Networking'

xml_str = ET.tostring(root, encoding='unicode', method='xml')

with open('create_desired_structure.xml','w') as f:
    f.write(xml_str)



