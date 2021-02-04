import xml.etree.ElementTree as ET
import os
import re

from get_data import XmlData

class AlternativeXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
            
    def get_active_alternatives(self):
        return re.findall(r"<active>(.*?)</active>", self.processed_data)
    
    def get_id_and_name_alternatives(self):
        name_id_data = ''.join(re.findall(r"(<alternativeid=.*?>)", self.processed_data))
        name_id_data = re.findall(r"\"(.*?)\"", name_id_data)
        return name_id_data[::2], name_id_data[1::2]
        

class AssignXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
            
    def get_alternative_id(self):
        return re.findall(r"<alternativeID>(.*?)</alternativeID>", self.processed_data)
    
    def get_category_assignment(self):
        return re.findall(r"<categoryID>(.*?)</categoryID>", self.processed_data)
    
    def get_dic_altid_to_cat(self):
        return dict(zip(self.get_alternative_id(), self.get_category_assignment()))

class CategoriesXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
            
    def get_active_categories(self):
        active = re.findall(r"<active>(.*?)<.*?active>", self.processed_data)
        if active == [] :
            return None
        return active
    
    def get_category_id(self):
        cat_id_data = ''.join(re.findall(r"(<categoryid=.*?>)", self.processed_data))
        cat_id_data = re.findall(r"\"(.*?)\"", cat_id_data)
        return cat_id_data
    
    def get_category_rank(self):
        return re.findall(r"<rank><.*?>(.*?)<.*?></rank>", self.processed_data)
    
    def get_dic_id_to_rank(self):
        active = self.get_active_categories()
        idx = self.get_category_id()
        rank = self.get_category_rank()
        if active is None :
            return dict(zip(idx,rank))
        dic = dict()
        for i, elmt in enumerate(active) : 
            if elmt == 'true':
                dic[idx[i]] = rank[i]
        return dic
                

class CriteriaXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data

    def get_criterion_id(self):
        crit_data = ''.join(re.findall(r"(<criterionid=.*?>)", self.processed_data))
        crit_data = re.findall(r"\"(.*?)\"", crit_data)
        return crit_data
    
class ParamXml :
    def __init__(self, processed_data):
        self.processed_data = processed_data
    
    def get_model_param(self):
        models_data = ''.join(re.findall(r"(<parameterid=.*?>)", self.processed_data))
        models_data = re.findall(r"\"(.*?)\"", models_data)
        num_data = re.findall(r"<value><.*?>(.*?)<.*?></value>", self.processed_data)
        return dict(zip(models_data, num_data))

class PerfTableXml :
    def __init__(self, processed_data):
      self.processed_data = processed_data

    def get_alternative_id(self):
        return re.findall(r"<alternativeID>(.*?)</alternativeID>", self.processed_data)

    def get_criterion_id(self):
        data = re.findall(r"<alternativePerformances>(.*?)</alternativePerformances>", self.processed_data)[0]
        return re.findall(r"<criterionID>(.*?)</criterionID>", data)
    
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
    
class CppXmlDataGenerator :
    def __init__(self, pert_table_data, cat_assignment, dic_categories, filepath):
        self.pert_table_data = pert_table_data
        self.cat_assignment = cat_assignment
        self.dic_categories = dic_categories
        self.filepath = filepath
        
    def create_xml(self):
       # create the file structure
        dataset = ET.Element('dataset')

        #giving datasetname
        datasetname = ET.SubElement(dataset, 'datasetname')
        datasetname.text = 'datasetNameTest'
        
        #giving number of criteria
        criteria = ET.SubElement(dataset, 'criteria')
        criteria.text = str(len(self.pert_table_data[list(self.pert_table_data.keys())[0]].values()))
        
        #giving number of categories
        categories = ET.SubElement(dataset, 'categories')
        categories.text = str(len(self.dic_categories))
        
        #giving number of alternatives
        alternatives = ET.SubElement(dataset, 'alternatives')
        alternatives.text = str(len(self.pert_table_data))
        
        for i, key in enumerate(self.pert_table_data.keys()) : 
            alternative = ET.SubElement(dataset, 'alternative')
            alternative.text = str(key)
            for criteria_id in self.pert_table_data[key].keys() : 
                criterion = ET.SubElement(alternative, str(criteria_id))
                criterion.text = self.pert_table_data[key][criteria_id]
            assignment = ET.SubElement(alternative, 'assignment')
            
            if self.cat_assignment[key] not in self.dic_categories.values():
                assignment.text = str(self.dic_categories[self.cat_assignment[key]])
            else :
                assignment.text = str(self.cat_assignment[key])

        # # create a new XML file with the results
        mydata = ET.tostring(dataset,  xml_declaration=True)
        myfile = open(self.filepath, "wb")
        myfile.write(mydata)
                