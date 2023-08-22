#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 19:11:45 2022

@author: adeyem01
"""

import glob, string
import pandas as pd

parent_dir = '/home/adeyem01/Documents/Study3/fifa/MatchEventsDB/'
sensorFolders =  sorted([i for i in glob.glob('*.csv')])
sensorFolders = sensorFolders[:len(sensorFolders)-1]

topTeams = ['France','Uruguay', 'Russia', 'Croatia', 'Brazil', 'Belgium', 'Sweden', 'England'] 
Dictionary = pd.read_csv("EventDictionary.csv")
letters = list(string.ascii_letters)[:len(Dictionary)]
Dictionary['Code'] = letters


for file in sensorFolders:
    match = pd.read_csv(file)
    
    teams = ','.join(list(match['team'].unique())).split(",")
   
    for team in teams:
        if team in topTeams:
            cat = "Top"
        else:
            cat = "Low"
            
        t = match.loc[match['team']==team].copy()
        s = list(t['type'])
        
        for row in Dictionary.index:
            t['type'] = t['type'].replace(Dictionary['Events'][row], Dictionary['Code'][row])
            
      
        possession = list(t['possession'].unique())
    
        possessionData = []
        for p in possession[1:]:
            dum = t.loc[t['possession'] == p]
            if len(dum) > 5:
                sequence =  ("".join(list(dum['type'])),team, cat)
                possessionData.append(sequence)
        
        frame = pd.DataFrame(possessionData, columns = ['Sequences', 'Teams', 'Label'])
        frame.to_csv(parent_dir+team +"_"+file, index=False)