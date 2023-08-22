# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 09:59:13 2021

@author: adeyem01
"""

from statsbombpy import sb
import pandas as pd
import string

competitions = sb.competitions()
competitionsID = competitions['competition_id'].value_counts()

## for multiples matches
### FIFA World Cup

matches = []
for row in competitions.index[17:18]:
    print(row)
    match = sb.matches(competitions['competition_id'][row], competitions['season_id'][row])
    combo = (competitions['competition_id'][row], competitions['season_id'][row])
    merged = (combo, match)
    matches.append(merged)

IDs = []
for index, match in matches:
    Id = match['match_id']
    ID = list(Id)
    IDs.append(ID)

# Call and encode event for each match

#MatchSequences = []
MatchSequences_fHalf = []
MatchSequences_sHalf = []
MatchData = []

for elements in IDs:
    for element in elements:
        events = sb.events(match_id = int(element))
        teams = '_'.join(map(str,list(events['team'].unique())))    

        eventTactics = events[['index','timestamp','minute','second','team','player','play_pattern', 'type','possession','shot_type']]
        eventTacticsSorted = eventTactics.sort_values(by='index')
        MatchData.append(eventTacticsSorted)
        
        
        # codify unique "type"
        typeList = eventTactics['type'].unique()
        NotypeList = int(len(typeList))
        code =  list(string.ascii_letters)
        code = code[:NotypeList]
        
        Dictionary = pd.DataFrame(typeList, columns=['Type'])
        Dictionary['Code'] = code 
        
        # Select the index and type columns
        Data = eventTacticsSorted[['index', 'type']]

        # Create a Longitudinal 'Type' events
        Dataa = Data.set_index('index')
        
        # replace type with its respective 'code' from the Dictionary.
        for row in Dictionary.index:
            Dataa['type'] = Dataa['type'].replace(Dictionary['Type'][row], Dictionary['Code'][row])
        
        # Split Data into first half
        fHalf = Dataa[:1484]
        
        # Create a long sequence of   type  
        LongSequence =  ''.join(map(str,list(fHalf['type']))) 
        mData = (teams, LongSequence)
        MatchSequences_fHalf.append(mData)
        
        # Split Data into second half
        sHalf = Dataa[1484:]
        
        # Create a long sequence of   type  
        LongSequence =  ''.join(map(str,list(sHalf['type']))) 
        mData = (teams, LongSequence)
        MatchSequences_sHalf.append(mData)

#FIFA2018 = pd.DataFrame(MatchSequences, columns=['Teams','Sequence'])
#FIFA2018.to_csv('FIFA2018.csv', index = False)

   

FIFA2018_fHalf = pd.DataFrame(MatchSequences_fHalf, columns=['Teams','Sequence'])
FIFA2018_fHalf.to_csv('FIFA2018_fHalf.csv', index = False)

FIFA2018_sHalf = pd.DataFrame(MatchSequences_sHalf, columns=['Teams','Sequence'])
FIFA2018_sHalf.to_csv('FIFA2018_sHalf.csv', index = False)


# save main data
for i in range(len(MatchData)):
    name = str(i) + '.csv'
    MatchData[i].to_csv(name, index = False)




## for single match
singleMatch = sb.matches(37, 42)
events = sb.events(match_id = 2275054)
teams = '_'.join(map(str,list(events['team'].unique()))) 
        

events = sb.events(match_id = int(IDs[0]))
teams = '_'.join(map(str,list(events['team'].unique())))    


eventTactics = events[['index','timestamp','minute','second','team','player','play_pattern', 'type','possession','shot_type']]
eventTacticsSorted = eventTactics.sort_values(by='index')


# codify unique "type"
typeList = eventTactics['type'].unique()
NotypeList = int(len(typeList))
code =  list(string.ascii_letters)
code = code[:NotypeList]

Dictionary = pd.DataFrame(typeList, columns=['Type'])
Dictionary['Code'] = code 

# codifty unique 'play_pattern'
#play_patternList = eventTactics['play_pattern'].unique()
#Noplay_pattern= int(len(play_patternList))
#code =  list(string.ascii_uppercase)
#code = code[:Noplay_pattern]

#Dictionary1 = pd.DataFrame(play_patternList, columns=['play_patternList'])
#Dictionary1['Code'] = code 

# Select the index and type columns
Data = eventTacticsSorted[['index', 'type']]

# Split Data into halves
#fHalf = Data[:1484]
#sHalf = Data[1484:]

# Creating Longitudinal event data for halves doesnot matter
# because the encoded data has code for half start and end.
# Thus, patterns with those code can be remove or further analysed

# Create a Longitudinal 'Type' events
Dataa = Data.set_index('index')

# replace type with its respective 'code' from the Dictionary.
for row in Dictionary.index:
    Dataa['type'] = Dataa['type'].replace(Dictionary['Type'][row], Dictionary['Code'][row])


# Create a long sequence of     
LongSequence =  ''.join(map(str,list(Dataa['type']))) 
mData = (teams, LongSequence)
mData = dict(mData)

# Create Dataframe per team
teams = eventTactics['team'].unique()
    
teamsData = []

for team in teams:
    tData = eventTactics[eventTactics['team'] == team]
    teamsData.append(tData)

Barcelona = pd.DataFrame(teamsData[0])
