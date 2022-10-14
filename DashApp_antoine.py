# import / dependances
import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objs as go

# importation données
#data = pd.read_csv('df_clean.csv')
data = pd.read_csv('train.csv',on_bad_lines="skip",delimiter=";")
print(data.info())

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
data['age'][data.loc[:,'age']<23]=1
data['age'][(data['age']>22) & (data['age']<28)]=2
data['age'][(data['age']>27) & (data['age']<33)]=3
data['age'][(data['age']>32) & (data['age']<38)]=4
data['age'][data['age']>37] = 5

data['age'][data['age']==1]='[18-22]'
data['age'][data['age']==2]='[23-27]'
data['age'][data['age']==3]='[28-32]'
data['age'][data['age']==4]='[33-37]'
data['age'][data['age']==5]='38+'

#graph répartition âge
datanew=data.loc[:,('iid','age')]
datanew=datanew.drop_duplicates()
dataage=datanew['age']

#graph répartition catégories travail
datanew=data.loc[:,('iid','career_c')]
datanew=datanew.drop_duplicates()
datacar=datanew['career_c']



#graphique décision
decision=data.loc[:,('dec_o','gender','age','career_c')]


app = dash.Dash()

app.layout = html.Div([
        html.Div(
            html.H1("Match Ai App", style={'color' :'red','text-align':'center'}),
            style={'border' : '1px black solid','float':'left','width':'99%','height':'80px'}),

    html.Div(
        dcc.Graph(
            id="pie_age",
            figure={'data': [go.Pie(values=dataage.value_counts(),labels=('[23-27]','[28-32]','[18-22]','[33-37]','38+'))],
                'layout': {'title': 'Répartition des âges'}
                    }),
        style={'border' : '1px black solid','float':'left','width':'30%','height':'450px'}),

    html.Div(
        dcc.Graph(
            id="hist_metier",
            figure={'data': [go.Histogram(histfunc="count",x=datacar)],
                'layout': {'title': 'Répartition des métiers'}
                    }),
        style={'border' : '1px black solid','float':'left','width':'69%','height':'450px'}),


    html.Div(children=[
        html.Label('Choisissez un critère'),

        dcc.RadioItems(id='select_input',
            options=[
                    {'label': 'Sexe', 'value': 'gender'},
                    {'label': 'Travail', 'value': 'career_c'},
                     {'label': 'Age', 'value': 'age'},
                    ],className='select_categ',
             value='gender'),

        dcc.Graph(id='graph_output')
    ],
        style={'border' : '1px black solid','float':'left','width':'99%','height':'350px'}),
])

@app.callback(
    Output(component_id='graph_output', component_property='figure'),
    Input(component_id='select_input', component_property='value')
)
def get_data_table(option):
    val = decision.loc[:, option]
    fig = go.Figure(data=[go.Histogram(histfunc="avg",x=val,y=decision.iloc[:,0])])
    fig.update_layout(title_text='Pourcentage de oui reçus', title_x=0.5)
    return fig


# Programme Main
if __name__ == '__main__':
    print('Start')
    app.run_server() # démarrer l'application DASH