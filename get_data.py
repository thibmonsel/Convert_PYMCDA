import xml.etree.ElementTree as ET
import os
import re

class XmlData: 
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw_data = self.get_xml_data()
    
    def get_xml_data(self):
        with open(self.filepath, 'r+') as xml_data:
            data = xml_data.readlines()
        return(' '.join(data))
  
    def parse_data(self):
        self.raw_data = re.sub(r"\s+", "", self.raw_data)
        self.raw_data = re.split(r"(<.*?>)", self.raw_data)
        self.raw_data = list(filter(None, self.raw_data))
        self.raw_data = ''.join(self.raw_data)