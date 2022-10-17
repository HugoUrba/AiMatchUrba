## Bienvenue sur AI match by EasyDate :wave:

EsayDate est un site de rencontre qui organise des soirées "speed-dating". Leur objectif est de faire se rencontrer des personnes qui vont "matcher" mutuellement au terme du moins de rendez-vous possibles

## Prédictions de match 

**modèle de prédiction avec gradient boosting**

Nous avons commencé par nettoyer et explorer les données, notamment en utilisant la méthode des KNN voisins pour remplacer les valeurs manquantes. Nous avons vu qu'il y avait un fort déséquilibre entre les matchs et non-matchs, nous avons donc utilisé la méthode SMOTE pour rééquilibrer notre jeu de données, en créant des données fictive. Puis nous avons normalisé le jeu de données.
```python
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = SMOTE().fit_resample(X_train, y_train)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit(X_train)
X_train_scale = scaler.transform(X_train)
X_test_scale = scaler.transform(X_test
```
Notre fichier [Train Clean](https://github.com/MaartinShz/AIMatch/blob/18e84fa2920afdcc8fd0d708c88ad878a22c4793/data/df_clean.csv) est notre jeu de données nettoyé.
Nous avons ensuite testé et optimisé différents modèles de prédiction (AdaBoost, RandomForest, réseaux de neuronnes...), nous nous sommes tournés vers le modèle de prédiction Gradient boosting, et on commence par importer scikit-learn et on séparer nos données en apprentissage et test (70/30):
```python
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

XTrain,XTest,yTrain,yTest = train_test_split(X,y,train_size=0.7,stratify=df.match,random_state=0)

gb_clf = GradientBoostingClassifier(n_estimators=30, learning_rate=0.75, max_features=20, max_depth=20, random_state=0)
gb_clf.fit(XTrain, yTrain)
predictions = gb_clf.predict(XTest)
```
 Avec la méthode GridSearch, on teste les hyperparamètres qui nous donnent une meilleure précision et un meilleur f1 score.
 On se base sur les 25 variables ayant le plus d'importance parmi les 70 variables du fichier de données d'origine ([train.csv](https://github.com/MaartinShz/AIMatch/blob/819f0a26da7b63e36c98d91d741f59dd3cfef28b/data/train.csv). Dans le fichier .py modèle, vous retrouverez les lignes de code de ce modèle de prédiction type 'boîte noire'. Au terme de la procédure, on a isolé la colonne qui prédisait, selon notre modèle, si les deux personnes allaient match mutuellement, fichier qu'on a posté sur notre compétition Kaggle afin de voir la précision de notre modèle sur l'échantillon test. Cette colonne de prédiction se trouve dans le fichier [submission](https://github.com/MaartinShz/AIMatch/blob/c0175122d37296fb8fc2e4e106d2628ab0e58826/data/submissions.csv)

## Création de l'application Dash

**Création de l'application Dash**

Nous avons ensuite codé une application à l'aide de la librairie Dash. On a recodé les variables afin de rendre les graphiques plus lisibles et importer un jeu de données avec le plus de variables possibles (fichier utilisé: [Train Clean](https://github.com/MaartinShz/AIMatch/blob/18e84fa2920afdcc8fd0d708c88ad878a22c4793/data/train.csv)). Le but ici est de faire de la visualisation de données des utilisateurs et utilisatrices du site de rencontre. La première partie définit les règles stylistiques pour la page qui sera générée.
On a ensuite créé un menu, sous forme de barre verticale:
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
Notre app suit le modèle d'une SPA (Single page Application), une partie menu et une partie contenu, qui affichera les graphiques qui nous intéressent. Dans le layout, on mettra ce que notre page va afficher, après avoir défini notre application.
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
Ici par exemple le graphique affiché sera un boxplot, fait avec la commande go.Box. ensuite on pourra choisir entre le sexe, dans le if, ou l'âge, dans le elif, à afficher dans le graphique. Enfin on définit dans une callback ce qu'afficheront les différents menus, leurs titres et graphiques. On utilise ici aussi un branchement conditionnel selon le pathname de la page. Et on lance notre application Dash avec le programme Main. Le code de cette application est à retrouver dans le document [DashApp](https://github.com/MaartinShz/AIMatch/blob/96a92086651a3c1cf6d7df437d752cc6ca37c886/DashApp.py).

## Déploiement sous Heroku
 Pour déployer notre application nous avons utilisé heroku, qui héberge notre application gratuitement. En paramétrant l'application, nous choisissons qu'elle nous lise du python. On s'assure qu'elle fasse tourner la bonne version de python, ici la 3.9. Une fois paramétré correctement, on déploie manuellement notre explication avec Heroku, qui génère un lien avec notre application hébergée!

 ## Informations fichiers

Dans le répertoire data, on retrouve les bases de données qu'on a utilisé:

[La base de données initiale](https://github.com/MaartinShz/AIMatch/blob/0d9e8f2b394d4f50eab6a09209255c710708d09d/data/train.csv), sans aucune retouche

[La base de données nettoyée pour créer le modèle](https://github.com/MaartinShz/AIMatch/blob/0d9e8f2b394d4f50eab6a09209255c710708d09d/data/df_clean.csv)

[Notre colonne de prédictions](https://github.com/MaartinShz/AIMatch/blob/0d9e8f2b394d4f50eab6a09209255c710708d09d/data/submissions.csv), obtenue suite à l'utilisation de notre modèle.


Dans les fichiers restants on a:

[La base de données pour l'application](https://github.com/MaartinShz/AIMatch/blob/0d9e8f2b394d4f50eab6a09209255c710708d09d/data/trainClean.csv), légérement nettoyée mais avec plus de variable que pour le modèle.

[Le code de notre application Dash](https://github.com/MaartinShz/AIMatch/blob/fd414669af78d612238ebeaa35c52569d6c9fac3/DashApp.py)

[Le code de la recherche de modèles](https://github.com/MaartinShz/AIMatch/blob/59d320783bda7fd0a304b97bb3bc75e92816a47b/submission.ipynb)

[Ajout des librairies nécessaires](https://github.com/MaartinShz/AIMatch/blob/59d320783bda7fd0a304b97bb3bc75e92816a47b/requirements.txt)

[Lancer sous la version 3.9 de Python](https://github.com/MaartinShz/AIMatch/blob/59d320783bda7fd0a304b97bb3bc75e92816a47b/runtime.txt)

[Recodage des données pour l'application Dash](https://github.com/MaartinShz/AIMatch/blob/59d320783bda7fd0a304b97bb3bc75e92816a47b/modele.py)

[Fichier de configuration Heroku](https://github.com/MaartinShz/AIMatch/blob/59d320783bda7fd0a304b97bb3bc75e92816a47b/Procfile)

Dans le répertoire assets, on a les éléments visuels nécessaires à notre application
