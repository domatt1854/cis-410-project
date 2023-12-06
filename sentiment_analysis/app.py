from dash import Dash, html, dcc, Input, Output, callback,State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from reddit_scraper import RedditScraper
from models import Sentiment_Scorer
import warnings
from io import BytesIO
from wordcloud import WordCloud
import base64
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

warnings.filterwarnings('ignore', module='models')

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
    html.Button('Submit', id='submit-val', style={"margin": "10px", "font-size": "15px", "background-color": "gray"}, n_clicks=0),
    
    html.Div(id='sentiment_drop_down_text', style={"margin": "10px"}),
    html.H2(id='subreddit_header_text', style={"margin": "10px"}, children="Please Select a SubReddit"),
    html.Div([
            dcc.Loading(
            id="loading_spinner",
            children=[html.Div([html.Div(id="loading-output-2")])],
            type="circle"
        )],
        style= {'margin': '50px'}
    ),
    html.Div([
        html.H4(id='wordcloud_header', style={"margin": "10px"})
    ],
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}
    ),
    html.Div([
        html.Img(id="wordcloud_positive"),
        # html.Img(id="wordcloud_neutral"),
        # html.Img(id="wordcloud_negative")
    ],
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}
    )
    
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])


# update_drop_menus
    # This function handles the fetching of Reddit Submissions
    # The Loading of the Model and Labeling the Dataset with Sentiments
    
# This function initiates other callbacks by updating the component `subreddit_header_text`:
    # add_wordclouds
@callback(
    Output(component_id='subreddit_header_text',component_property='children'),
    Output(component_id='loading_spinner', component_property="children"),
    Input(component_id='submit-val',component_property='n_clicks'),
    State(component_id='dropdown_submission_type',component_property='value'),
    State(component_id='dropdown_sentiment_model_name', component_property='value'),
    State(component_id='input_subreddit',component_property='value'),
    prevent_initial_call=True
)
def update_dropdown_menus(n_clicks, topic_type, model_name, subreddit_name):
    global df
    global sentiment_scorer
    
    if not subreddit_name:
        print("Subreddit is Null: {}".format(subreddit_name))
        return "Please Select a SubReddit"
    
    print("Scraping {} Submissions for Subreddit: {}".format(topic_type, subreddit_name))
    
    try:
        df = scraper.scrape_subreddit_submissions(subreddit_name, kind=topic_type)
    except:
        return "Subreddit {} was not found!".format(subreddit_name)
    
    print('-' * 20)
    print(df.head())
    print('-' * 20)
    sentiment_scorer = Sentiment_Scorer(df, model_name)
    print("Loaded in Model {}!".format(model_name))
    df = sentiment_scorer.label_dataset()
    print('-' * 20)
    print(df.head())
    print('-' * 20)
    return 'Performing Analysis on "{}" using {}'.format(subreddit_name, model_name), None

@callback(
    Output('wordcloud_positive', 'src'),
    Output('wordcloud_header', 'children'),
    Input('subreddit_header_text','children'),
    prevent_initial_call=True
)
def add_wordclouds(children):
    print("Entered WordCloud Generation Function")
    print(df.head())
    try:
        img = BytesIO()
        vocab = df.dropna()['text'].str.replace(r'\?|\.|\'', ' ')
        #print("vocab: {}".format(vocab))
        vocab = ' '.join(vocab)
        # print("vocab: {}".format(vocab))
        # vocab = ' '.join([i for i in vocab.split(' ') if i not in stopwords.words('english')])
        # print("vocab: {}".format(vocab))
        print("Done Formatting Vocab")
        wordcloud_positive = WordCloud(background_color='black', width=600, height=360).generate(vocab)
        print("Done Creating Wordcloud Obj")
        wordcloud_positive.to_image().save(img, format='PNG')
        
        print("Wordcloud Done")
    except Exception as e:
        print(e)
    
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode()), "Most Commonly-Used Words In This Subreddit"

if __name__ == '__main__':
    app.run(debug=True)
    