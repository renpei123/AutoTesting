import xlrd
import datetime
import time
import sys
from xml.dom import minidom
import os

class Excel2xml:
    current_path = os.path.dirname(os.path.realpath(__file__))
    job_list_file = os.path.join(current_path, 'REFT_SERVICE_LINE (2).xlsx')

    def convert_xlsx_to_dict_array(self,file_name):
        data = xlrd.open_workbook(file_name)
        table = data.sheets()[0]
        nrows = table.nrows
        columns = table.row_values(0)
        result_list = []
        for i in range(1,nrows):
            value = table.row_values(i)
            row = dict()        
            for i in range(len(columns)):
                row[columns[i]] = value[i]
            result_list.append(row)
        return result_list

    def dict_array_to_xml_file(self,dict_array):
        dom = minidom.Document()
        root_node = dom.createElement('rows')
        dom.appendChild(root_node)
        for dict_value in dict_array:
            print(dict_value)
            row_node = dom.createElement('row')
            root_node.appendChild(row_node)
            for k in dict_value.keys():
                col_node = dom.createElement(k)
                row_node.appendChild(col_node)
                col_text = dom.createTextNode(dict_value[k])
                col_node.appendChild(col_text)
        try:
            with open('excel2xml.xml', 'w', encoding='UTF-8') as fh:
                dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
                print('write xml OK!')
        except Exception as err:
            print('error{0}'.format(err))

if __name__ == "__main__":
    #print(ReadConfig.job_list_file)
    ex = Excel2xml()
    dict_array = ex.convert_xlsx_to_dict_array(ex.job_list_file)
    print(dict_array)
    ex.dict_array_to_xml_file(dict_array)


