# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 22:28:15 2022

@author: Maartin
"""
#########################################################################################################################
# import / dependances
#pip install -Iv dash-bootstrap-components==0.11.0

import dash
import dash_core_components as dcc
import dash_html_components as html
#from dash import html
#from dash import dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objs as go



# importation données
data = pd.read_csv('trainClean.csv',on_bad_lines="skip",delimiter=",")
#print(data.info())

#graphique décision
decision=data.loc[:,('dec_o','gender','age','career_c')]

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
sidebar = html.Div(
    [
        html.H1("Match Ai App", style={'color' :'red','text-align':'center'}),
        html.H2("Menu", className="display-4"),
        html.Hr(),
        
        dbc.Nav([
            dbc.NavLink("Statistiques Descriptives", href="/", active="exact"),html.Hr(),
            dbc.NavLink("Profil type", href="/page-1", active="exact"),html.Hr(),
            dbc.NavLink("Explication Modèle", href="/page-2", active="exact"),html.Hr(),
            ],vertical=True,pills=True,
        ),
   ],
   style=SIDEBAR_STYLE,
)
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

#########################################################################################################################
# DASH Application

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
   [Input("url", "pathname")]
)

def render_page_content(pathname):
    #val = decision.loc[:, option]
    #fig = go.Figure(data=[go.Histogram(histfunc="avg",x=val,y=decision.iloc[:,0])])
    #fig.update_layout(title_text='Pourcentage de oui reçus', title_x=0.5)
    #return fig
    
    if pathname == "/":
        return [
                html.H1('Statistiques Descriptives',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(data, barmode='group', x='dec_o',
                         y=['gender']))
                ]
    elif pathname == "/page-1":
        return [
                html.H1('Profil type',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(data, barmode='group', x='age',
                         y=['gender']))
                ]
    elif pathname == "/page-2":
        return [
                html.H1('Explication Modèle',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(data, barmode='group', x='career_c',
                         y=['gender']))
                ]
    # If the user tries to reach a different page, return a 404 message
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
    print('Start')
    app.run_server(debug=False, port=8050) # démarrer l'application DASH