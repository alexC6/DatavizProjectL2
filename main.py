import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import requests as rq
import webbrowser as wb
from bs4 import BeautifulSoup as BSoup
from dash.dependencies import Input, Output

file = '~/Documents/Projets.git/dataviz/pokemon.csv'
df = pd.read_csv(file)

## Déclaration des variables globales
url = ''
gen = []

## Ajout des valeurs du dropdown sur les générations
for i in range (1, 7):
    gen.append({'label' : 'Génération ' + str(i), 'value' : i})

def list_pokemon_type(pType, pGen):
    list_type_gen = []
    df_gen = df[df.Gen == pGen]

    list_type_gen.append(df_gen[df_gen.Type1 == pType])

    return list_type_gen

## Création d'une liste des Pokémons
pokemons = df.Nom.unique()
pok = []

## Constitution de la liste des valeurs du dropdown sur les Pokémons
for i in pokemons:
    pok.append({'label' : str(i), 'value' : str(i)})

## Création d'une liste contenant les types
types = df.Type1.unique()
types_values = []

## Consitutions des valeurs des checkboxs sur les types
for i in types:
    types_values.append({'label' : i, 'value' : i})

## Fonction retournant le nombre de Pokémons par type pour une génération donnée
def count_types(pGen):
    list_num = []
    df_gen = df[df.Gen == pGen]
    nb_types_gen = df_gen['Type1'].value_counts()

    for i in types:
        if (i in nb_types_gen):
            list_num.append(nb_types_gen[i])
        else:
            list_num.append(0)
    
    return list_num

## Création d'un tuple pour les règles CSS globales
css = {
    'background' : '#FFFFFF',
    'text' : '#000000',
    'font' : 'arial'
}

app = dash.Dash()

app.layout = html.Div(
    ## Style global de la page
    style = {
        'backgroundColor' : css['background'],
        'font-family' : css['font']
    },
    children = [
        ## Titre
        html.H1(
            children = 'Projet DataViz',
            style = {
                'textAlign' : 'center',
                'color' : css['text']
            }
        ),
        ## Sous-titre
        html.H2(
            children = 'Quelques stats sur les Pokémon ...',
            style = {
                'textAlign' : 'center',
                'color' : css['text']
            }
        ),
        ## Crédits
        html.Div(
            children = 'Auteurs : Alexandre Coulais et Quentin Hourcadette',
            style = {
                'textAlign' : 'center',
                'color' : css['text']
            }
        ),
        ## Conteneur du graphique comparant les statistiques générales
        html.Div(
            style = {
                'display' : 'grid',
                'grid-template-columns' : '2fr 1fr',
                'grid-gap' : '10px',
                'height' : '500px',
                'padding' : '20px 0px 20px 0px'
            },
            children = [
                dcc.Graph(
                    id = 'stats'
                ),
                html.Div(
                    style = {
                        'display' : 'grid',
                        'grid-template-columns' : '1fr 2fr',
                        'grid-template-rows' : '50px 400px'
                    },
                    children = [
                        dcc.Checklist(
                            id = 'stats_types',
                            style = {
                                'grid-column' : '1',
                                'grid-row' : '1 / 3',
                                'display' : 'grid',
                                'grid-template-rows' : 'repeat(18, 1fr)',
                                'grid-columns-gap' : '20px',
                                'padding-left' : '40px'
                            },
                            options = types_values,
                            value = types
                        ),
                        dcc.RadioItems(
                            id = 'stats_att_def',
                            style = {
                                'grid-column' : '2',
                                'grid-row' : '1'
                            },
                            options = [
                                {'label': 'Attaque', 'value': 'Attaque'},
                                {'label': 'Défense', 'value': 'Defense'}
                            ],
                            value = 'Attaque'
                        ),
                        ## Conteneur de l'image affichant le Pokémon sélectionné et le bouton lien
                        html.Div(
                            style = {
                                'grid-column' : '2',
                                'grid-row' : '2',
                                'max-height' : '100%',
                                'max-width' : '80%',
                                'display' : 'grid',
                                'grid-template-rows' : '350px 50px'
                            },
                            children = [
                                html.Img(
                                    id = 'select_img',
                                    style = {
                                        'grid-row' : '1',
                                        'max-height' : '90%',
                                        'max-width' : '100%',
                                        'align-self' : 'center',
                                        'justify-self' : 'center'
                                    }
                                ),
                                html.Button(
                                    'Lien Poképédia',
                                    id = 'open_page',
                                    style = {'grid-row' : '2'}
                                )
                            ]
                        ),
                        html.P(id = 'out', style = {'display' : 'none'})
                    ]
                )
            ]
        ),
        ## Conteneur du graphique sur les types et générations avec le dropdown associé
        html.Div(
            style = {
                'display' : 'grid',
                'grid-template-columns' : '3fr 1fr',
                'grid-auto-rows' : '500px',
                'padding' : '20px 0px 20px 0px',
                'margin-right' : '20px'
            },
            children = [
                dcc.Graph(id = 'types_gen'),
                html.Div(
                    style = {
                        'width' : '80%',
                        'margin-top' : '7%',
                        'margin-left' : '6%'
                    },
                    children = [
                        dcc.Dropdown(
                            id = 'drop_gen',
                            options = gen,
                            value = [1, 2, 3, 4, 5, 6],
                            multi = True,
                            placeholder = "Selectionner une génération"
                        )
                    ]
                )
            ]
        ),
        ## Conteneur du comparateur de Pokémon
        html.Div(
            style = {
                'display' : 'grid',
                'grid-template-rows' : '100px 400px 100px',
                'margin' : '0px 40px 0px 40px'
            },
            children = [
                ## Conteneur des dropdown
                html.Div(
                    style = {
                        'display' : 'grid',
                        'grid-columns-template' : '50% 50%'
                    },
                    children = [
                        dcc.Dropdown(
                            id = 'pkm_cmp_1',
                            options = pok,
                            value = 'Pikachu',
                            multi = False,
                            placeholder = "Selectionner un Pokémon",
                            style = {
                                'grid-column' : '1',
                                'margin-right' : '20px'
                            }
                        ),
                        dcc.Dropdown(
                            id = 'pkm_cmp_2',
                            options = pok,
                            value = 'Raichu',
                            multi = False,
                            placeholder = "Selectionner un Pokémon",
                            style = {
                                'grid-column' : '2'
                            }
                        )
                    ]
                ),
                ## Conteneur des images
                html.Div(
                    style = {
                        'display' : 'grid',
                        'grid-columns-template' : '50% 50%'
                    },
                    children = [
                        html.Img(
                            id = 'img_cmp_1',
                            style = {
                                'grid-column' : '1',
                                'max-height' : '90%',
                                'max-width' : '100%',
                                'align-self' : 'center',
                                'justify-self' : 'center'
                            }
                        ),
                        html.Img(
                            id = 'img_cmp_2',
                            style = {
                                'grid-column' : '2',
                                'max-height' : '90%',
                                'max-width' : '100%',
                                'align-self' : 'center',
                                'justify-self' : 'center'
                            }
                        )
                    ]
                ),
                ## Conteneur des résultats
                html.Div(
                    style = {
                        'display' : 'grid',
                        'grid-columns-template' : '1fr 1fr',
                        'grid-columns-gap' : '20px'
                    },
                    children = [
                        html.P(id = 'cmp_1'),
                        html.P(id = 'cmp_2')
                    ]
                )
            ]
        )
    ]
)

