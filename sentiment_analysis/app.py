from dash import Dash, html, dcc, Input, Output, callback,State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from reddit_scraper import RedditScraper
from models import Sentiment_Scorer
import warnings

warnings.filterwarnings('ignore', module='models')

global df
global scraper
global sentiment_scorer

scraper = RedditScraper()
sentiment_scorer = None
df = None

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Reddit Sentiment Analysis Dashboard', style={"margin": "10px"}),
    html.Div(children='Analyze the Sentiment of your Favorite Subreddit and more!', style={"margin": "10px"}),

    # dcc.Input(
    #     id='input_subreddit',
    #     placeholder="Enter a Subreddit here.",
    #     type='text',
    #     style={"margin": "10px"}
    # ),
    
    
    # dcc.Dropdown(
    #     ['K Nearest Neighbors', 'Decision Tree', 'Random Forest', 'Logistic Regression', 'SGD Classifier', 'Hard Voting Classifier', 'Soft Voting Classifier'],
    #     'K Nearest Neighbors',
    #     id='dropdown_sentiment_model_name',
    #     style= {"margin": "5px", }
    # ),
    html.Div([
        dcc.Input(
            id='input_subreddit',
            placeholder="Enter a Subreddit here.",
            type='text',
            style={"margin": "10px", "width": "95%", "font-size": "20px"}
        ),
        html.Div(children='Select a Model to Use', style={"margin": "10px"}),
        dcc.Dropdown(
            ['K Nearest Neighbors', 'Decision Tree', 'Random Forest', 'Logistic Regression', 'SGD Classifier', 'Hard Voting Classifier', 'Soft Voting Classifier'],
            'K Nearest Neighbors',
            id='dropdown_sentiment_model_name',
            style= {"margin": "5px" }
        ),
        html.Div(children='Select The Kind of Posts to Analyze', style={"margin": "10px"}),
        dcc.Dropdown(
            ['Hot', 'Top', 'New', 'Controversial'],
            'Hot',
            id='dropdown_submission_type',
            style= {"margin": "5px" }
        ),
        ],
        style={"width": "50%"}
    ),
    html.Button('Submit', id='submit-val', style={"margin": "10px", "font-size": "15px", "background-color": "gray"}),
    
    html.Div(id='sentiment_drop_down_text', style={"margin": "10px"}),
    html.H2(id='subreddit_header_text', style={"margin": "10px"}),
    dcc.Loading(
                    id="loading_spinner",
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="circle",
    )
    
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])

@callback(
    Output(component_id='subreddit_header_text',component_property='children'),
    Output(component_id='loading_spinner', component_property="children"),
    Input(component_id='submit-val',component_property='n_clicks'),
    State(component_id='dropdown_submission_type',component_property='value'),
    State(component_id='dropdown_sentiment_model_name', component_property='value'),
    State(component_id='input_subreddit',component_property='value')
)
def performAnalysis(n_clicks, topic_type, model_name, subreddit_name):
    if not subreddit_name:
        print("Subreddit is Null: {}".format(subreddit_name))
        return "Please Select a SubReddit"
    
    print("Scraping {} Submissions for Subreddit: {}".format(topic_type, subreddit_name))
    try:
        df = scraper.scrape_subreddit_submissions(subreddit_name, kind=topic_type)
    except:
        return "Subreddit {} was not found!".format(subreddit_name)
    
    print(df.head())
    sentiment_scorer = Sentiment_Scorer(df, model_name)
    print("Loaded in Model {}!".format(model_name))
    
    return 'Performing Analysis on "{}" using {}'.format(subreddit_name, model_name), None

if __name__ == '__main__':
    app.run(debug=True)
    