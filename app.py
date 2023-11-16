from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

MARGIN_10 = {"margin": "10px"}

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Reddit Sentiment Analysis Dashboard', style=MARGIN_10),
    html.Div(children='Analyze the Sentiment of your Favorite Subreddit and more!', style=MARGIN_10),

    dcc.Input(
        id='input_subreddit',
        placeholder="Enter a Subreddit here.",
        style=MARGIN_10
    ),
    
    dcc.Dropdown(
        ['VADER'],
        'VADER',
        id='dropdown_sentiment_model_name'
    ),
    
    html.Div(id='sentiment_drop_down', style=MARGIN_10)
    
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])

if __name__ == '__main__':
    app.run(debug=True)