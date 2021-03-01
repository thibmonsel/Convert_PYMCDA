


if __name__ == '__main__':
    from get_data import XmlData
    from dataset_converter import AlternativeXml, AssignXml, CategoriesXml, CriteriaXml, ParamXml, PerfTableXml, CppXmlDataGenerator 
    from model_converter import CatProfilesXml, CompatibleAltsXml, CritWeightsXml, LambdaXml, PerfTableXml, CppXmlModelGenerator
    import os
    
    data_path = "./pymcda/ws/LearnMRSortMeta/tests/"
    
    #for data
    for filename in os.listdir(data_path):
        if filename.startswith("in") and filename != "in6" :
                        
            filepath = data_path + "/" +filename + "/alternatives.xml"
            filepath2 = data_path + "/" +filename + "/assign.xml"
            filepath3 = data_path + "/" +filename + "/categories.xml"
            filepath4 = data_path + "/" +filename + "/criteria.xml"
            filepath5 = data_path + "/" +filename + "/perfs_table.xml"
            
            xml = XmlData(filepath)
            xml.parse_data()
            alt = AlternativeXml(xml.raw_data)
            
            xml2 = XmlData(filepath2)
            xml2.parse_data()
            assig = AssignXml(xml2.raw_data)
            cat_assignment = assig.get_dic_altid_to_cat()
        
            xml3 = XmlData(filepath3)
            xml3.parse_data()
            cat = CategoriesXml(xml3.raw_data)
            categories = cat.get_dic_id_to_rank()
        
            xml4 = XmlData(filepath4)
            xml4.parse_data()
            crit = CriteriaXml(xml4.raw_data)
            criteria = crit.get_criterion_id()
            
            from dataset_converter import PerfTableXml
            xml5 = XmlData(filepath5)
            xml5.parse_data()
            perf = PerfTableXml(xml5.raw_data)
            pert_table_data = perf.create_dic_values()

            # print('filename : ', filename, '\n')
            # print("nb of alt : ", len(pert_table_data), '\n')
            # print("perftable", pert_table_data, '\n')
            # print("cat_assignment", cat_assignment, '\n')
            # print("criteria", criteria, '\n')
            # print("categories", categories, '\n')
            # print(' -------------- \n')
            
            #create xml files for c++
            gen = CppXmlDataGenerator(pert_table_data, cat_assignment, categories,  "data/" + filename + 'dataset.xml')
            gen.create_xml()
            
            
    for filename in os.listdir(data_path):
        if filename.startswith("out") and filename != "out6" and filename !="out5":
            filepath = data_path +filename + "/cat_profiles.xml"
            filepath2 = data_path +filename + "/compatible_alts.xml"
            filepath3 = data_path +filename + "/crit_weights.xml"
            filepath4 = data_path +filename + "/lambda.xml"
            filepath5 = data_path +filename + "/profiles_perfs.xml"
            
            xml = XmlData(filepath)
            xml.parse_data()
            alt = CatProfilesXml(xml.raw_data)
            cat_prof_name= alt.get_cat_profiles_name()
            
            xml2 = XmlData(filepath2)
            xml2.parse_data()
            comp = CompatibleAltsXml(xml2.raw_data)
            
            xml3 = XmlData(filepath3)
            xml3.parse_data()
            crit = CritWeightsXml(xml3.raw_data)
            criteria = crit.get_criteria_ids()
            criteria_weights = crit.get_criteria_weight()
            
            xml4 = XmlData(filepath4)
            xml4.parse_data()
            lamb = LambdaXml(xml4.raw_data)
            ldba = lamb.get_lambda()
            
            xml5 = XmlData(filepath5)
            xml5.parse_data()
            prof = PerfTableXml(xml5.raw_data)
            prof_table_data = prof.create_dic_values()
            
            print("filename :", filename)
            print("prof_table", prof_table_data)
            print("lmabda", ldba)
            print("criteria", criteria)
            print("criteria weigths", criteria_weights)
            print("cat prof name", cat_prof_name, '\n\n')
            
            #create xml files for c++
            gen = CppXmlModelGenerator(prof_table_data, ldba, criteria, criteria_weights ,cat_prof_name, "data/" + filename + 'model.xml')
            gen.create_xml()
            gen.create_xml_mode_crit()