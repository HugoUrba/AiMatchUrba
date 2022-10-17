## Bienvenue sur AI match :wave:

AI Match est un site de rencontre qui organise des soirées "speed-dating". Leur objectif est de faire se rencontrer des personnes qui vont "matcher" mutuellement au terme du moins de rendez-vous possibles

## Prédictions de match 

**modèle de prédiction avec gradient boosting**

Nous avons commencé par nettoyer et explorer les données, notamment en utilisant la méthode des KNN voisins pour remplacer les valeurs manquantes. Notre fichier df_clean.csv est notre jeu de données nettoyé.
Nous avons ensuite testé et optimisé différents modèles de prédiction (AdaBoost, RandomForest, réseaux de neuronnes...), nous nous sommes tournés vers le modèle de prédiction Gradient boosting, et on commence par importer sci-kit learn et on séparer nos données en apprentissage et test (70/30):
```python
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

XTrain,XTest,yTrain,yTest = train_test_split(X,y,train_size=0.7,stratify=df.match,random_state=0)

gb_clf = GradientBoostingClassifier(n_estimators=30, learning_rate=0.75, max_features=20, max_depth=20, random_state=0)
gb_clf.fit(XTrain, yTrain)
predictions = gb_clf.predict(XTest)
```
 Avec une boucle for, on teste les hyperparamètres qui nous donnent une meilleure précision et un meilleur f1 score.
 On se base sur les 25 variables ayant le plus d'importance parmi les 70 variables du fichier de données d'origine ([train.csv](https://github.com/MaartinShz/AIMatch/blob/819f0a26da7b63e36c98d91d741f59dd3cfef28b/data/train.csv). Dans le fichier .py modèle, vous retrouverez les lignes de code de ce modèle de prédiction type 'boîte noire'. Au terme de la procédure, on a isolé la colonne qui prédisait, selon notre modèle, si les deux personnes allaient match mutuellement, fichier qu'on a posté sur notre compétition Kaggle afin de voir la précision de notre modèle sur l'échantillon test. Cette colonne de prédiction se trouve dans le fichier [submission](https://github.com/MaartinShz/AIMatch/blob/c0175122d37296fb8fc2e4e106d2628ab0e58826/data/submissions.csv)

## Déploiement de l'application Dash

**Création de l'application Dash**

Nous avons ensuite codé une application à l'aide de la librairie Dash. On a recodé les variables afin de rendre les graphiques plus lisibles et importer un jeu de données avec le plus de variables possibles. Le but ici est de faire de la visualisation de données des utilisateurs et utilisatrices du site de rencontre. La première partie définit les règles stylistiques pour la page qui sera générée.
On a ensuite créé un menu, sous forme de barre horizontale:
```python
sidebar = html.Div(
    [
        html.Div(html.Img(src=logo,width='200',height='200',alt='logo'),style={'text-align':'center'}),
        html.Hr(),
        
        dbc.Nav([
            dbc.NavLink("Présentation des Profils", href="/PresentationdesProfils", active="exact"),html.Hr(),
            dbc.NavLink("Profil type", href="/ProfilType", active="exact"),html.Hr(),
            dbc.NavLink("Explication Modèle", href="/ExplicationModele", active="exact"),html.Hr(),
            ],vertical=True,pills=True,
        ),
   ],
   style=SIDEBAR_STYLE,
)
```
Notre app va être "séparée" en deux, une partie menu qu'on vient de coder et une partie contenu, qui affichera les graphiques qui nous intéressent. Dans le layout, on mettra ce que notre page va afficher, après avoir défini notre application.
```python
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])
```
On aura donc bien une application avec une page en url, avec dans cette page, notre menu ("sidebar") et notre contenu ("content").

Afin d'avoir des graphiques plus dynamiques, on se sert de branchements conditionnels dans nos callbacks afin de définir des variables que l'utilisateur pourra sélectionner afin de modifier les graphiques affichés par l'appli:
```python
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
```
Ici par exemple le graphique affiché sera un boxplot, fait avec la commande go.Box. ensuite on pourra choisir entre le sexe, dans le if, ou l'âge, dans le elif, à afficher dans le graphique. Enfin on définit dans une callback ce qu'afficheront les différents menus, leurs titres et graphiques. On utilise ici aussi un branchement conditionnel selon le pathname de la page. Et on lance notre application Dash avec le programme Main. Le code de cette application est à retrouver dans le document [DashApp](https://github.com/MaartinShz/AIMatch/blob/96a92086651a3c1cf6d7df437d752cc6ca37c886/DashApp.py)
