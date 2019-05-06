from xml.dom import minidom

dom=minidom.Document()
root_node=dom.createElement('root')
dom.appendChild(root_node)
book_node=dom.createElement('book')
root_node.appendChild(book_node)
book_node.setAttribute('price','199')
name_node=dom.createElement('name')
root_node.appendChild(name_node)
name_text=dom.createTextNode('program_version_1')
name_node.appendChild(name_text)
root_node.appendChild(name_node)
name_node2 = dom.createElement('name')
root_node.appendChild(name_node2)
name_text2 = dom.createTextNode('program_version_2')
name_node2.appendChild(name_text2)
try:
    with open('dom_write.xml','w',encoding='UTF-8') as fh:
        dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
        print('write xml OK!')
except Exception as err:
    print('error{0}'.format(err))