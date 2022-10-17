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
data = pd.read_csv('trainClean.csv',on_bad_lines="skip",delimiter=",")
print(data.info())

#graph répartition âge
datanew=data.loc[:,('iid','age')]
datanew=datanew.drop_duplicates()
dataage=datanew['age']

#graph répartition catégories travail
datanew=data.loc[:,('iid','career_c')]
datanew=datanew.drop_duplicates()
datacar=datanew['career_c']

#graphique décision
decision=data.loc[:,('dec_o','gender','age','career_c','income')]


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
                    {'label': 'Age', 'value': 'age'}
                    ],className='select_categ',
             value='gender'),

        dcc.Graph(id='graph_output')
    ],
        style={'border' : '1px black solid','float':'left','width':'99%','height':'600px'}),

    html.Div(children=[

        dcc.Dropdown(id='dropdown_input',
                    options=[{'label': 'Attractive', 'value': 'attr1_1'},
                    {'label': 'Sincere', 'value': 'sinc1_1'},
                    {'label': 'Intelligent', 'value': 'intel1_1'},
                    {'label': 'Fun', 'value': 'fun1_1'},
                    {'label': 'Ambitious', 'value': 'amb1_1'},
                    {'label': ' Has shared interests/hobbies', 'value': 'shar1_1'}],
                     value='attr1_1'),

        dcc.RadioItems(id='radio_input',
                       options=[
                           {'label': 'Sexe', 'value': 'gender'},
                           {'label': 'Age', 'value': 'age'}
                       ],
                       value='gender'),

        dcc.Graph(id='boxplot_output')
    ],
        style={'border' : '1px black solid','float':'left','width':'99%','height':'600px'})

])

@app.callback(
    Output(component_id='graph_output', component_property='figure'),
    Input(component_id='select_input', component_property='value'))
def get_data_table(option):
    val = decision.loc[:, option]
    fig = go.Figure(data=[go.Histogram(histfunc="avg",x=val,y=decision.iloc[:,0])])
    if (option=='gender'):
        fig.update_layout(title_text="Pourcentage de oui reçus selon le sexe", title_x=0.5)
    elif (option=='age'):
        fig.update_layout(title_text="Pourcentage de oui reçus selon l'âge", title_x=0.5)
    elif (option=='career_c'):
        fig.update_layout(title_text="Pourcentage de oui reçus selon le type de travail", title_x=0.5)

    return fig

@app.callback(
    Output(component_id='boxplot_output', component_property='figure'),
    Input(component_id='radio_input', component_property='value'),
    Input(component_id='dropdown_input', component_property='value'))
def make_box(abs,ord):
    x_abs=data.loc[:,abs]
    y_ord=data.loc[:,ord]
    fig = go.Figure(data=[go.Box(x=x_abs,y=y_ord)])
    if (abs=='gender'):
        fig.update_layout(title_text="Importance de critères selon le sexe", title_x=0.5)
    elif (abs=='age'):
        fig.update_layout(title_text="Importance de critères selon l'âge", title_x=0.5)
    return fig


# Programme Main
if __name__ == '__main__':
    print('Start')
    app.run_server() # démarrer l'application DASH