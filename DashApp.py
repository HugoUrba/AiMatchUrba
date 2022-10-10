# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 22:28:15 2022

@author: Maartin
"""
#########################################################################################################################
# import / dependances
import dash
import dash_core_components as dcc    
import dash_html_components as html

import pandas as pd
import numpy as np

import plotly.express as px





# importation données
data = pd.read_csv('df_clean.csv')
print(data.info())


#activités les plus populaires
populatActivite = data.iloc[:,41:57].mean().sort_values(ascending=False)
#print(populatActivite.array)#.index


#études les plus renseignées
etudeRenseigne=data['field_cd'].value_counts().sort_values(ascending=False)
print(etudeRenseigne.index)
#########################################################################################################################
# DASH Application

app = dash.Dash()
  
app.layout = html.Div(children =[
    
    html.H1("Match Ai App"),
    
    dcc.Graph(
        id ="example",
        figure ={
            'data':[
                       {'x':populatActivite.index, 'y':populatActivite.array,'type':'line', 'name':'Activités'},
                   ],
            'layout':{
                'title':'Activités Populaires'
            }
        }
    ),
    dcc.Graph(
        id ="example2",
        figure ={
            'data':[
                       {'x':etudeRenseigne.index, 'y':etudeRenseigne.array,'type':'bar', 'name':'Etudes Des participants'},
                   ],
            'layout':{
                'title':'Etudes des Célibataires'
            }
        }
    )
])

#########################################################################################################################
# Programme Main
if __name__ == '__main__':
    print('Start')
    app.run_server() # démarrer l'application DASH