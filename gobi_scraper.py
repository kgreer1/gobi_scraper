"""
Kat Greer
Agnes Scott College

The file scrapes GOBI for print and ebook pricing.

Adapted from python file created by Katharine Frazier, NC State University Libraries
https://github.com/kchasefray/GOBI_Searching

"""

import pandas as pd
import re
from selenium import webdriver
import gobi_config

#establish webdriver
browser = webdriver.Firefox()

#tell browser to fetch website
browser.get('https://www.gobi3.com/Pages/Login.aspx')

#find username field, send username
userElem = browser.find_element_by_id('guser')
userElem.send_keys(gobi_config.username)

#find password field, send password
passwordElem = browser.find_element_by_id('gpword')
passwordElem.send_keys(gobi_config.password)
passwordElem.submit()

#create empty lists
isbn_list = []
binding_list = []
price_list = []

choices = {}

#read in ISBNs from file
file = pd.read_excel(gobi_config.input_file, index_col=0, dtype={'isbn': 'str'})

#append column values to list
isbn_list = file['isbn'].values

#iterate through list searching for each isbn in GOBI
#for i in range(0, len(isbn_list) - 1):

#find search box
searchElem = browser.find_element_by_id('basicsearchinput')
#input isbn from list
searchElem.send_keys(isbn_list[0])
#submit
searchElem.submit()

#find all results on results page
itemElem = browser.find_elements_by_id('containeritems')

print(itemElem)

# #iterate through results and transform each web element into a text element
# for item in itemElem:
#     individual_item = item.text

#     #regex to find price
#     priceRegex = re.compile(r'(\d+(?:\.\d+)\s)')
#     rawprice = priceRegex.search(str(individual_item))
#     price = rawprice.group()

#     #regex to find binding (ebook, cloth, paper)
#     bindingRegex = re.compile(r'Binding:(\w+)')
#     ebookorprint = bindingRegex.search(str(individual_item))
#     binding = ebookorprint.group()

#     #append resuls to list
#     binding_list.append(binding)
#     price_list.append(price)

# #add lists to results dictionary
# #choices.update({'isbn': isbn_list})
# choices.update({'binding': binding_list})
# choices.update({'price': price_list})

# #create df of choices dictionary
# df = pd.DataFrame.from_dict(choices)
# #df.groupby('isbn')
# #send to excel file
# df.to_excel(gobi_config.output_file)