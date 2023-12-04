from dash import Dash, html, dcc, Input, Output, callback
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

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Reddit Sentiment Analysis Dashboard', style={"margin": "10px"}),
    html.Div(children='Analyze the Sentiment of your Favorite Subreddit and more!', style={"margin": "10px"}),

    dcc.Input(
        id='input_subreddit',
        placeholder="Enter a Subreddit here.",
        style={"margin": "10px"}
    ),
    
    dcc.Dropdown(
        ['VADER','KNN','Decision Tree','Random Forest','Logisistic Regression','SGD'],
        'VADER',
        id='dropdown_sentiment_model_name',
        style= {"margin": "5px"}
    ),
    
    html.Div(id='sentiment_drop_down_text', style={"margin": "10px"}),
    html.H2(id='subreddit_header_text', style={"margin": "10px"})
    
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])

@callback(
    Output(component_id='subreddit_header_text', component_property='children'),
    Input(component_id='input_subreddit', component_property='value')
)
def update_subreddit(input_subreddit):
    if not input_subreddit:
        return ""
    return "Analysis of /r/{}".format(input_subreddit)


@callback(
    Output(component_id='sentiment_drop_down_text', component_property='children'),
    Input(component_id='dropdown_sentiment_model_name', component_property='value')
)
def update_model(dropdown_value):
    return "You have selected {}".format(dropdown_value)

if __name__ == '__main__':
    app.run(debug=True)
    