# pandas : bibliothèque de manipulation et d'analyse des données
# dash : bibliothèque de création d'applications web interactives
# dcc (dash core components) : composants interactifs
# html : (dash html components) : balises HTML

import pandas as pd
from dash import Dash, dcc, html, Input, Output

# Lecture du fichier CSV et prétraitement des données
data = (
    pd.read_csv("avocado.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)
regions = data["region"].sort_values().unique()
avocado_types = data["type"].sort_values().unique()

# Initialisation de l'application Dash
app = Dash(__name__)
app.title = "Avocado Analytics: Understand Your Avocados!"

# Layout de l'application
app.layout = html.Div(
    children=[
        html.Div(
            children = [
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics",
                    className="header-title",
                ),
                html.P(
                    children=(
                        "Analyze the behavior of avocado prices and the number "
                        "of avocados sold in the US between 2015 and 2018."
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        
        # Filtres
        html.Div(
            children=[

                #Filtre par régions
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),

                #Filtre par type d'avocat
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": avocado_type.title(),
                                    "value": avocado_type,
                                }
                                for avocado_type in avocado_types
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),

                #Sélecteur de période (date de début et de fin)
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(),
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        
        # Graphiques
        html.Div(
        children=[

            # Graphique des prix moyens des avocats 
            html.Div(
                children=
                    dcc.Graph(
                    id="price-chart",
                    config={"displayModeBar": False},
                ),
                className="card",
            ),

            # Graphique du volume total des avocats vendus
            html.Div(
                children=
                    dcc.Graph(
                    id="volume-chart",
                    config={"displayModeBar": False},
                ),
                className="card",
            ),
        ],
        className="wrapper",
    ),

    html.Div(
        children=[
            html.H3(children = "Réalisé par un groupe d'étudiants de l'Université de Yaoundé I", className="texte"),
        ],
        className="footer",
    ),
    ]
)

#Ajout de l'interaction dans l'app via les callbacks

#Définitions des entrées et des sorties
@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)

def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure

# Exécution de l'application
if __name__ == "__main__":
    app.run_server(debug=True)
