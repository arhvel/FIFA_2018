# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 18:29:30 2021

@author: adeyem01
"""

import pandas as pd
import string


data = pd.read_csv('0.csv')

Data = data[['index', 'type']]

typeList = Data['type'].unique()
NotypeList = int(len(typeList))
code =  list(string.ascii_letters)
code = code[:NotypeList]

Dictionary = pd.DataFrame(typeList, columns=['Type'])
Dictionary['Code'] = code 
Dictionary.to_csv('Dictionary.csv', index = False)

# Split Data into halves
#fHalf = Data[:1484]
#sHalf = Data[1484:]

# Creating Longitudinal event data for halves doesnot matter
# because the encoded data has code for half start and end.
# Thus, patterns with those code can be remove or further analysed

top = pd.read_csv('top.csv')
topp = top.copy()

# Create a Longitudinal 'Type' events
Dataa = Data.set_index('index')

# replace type with its respective 'code' from the Dictionary.
for row in Dictionary.index:
    topp['Subsequences1'] = topp['Subsequences1'].str.replace(Dictionary['Code'][row], Dictionary['Type'][row])

topp['Subsequences1'] = topp['Subsequences1'].str.replace(Dictionary['Code'], Dictionary['Type'])

df['range'] = df['range'].str.replace(',','-')

pat = 'dc'

encoded = []
for riw in Dictionary.index:
    li = list(pat)
    lis = li.replace(Dictionary['Code'][row], Dictionary['Type'][row])
    encoded.append(lis)