## Génération du premier graphique
@app.callback(
    Output('stats', 'figure'),
    [Input('stats_types', 'value'),
    Input('stats_att_def', 'value')]
)
def update_stats(types, att_def):
    return {
        'data' : [
            ## Création pour chaque type d'un ensemble de points 
            go.Scatter(
                x = df[df['Type1'] == i][att_def],
                y = df[df['Type1'] == i]['SP ' + str(att_def)],
                text = df[df['Type1'] == i]['Nom'],
                mode = 'markers',
                marker = {
                    'size' : 10,
                    'line' : {'width' : 0.5, 'color' : 'white'}
                },
                name = i
            ) for i in types
        ],
        'layout' : go.Layout(
            xaxis = go.layout.XAxis(
                title = 'SP ' + str(att_def),
                range = [0, df[att_def].max() + 10]
            ),
            yaxis = go.layout.YAxis(
                title = att_def,
                range = [0, df['SP ' + str(att_def)].max() + 10]
            ),
            margin = {'l' : 40, 'b' : 40, 't' : 10, 'r' : 10},
            hovermode = 'closest'
        )
    }

@app.callback(
    Output('types_gen', 'figure'),
    [Input('drop_gen', 'value')]
)
def update_graph(drop_value):
    fig_types_gen = go.Figure()

    ## Génération du graphique affichant la quantité de Pokémons par type et générations
    for i in drop_value:
        fig_types_gen.add_trace(go.Scatter(
            x = types,
            y = count_types(i),
            name = 'Génération ' + str(i),
            text = types[i]
        ))

        fig_types_gen.update_traces(
            hoverinfo = 'name+x+y',
            line = {'width' : 0.5},
            marker = {'size' : 8},
            showlegend = True
        )

        fig_types_gen.update_layout(
            margin = {'l' : 40, 'b' : 40, 't' : 40, 'r' : 40},
            xaxis = go.layout.XAxis(
                autorange = True,
                range = [types[0], types[1]],
                rangeslider = dict(
                    autorange = True,
                    range = [types[0], types[1]]
                )
            )
        )

    return fig_types_gen

## Série de callback agissant sur l'image affiché dans le comparateur ainsi que le réultat de la comparaison
@app.callback(
    Output('select_img', 'src'),
    [Input('stats', 'clickData')])
