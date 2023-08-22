
import glob, string
import pandas as pd

sensorFolders =  sorted([i for i in glob.glob('*.csv')])
sensorFolders = sensorFolders[:len(sensorFolders)-1]

topTeams = ['France','Uruguay', 'Russia', 'Croatia', 'Brazil', 'Belgium', 'Sweden', 'England'] 
Dictionary = pd.read_csv("EventDictionary.csv")
letters = list(string.ascii_letters)[:len(Dictionary)]
Dictionary['Code'] = letters


SequencesP = []
for file in sensorFolders:
    match = pd.read_csv(file)
    
    teams = ','.join(list(match['team'].unique())).split(",")
    
    for team in teams:
        t = match.loc[match['team']==team].copy()
        s = list(t['type'])
        
        for row in Dictionary.index:
            t['type'] = t['type'].replace(Dictionary['Events'][row], Dictionary['Code'][row])
      
        possession = list(t['possession'].unique())
    
        for p in possession[1:]:
            dum = t.loc[t['possession'] == p]
            if len(dum) > 5:
                if team in topTeams:
                    sequence =  ("".join(list(dum['type'])),team, 'Top')
                    SequencesP.append(sequence)
                else:
                    sequence =  ("".join(list(dum['type'])),team, 'Low')
                    SequencesP.append(sequence)
      
DataP = pd.DataFrame(SequencesP, columns = ['Sequences', 'Teams', 'Label'])   

#DataP_top = DataP[DataP['Label']== 'Top']
#DataP_low = DataP[DataP['Label']== 'Low']
#Data = [DataP_top, DataP_low]