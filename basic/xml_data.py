import os.path
import sys
import xml.dom.minidom


xml_path = 'D:/Code/Python_Learn_Note/dataset/xml/rs00012.xml'

dom = xml.dom.minidom.parse(xml_path)
print('dom: \n',dom)

root = dom.documentElement
print('root: \n',root)

objects = root.getElementsByTagName('object')
print('objects: \n',objects)

for i,obj in enumerate(objects):
    name = obj.getElementsByTagName('name')[0].firstChild.data
    
    print(name)