def display_click_data(clickData):
    global url

    if clickData is None:
        url = 'https://www.pokepedia.fr/Pikachu'
    else:
        url = 'https://www.pokepedia.fr/' + str(clickData['points'][0]['text'])
    
    requete = rq.get(url)
    page = requete.content
    soup = BSoup(page, "lxml")
    recup = soup.find("a", {"class" : "image"}).contents[0]
    imgPage = 'https://www.pokepedia.fr/Fichier:' + str(recup.attrs['alt'])
    requete = rq.get(imgPage)
    page = requete.content
    soup = BSoup(page, "lxml")
    recup = soup.find("div", {"id" : "file"}).contents[0]
    imgURL = 'https://www.pokepedia.fr' + str(recup.attrs['href'])

    return imgURL

@app.callback(
    Output('out', 'title'),
    [Input('open_page', 'n_clicks')])
def on_click(id):
    wb.open(url)

@app.callback(
    Output('img_cmp_1', 'src'),
    [Input('pkm_cmp_1', 'value')])
def change_img_1(pPokemon):
    urlCmp = 'https://www.pokepedia.fr/' + str(pPokemon)
    requete = rq.get(urlCmp)
    page = requete.content
    soup = BSoup(page, "lxml")
    recup = soup.find("a", {"class" : "image"}).contents[0]
    imgPage = 'https://www.pokepedia.fr/Fichier:' + str(recup.attrs['alt'])
    requete = rq.get(imgPage)
    page = requete.content
    soup = BSoup(page, "lxml")
    recup = soup.find("div", {"id" : "file"}).contents[0]
    imgURL = 'https://www.pokepedia.fr' + str(recup.attrs['href'])

    return imgURL

@app.callback(
    Output('img_cmp_2', 'src'),
    [Input('pkm_cmp_2', 'value')])
def change_img_2(pPokemon):
    urlCmp = 'https://www.pokepedia.fr/' + str(pPokemon)
    requete = rq.get(urlCmp)
    page = requete.content
    soup = BSoup(page, "lxml")
    recup = soup.find("a", {"class" : "image"}).contents[0]
    imgPage = 'https://www.pokepedia.fr/Fichier:' + str(recup.attrs['alt'])
    requete = rq.get(imgPage)
    page = requete.content
    soup = BSoup(page, "lxml")
    recup = soup.find("div", {"id" : "file"}).contents[0]
    imgURL = 'https://www.pokepedia.fr' + str(recup.attrs['href'])

    return imgURL

@app.callback(
    Output('cmp_1', 'children'),
    [Input('pkm_cmp_1', 'value'),
    Input('pkm_cmp_2', 'value')])
def change_cmp_1(pPok1, pPok2):
    total1 = df[df.Nom == pPok1].Total.values[0]
    total2 = df[df.Nom == pPok2].Total.values[0]

    text = 'GAGNANT'

    if (total1 < total2):
       text = 'PERDANT'
    
    return text

@app.callback(
    Output('cmp_1', 'style'),
    [Input('pkm_cmp_1', 'value'),
    Input('pkm_cmp_2', 'value')])
def change_cmp_1(pPok1, pPok2):
    total1 = df[df.Nom == pPok1].Total.values[0]
    total2 = df[df.Nom == pPok2].Total.values[0]

    bckgnd = '#b7ffa4'
    color = '#26b300'

    if (total1 < total2):
        bckgnd = '#ff9090'
        color = '#b30000'

    style = {
        'display' : 'flex',
        'align-self' : 'center',
        'justify-self' : 'center',
        'justify-content' : 'center',
        'align-items' : 'center',
        'border-radius' : '10px',
        'height' : '75px',
        'width' : '200px',
        'background' : bckgnd,
        'color' : color,
        'grid-column' : '1',
        'font-size' : '20px',
        'font-weight' : 'bold'
    }
    
    return style

@app.callback(
    Output('cmp_2', 'children'),
    [Input('pkm_cmp_1', 'value'),
    Input('pkm_cmp_2', 'value')])
def change_cmp_1(pPok1, pPok2):
    total1 = df[df.Nom == pPok1].Total.values[0]
    total2 = df[df.Nom == pPok2].Total.values[0]

    text = 'GAGNANT'

    if (total1 > total2):
       text = 'PERDANT'
    
    return text

@app.callback(
    Output('cmp_2', 'style'),
    [Input('pkm_cmp_1', 'value'),
    Input('pkm_cmp_2', 'value')])
def change_cmp_1(pPok1, pPok2):
    total1 = df[df.Nom == pPok1].Total.values[0]
    total2 = df[df.Nom == pPok2].Total.values[0]

    bckgnd = '#b7ffa4'
    color = '#26b300'

    if (total1 > total2):
        bckgnd = '#ff9090'
        color = '#b30000'

    style = {
        'display' : 'flex',
        'align-self' : 'center',
        'justify-self' : 'center',
        'justify-content' : 'center',
        'align-items' : 'center',
        'border-radius' : '10px',
        'height' : '75px',
        'width' : '200px',
        'background' : bckgnd,
        'color' : color,
        'grid-column' : '2',
        'font-size' : '20px',
        'font-weight' : 'bold'
    }
    
    return style

if __name__ == '__main__' :
    app.run_server(debug = True)