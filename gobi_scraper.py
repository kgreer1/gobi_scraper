"""
Kat Greer
Agnes Scott College

This python script scrapes GOBI for print and ebook pricing.

Adapted from python script created by Katharine Frazier, NC State University Libraries
https://github.com/kchasefray/GOBI_Searching

"""

import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
result_title_list = []
result_isbn_list = []
result_binding_list = []
result_price_list = []

#create empty dictonary for results
results = {}

#read in ISBNs from file
file = pd.read_excel(gobi_config.input_file, index_col=0, dtype={'isbn': 'str'})

#append column values to list
isbn_list = file['isbn'].values

#iterate through list searching for each isbn in GOBI
#for i in range(0, len(isbn_list) - 1):

#find search box
searchElem = WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.ID, 'basicsearchinput')))
#clear search box input field
searchElem.clear()
#input isbn from list
searchElem.send_keys(isbn_list[0])
#submit
searchElem.submit()

#wait for results page to load and find all results on results page
itemElem = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@id="containeritems"]/div')))

#iterate through results and transform each web element into a text element
for item in itemElem:
    individual_item = item.text
    print(individual_item)

    #regex to find isbn
    isbnRegex = re.compile(r'ISBN:(\d+)')
    rawisbn = isbnRegex.search(str(individual_item))
    isbn = rawisbn.group(1)

    #regex to find title
    titleRegex = re.compile(r'Title:(.+)')
    rawtitle = titleRegex.search(str(individual_item))
    print(rawtitle)
    title = rawtitle.group(1)
    print(title)

    #regex to find price
    priceRegex = re.compile(r'(\d+(?:\.\d+)\s)')
    rawprice = priceRegex.search(str(individual_item))
    price = rawprice.group(1)

    #regex to find binding (ebook, cloth, paper)
    bindingRegex = re.compile(r'Binding:(\w+)')
    ebookorprint = bindingRegex.search(str(individual_item))
    binding = ebookorprint.group(1)

    #append results to list
    result_isbn_list.append(isbn)
    result_title_list.append(title)
    result_binding_list.append(binding)
    result_price_list.append(price)

#add lists to results dictionary
results.update({'isbn': result_isbn_list})
results.update({'title': result_title_list})
results.update({'binding': result_binding_list})
results.update({'price': result_price_list})

print(results)

#create dataframe of choices dictionary
df = pd.DataFrame.from_dict(results)
df.groupby('isbn')

#send results to excel file
df.to_excel(gobi_config.output_file)