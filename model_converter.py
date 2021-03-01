import xml.etree.ElementTree as ET
import os
import re

from get_data import XmlData

class CatProfilesXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
            
    def get_cat_profiles_name(self):
        #for each bh, the lowercategory is bh-1 and the upper one is bh+1
        return re.findall(r"<alternativeID>(.*?)</alternativeID>", self.processed_data)
    
        
class CompatibleAltsXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
            
    def get_alternative_id(self):
        alt_id_data = ''.join(re.findall(r"(<alternativeid=.*?>)", self.processed_data))
        alt_id_data = re.findall(r"\"(.*?)\"", alt_id_data)
        return alt_id_data
    
    def get_active_alternative(self):
        return re.findall(r"<active>(.*?)</active>", self.processed_data)

class CritWeightsXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
            
    def get_criteria_ids(self):
        ids =  re.findall(r"<criterionID>(.*?)</criterionID>", self.processed_data)
        if "".join(ids).isdigit() is True:
            return ["crit"+str(i) for i in ids]
        return ids
    
    def get_criteria_weight(self):
        return re.findall(r"<value><.*?>(.*?)<.*?></value>", self.processed_data)
    
class LambdaXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
    
    def get_lambda(self):
        return re.findall(r"<value><.*?>(.*?)<.*?></value>", self.processed_data)
    
class PerfTableXml :
    def __init__(self, processed_data):
      self.processed_data = processed_data

    def get_alternative_id(self):
        return re.findall(r"<alternativeID>(.*?)</alternativeID>", self.processed_data)

    def get_criterion_id(self):
        data = re.findall(r"<alternativePerformances.*?>(.*?)</alternativePerformances>", self.processed_data)[0]
        ids = re.findall(r"<criterionID>(.*?)</criterionID>", data)
        if "".join(ids).isdigit() is True:
            return ["crit"+str(i) for i in ids]
        return ids
    
    def get_performance_values(self):
        criteria = self.get_criterion_id()
        num_values = re.findall(r"<value><.*?>(.*?)<.*?></value>", self.processed_data)
        return [num_values[i:i + len(criteria)] for i in range(0, len(num_values), len(criteria))]

    def create_dic_values(self):
        #return obj is a dict of dicts : key is alternative id and value is a dic 
        #where the key is the criterion and the value its perf value
        alt_id = self.get_alternative_id()
        crit_id = self.get_criterion_id()
        perf_val = self.get_performance_values()
        
        list_dic = []
        for i in range(len(perf_val)):
            list_dic.append(dict(zip(crit_id, perf_val[i])))
            
        return dict(zip(alt_id,list_dic))
    
    
class CppXmlModelGenerator :
    def __init__(self, prof_table_data, lbd, criteria, criteria_weights, cat_prof_name,  filepath):
        self.prof_table_data = prof_table_data
        self.lbd = lbd
        self.criteria = criteria
        self.cat_prof_name = cat_prof_name
        self.criteria_weights = criteria_weights
        self.filepath = filepath
        
    def create_xml(self):
       # create the file structure
        model = ET.Element('model')

        #giving modelname
        modelname = ET.SubElement(model, 'modelName')
        modelname.text = 'modelName'
        
        #giving number of criteria
        criteria = ET.SubElement(model, 'criteria')
        criteria.text = str(len(self.criteria))
        
        #giving number of categories
        categories = ET.SubElement(model, 'categories')
        categories.text = str(len(self.cat_prof_name))
        
        #giving lambda
        lbda = ET.SubElement(model, 'lambda')
        lbda.text = str(self.lbd[0])
        
        for i, key in enumerate(self.prof_table_data.keys()) : 
            profile = ET.SubElement(model, 'profile')
            profile.text = str(key)
            for j in range(len(self.criteria)) : 
                criterion = ET.SubElement(profile, str(self.criteria[j]))
                criterion.text = self.prof_table_data[key][str(self.criteria[j])]
            weight = ET.SubElement(model, 'weight')
            weight.text = str(self.criteria_weights[i])
            direction = ET.SubElement(model, 'direction')
            direction.text = "1" # default 
    
        # # create a new XML file with the results
        mydata = ET.tostring(model,  xml_declaration=True)
        myfile = open(self.filepath, "wb")
        myfile.write(mydata)
        
    def create_xml_mode_crit(self):
        # create the file structure
        model = ET.Element('model')

        #giving modelname
        modelname = ET.SubElement(model, 'modelName')
        modelname.text = 'modelName'

        #giving number of criteria
        criteria = ET.SubElement(model, 'criteria')
        criteria.text = str(len(self.criteria))

        #giving number of categories
        categories = ET.SubElement(model, 'categories')
        categories.text = str(len(self.cat_prof_name))

        #giving lambda
        lbda = ET.SubElement(model, 'lambda')
        lbda.text = str(self.lbd[0])
        
        for i, crit_id in enumerate(self.criteria) :
            crit = ET.SubElement(model, str(crit_id))
            for cat_profile_name in self.cat_prof_name : 
                cat = ET.SubElement(crit, str(cat_profile_name))
                cat.text = str(self.prof_table_data[cat_profile_name][crit_id])
            weight = ET.SubElement(crit, 'weight')
            weight.text = str(self.criteria_weights[i])
            direction = ET.SubElement(crit, 'direction')
            direction.text = "1" # default 
 
        # create a new XML file with the results
        mydata = ET.tostring(model,  xml_declaration=True)
        new_path = self.filepath.split('.xml')[0] + "crit.xml"
        print(new_path)
        myfile = open(new_path, "wb")
        myfile.write(mydata)
                