
#########################################################################################################################
# import / dependances

#pip install -Iv dash-bootstrap-components==0.11.0

import dash
#import dash_core_components as dcc
#import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
#from dash import dbc


from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objs as go

from PIL import Image

#########################################################################################################################
# manipulation des données
# importation données
data = pd.read_csv('data/trainClean.csv',on_bad_lines="skip",delimiter=",")
#print(data.info())

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

################################

afficheimportance = Image.open("assets/affiche-importance-var.png")
logo = Image.open("assets/logo2.png")
logoEntreprise = Image.open("assets/logo.png")


#########################################################################################################################
# CSS / regle stylistique

#style des de la partie contenu des graph,etc...
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#style du menu
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

#########################################################################################################################
# Partie de l'App sur le modèle d'une App SPA ( Single page Application)
# Partie MENU
sidebar = html.Div(
    [
        html.Div(html.Img(src=logo,width='200',height='200',alt='logo'),style={'text-align':'center'}),
        html.Hr(),
        
        dbc.Nav([#liste des page du menu
            dbc.NavLink("Présentation des Profils", href="/PresentationdesProfils", active="exact"),html.Hr(),
            dbc.NavLink("Profil type", href="/ProfilType", active="exact"),html.Hr(),
            dbc.NavLink("Explication Modèle", href="/ExplicationModele", active="exact"),html.Hr(),
            ],vertical=True,pills=True,
        ),
   ],
   style=SIDEBAR_STYLE,
)

# Partie Contenu
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)# vide au chargement # rempli avec un callback

#########################################################################################################################
# DASH Application

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

#########################################################################################################################
# Echange de donnée de L'app / CallBack

#callback pour les graphes avec nos filtres
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

#########################################################################################################################
# callback permettant la navigation et le chargement des contenus dans la partie dédiée

@app.callback(
    Output("page-content", "children"),
   [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/": #page accueil
        return [
                html.Br(),
                html.H1('🎉 Bienvenue 🎉', style={'textAlign':'center'}),
                html.Br(),
                html.Div(html.Img(src=logoEntreprise,alt='logoEntreprise'),style={'text-align':'center'}),
                html.Br(),
                html.H2(" 💖💖💖 Ici commence l'Amour avec un Grand Ai 💖💖💖 ",className="alert alert-danger",style={'text-align':'center'})
                ]
###############################################################

    elif pathname == "/PresentationdesProfils": #page Presentation des données
        return [
                html.H1('Présentation des Profils',
                        style={'textAlign':'center'}),
                html.Div(dcc.Graph(id="pie_age",
                        figure={'data': [go.Pie(values=dataage.value_counts(),labels=('[23-27]','[28-32]','[18-22]','[33-37]','38+'))],
                            'layout': {'title': 'Répartition des âges'}
                                }),
                    style={'border-top':'1px solid','border-bottom':'1px solid','border-left':'1px solid','float':'left','width':'30%','height':'500px'}),

                html.Div(dcc.Graph(id="hist_metier",
                        figure={'data': [go.Histogram(histfunc="count",x=datacar)],
                            'layout': {'title': 'Répartition des métiers'}
                                }),
                    style={'border' : '1px black solid','float':'left','width':'69%','height':'500px'}),                   
                ]
###############################################################

    elif pathname == "/ProfilType": #page profil qui match le plus
        return [
                html.Div(children=[
                    html.Label('Choisissez un critère'),
                    dcc.RadioItems(id='select_input',
                        options=[ # filtres du graph
                                {'label': 'Sexe ', 'value': 'gender'},
                                {'label': 'Travail ', 'value': 'career_c'},
                                {'label': 'Age ', 'value': 'age'}
                                ],
                         value='gender'),

                    dcc.Graph(id='graph_output')
                ],style={'border-top':'1px solid','border-right':'1px solid','border-left':'1px solid','float':'left','width':'99%','height':'600px'}),
                
                html.Div(children=[
                    html.Label('Choisissez un critère'),
                    dcc.Dropdown(id='dropdown_input', # filtres du graph en liste déroulante
                                options=[{'label': 'Attractive', 'value': 'attr1_1'},
                                {'label': 'Sincere', 'value': 'sinc1_1'},
                                {'label': 'Intelligent', 'value': 'intel1_1'},
                                {'label': 'Fun', 'value': 'fun1_1'},
                                {'label': 'Ambitious', 'value': 'amb1_1'},
                                {'label': ' Has shared interests/hobbies', 'value': 'shar1_1'}],
                                 value='attr1_1',style={'width':'50%'}),

                    dcc.RadioItems(id='radio_input',
                                   options=[
                                       {'label': 'Sexe ', 'value': 'gender'},
                                       {'label': 'Age ', 'value': 'age'}
                                   ],
                                   value='gender'),
                    
                    dcc.Graph(id='boxplot_output')
                ],
                    style={'border' : '1px black solid','float':'left','width':'99%','height':'600px'}),html.Hr()
                
            
                ]
###############################################################

    elif pathname == "/ExplicationModele": #page pour expliquer la solution
        return [
            html.H1("Coefficients sur l’importance des variables de notre Modèle", style={'color' :'black','text-align':'center'}),
            html.H1('Gradient Boosting', style={'textAlign':'center'}),
            html.Div(html.Img(src=afficheimportance)),
            html.Br(),
            html.P("Les variables les plus importantes dans notre modèle sont : \n"),
            html.P(" pf_o_sin : la préférence déclarée du partenaire sur la sincérité \n "),
            html.P(" age_o : age du partenaire \n "),
            html.P(" int_corr : indice de correspondance des centres d'intérêt  \n"),
            html.Br(),
            html.H2(' Comprendre le boosting de gradient', style={'textAlign':'left'}),
            html.Br(),
            html.P("Le boosting de gradient est un type de boosting d’apprentissage de la machine. Il repose fortement sur la prédiction que le prochain modèle réduira les erreurs de prédiction lorsqu’il sera mélangé avec les précédents. L’idée principale est d’établir des résultats cibles pour ce prochain modèle afin de minimiser les erreurs. \n "),

            ]
    
###############################################################
# Si l'utilisateur essaye d'accéder à des pages différentes, retourne une erreur 404 

    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"La page {pathname} n'existe pas..."),
        ]
    )
    

#########################################################################################################################
# Programme Main

if __name__ == '__main__':
    app.run_server(debug=True, port=8050) # démarrer l'application DASH