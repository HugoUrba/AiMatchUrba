import pandas as pd
data = pd.read_csv('train.csv',on_bad_lines="skip",delimiter=";")
#recodage sexe
data.loc[:,'gender'][data.loc[:,'gender']==1]='Homme'
data.loc[:,'gender'][data.loc[:,'gender']==0]='Femme'
#recodage métiers
data.loc[:,'career_c'][data.loc[:,'career_c']==1]='Lawyer'
data.loc[:,'career_c'][data.loc[:,'career_c']==2]='Academic'
data.loc[:,'career_c'][data.loc[:,'career_c']==3]='Psychologist'
data.loc[:,'career_c'][data.loc[:,'career_c']==4]='Doctor'
data.loc[:,'career_c'][data.loc[:,'career_c']==5]='Engineer'
data.loc[:,'career_c'][data.loc[:,'career_c']==6]='Entertainment'
data.loc[:,'career_c'][data.loc[:,'career_c']==7]='Finance/Marketing'
data.loc[:,'career_c'][data.loc[:,'career_c']==8]='Real Estate'
data.loc[:,'career_c'][data.loc[:,'career_c']==9]='Humanitarian Affairs'
data.loc[:,'career_c'][data.loc[:,'career_c']==10]='Undecided'
data.loc[:,'career_c'][data.loc[:,'career_c']==11]='Social Work'
data.loc[:,'career_c'][data.loc[:,'career_c']==12]='Speech Pathology'
data.loc[:,'career_c'][data.loc[:,'career_c']==13]='Politics'
data.loc[:,'career_c'][data.loc[:,'career_c']==14]='Athletics'
data.loc[:,'career_c'][data.loc[:,'career_c']==15]='Other'
data.loc[:,'career_c'][data.loc[:,'career_c']==17]='Architecture'
#recodage âge
data['age'][data['age']<23]=1
data['age'][(data['age']>22) & (data['age']<28)]=2
data['age'][(data['age']>27) & (data['age']<33)]=3
data['age'][(data['age']>32) & (data['age']<38)]=4
data['age'][data['age']>37] = 5
data['age'][data['age']==1]='[18-22]'
data['age'][data['age']==2]='[23-27]'
data['age'][data['age']==3]='[28-32]'
data['age'][data['age']==4]='[33-37]'
data['age'][data['age']==5]='38+'
#remplacer ',' par '.' pour var quanti et changer nom col
data['income']=data['income'].replace(",","",regex=True)
data['income']=data['income'].astype(float)
data.iloc[:,64:70]=data.iloc[:,64:70].replace(",",".",regex=True)
data.iloc[:,64:70]=data.iloc[:,64:70].astype(float)


data.to_csv('trainClean.csv', index=False)