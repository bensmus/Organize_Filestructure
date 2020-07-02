import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

# this program makes an ONIX file from a .txt file

product_tree_list = []

publishertext = input('Publisher name? ')
infile_name = input('Input file name (use extension .txt)? ')  # for reading the .txt file created by isbn_filestructure.py
outfile_name = input('Output file name (use extension .xml)? ')  # for outputting it to an ONIX file

def elem(name, content=None):
    '''Quick way to define element tree element'''
    
    element = ET.Element(name)
    if content:
        element.text = content
    return element

def subelem(parent, name, content=None):
    '''Quick way to define element tree subelement'''

    element = ET.SubElement(parent, name)
    if content:
        element.text = content
    return element

def subelem_cdata(parent, name, content):
    '''Quick way to define element tree subelement with <![CDATA[{}]]>'''

    element = ET.SubElement(parent, name)
    element.text = '<![CDATA[{}]]>'.format(content)
    return element

''' Functions work like this:
product = elem('product')
title = subelem(product, 'title')
b203 = subelem_cdata(title, 'b203', 'Work-text in General Physics 2 for Senior High School')
product_tree = unescape(ET.tostring(product).decode())
print(product_tree)

Makes a string of valid XML!
'''

def make_product_tree(isbn, titletext, publishertext):
    product = elem('product')
    
    subelem(product, 'a001', isbn)

    productidentifier = subelem(product, 'productidentifier')
    subelem(productidentifier, 'b244', isbn)

    title = subelem(product, 'title')
    subelem_cdata(title, 'b203', titletext)

    contributor = subelem(product, 'contributor')
    subelem_cdata(contributor, 'b036', publishertext)

    language = subelem(product, 'language')
    subelem(language, 'b252', 'eng')

    publisher = subelem(product, 'publisher')
    subelem_cdata(publisher, 'b081', publishertext)

    subelem(product, 'b003', '20200101')
    
    supplydetail = subelem(product, 'supplydetail')
    price = subelem(supplydetail, 'price')
    subelem(price, 'j151', '0.00')

    product_tree = unescape(ET.tostring(product).decode())
    return product_tree


def get_isbn(line):
    '''Used when parsing the input .txt file for isbn'''

    isbn = line[:13]
    return isbn

def get_title(line):
    '''Used when parsing the input .txt file for title'''

    string = line[18:]
    title = ''
    for char in string:
        if char == '.':
            break
        title += char
    print(title)
    return title

# print(make_product_tree('123', 'Cats & Racoons', 'Can be friends')) WORKS

# the .txt file
with open(infile_name, 'r') as f:
    lines = f.readlines()  # list of strings 

# the ONIX file
with open(outfile_name, 'a') as f:
    for line in lines:
        isbn = get_isbn(line)
        titletext = get_title(line)
        product_tree = make_product_tree(isbn, titletext, publishertext)
        f.write(product_tree + '\n')
        