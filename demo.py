#import pandas and numpy
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Import all modules 
import dash
from dash import dcc, html
from flask import Flask
import dash_bootstrap_components as dbc


# Initiate the App
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP])


# Read the files
df = pd.read_csv('count.csv')
df1 = pd.read_csv('data.csv')


# Build the components
Header_component = html.H1("Traffic Analysis Dashboard", style={'color':'darkcyan','text-align': 'center', 'font-size':'72px' })

# Visual Components

# Component1
countfig = go.FigureWidget()

countfig.add_scatter(name = "bus", x = df["Time"], y = df["bus"], fill ="tonexty", line_shape = 'spline')
countfig.add_scatter(name = "car", x = df["Time"], y = df["car"], fill ="tonexty", line_shape = 'spline')

countfig.update_layout(title = "Vehicle Time Line")

# Component 2
countfig_cum = go.FigureWidget()

countfig_cum.add_scatter(name = "bus", x = df["Time"], y = df["bus"].cumsum(), fill ="tonexty", line_shape = 'spline')
countfig_cum.add_scatter(name = "car", x = df["Time"], y = df["car"].cumsum(), fill ="tonexty", line_shape = 'spline')

countfig_cum.update_layout(title = "Cummulative Traffic")

 # Component 3 
indicator = go.FigureWidget(
    go.Indicator(
        mode = "gauge+number",
        value = df['car'].mean(),
        title = {'text':'Speed km/h'},
    )
 )
indicator.update_layout(title = "Average Car Speed")

#Component4
indicator1 = go.FigureWidget(
    go.Indicator(
        mode = "gauge+number",
        value = df['bus'].mean(),
        title = {'text':'Speed km/h'},
        gauge = {'bar':{'color':'cyan'}}
    )
 )


indicator1.update_layout(title = "Average Bus Speed")
#Component5
piefig = go.FigureWidget(
    px.pie(
    labels =["car", "bus"],
    values = [df['car'].sum(),df['bus'].sum()],
    hole = 0.5
    )
)
piefig.update_layout(title = "Traffic Distribution")



#Design the app layout
app.layout = html.Div(
    [
        dbc.Row([
            Header_component
        ]),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure = countfig)]
            ), dbc.Col(
                [dcc.Graph(figure = countfig_cum)]
            )]
        ),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure = indicator)]
            ), dbc.Col(
                [dcc.Graph(figure = indicator1)]
            ), dbc.Col(
                [dcc.Graph(figure = piefig)]
            ) ]
        )
    ]
)

# Run the App
app.run_server(debug=True)

