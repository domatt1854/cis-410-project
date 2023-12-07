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
from nltk.probability import FreqDist
import numpy as np

nltk.download('stopwords')
warnings.filterwarnings('ignore', module='models')

scraper = RedditScraper()
sentiment_scorer = None
df = None

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    html.H1(children='Reddit Sentiment Analysis Dashboard', style={"margin": "10px"}),
    html.Div(children='Analyze the Sentiment of your Favorite Subreddit and more!', style={"margin": "10px"}),
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
    html.H3(id='subreddit_header_text', style={"margin": "10px"}, children="Please Select a SubReddit"),
    html.Div([
            dcc.Loading(
            id="loading_spinner",
            children=[html.Div([html.Div(id="loading-output-2")])],
            type="circle"
        )],
        style= {'margin': '50px'}
    ),
    html.Div([
        html.H4(id='wordcloud_header')
    ],
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center', 'margin': '20px'}
    ),
    html.Div([
        html.Img(id="wordcloud_positive")
    ],
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}
    ),
    html.H4(id='sentiment_pie_chart_header', style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center', 'margin': '20px'}),
    html.Div(id='sentiment_pie_chart_div',
        children=[
            html.Div(id="sentiment_pie_chart_graph")
    ],
    style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}),
    
    html.H4(id='stacked_sentiment_bar_chart_header', style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center', 'margin': '20px'}),
    html.Div(id='stacked_sentiment_bar_chart_time_div',
        children=[
            html.Div(id="stacked_sentiment_bar_chart_time_graph")
    ],
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}
    ),
    html.Div(
        id='boxplot_scores_ratio_div',
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center', 'margin': '15px', 'padding': '15px'}
    ),
    html.Div(
        id='freqdist_positive_bar_chart_div',
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center', 'margin': '15px', 'padding': '15px'}
    ),
    html.Div(
        id='freqdist_neutral_bar_chart_div',
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center', 'margin': '15px', 'padding': '15px'}
    ),
    html.Div(
        id='freqdist_negative_bar_chart_div',
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center', 'margin': '15px', 'padding': '15px'}
    )
    
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
    
    try:
        print('-' * 20)
        print(df.head())
        print('-' * 20)
        
        sentiment_scorer = Sentiment_Scorer(df, model_name)
        
        print("Loaded in Model {}!".format(model_name))
        
        df = sentiment_scorer.label_dataset()
        
        print('-' * 20)
        print(df.head())
        
        print('-' * 20)
        
        df['text'] = df['text'].apply(lambda x: sentiment_scorer.clean_text(x))
        df['tokens'] = df['text'].apply(lambda x: nltk.word_tokenize(x))
        
        print('-------------------------------------------- COLUMNS -----------------------------')
        print(df.columns)
        print('------------------------------------------------------------------------')
    
    except Exception as e:
        print("Error in loading model: {}".format(e))
        
    return 'Sentiment Analysis of Subreddit r/{}\'s {} posts using {}'.format(subreddit_name, topic_type, model_name), None

@callback(
    Output('wordcloud_positive', 'src'),
    Output('wordcloud_header', 'children'),
    Input('subreddit_header_text','children'),
    prevent_initial_call=True
)
def add_wordclouds(children):
    global df
    print("Entered WordCloud Generation Function")
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


@callback(
    Output('sentiment_pie_chart_div', 'children'),
    Output('sentiment_pie_chart_header', 'children'),
    Input('wordcloud_header','children'),
    prevent_initial_call=True
)
def add_sentiment_pie_chart(children):
    print("Time Series Chart Called")
    global df
    print(df.columns)
    print(df.head())
    return dcc.Graph(
        figure=px.pie(
            df['sentiment'].value_counts().reset_index(),
            values='count',
            names='sentiment',
            hole=.3,
            template='plotly_dark',
            title='Composition of Sentiment in this Subreddit by Posts')), \
        "Quick Overview of this Subreddit\'s Overall Sentiment"
        
@callback(
    Output('stacked_sentiment_bar_chart_time_div', 'children'),
    Output('stacked_sentiment_bar_chart_header', 'children'),
    Input('sentiment_pie_chart_div','children'),
    prevent_initial_call=True
)
def add_time_series_bar_chart(children):
    print("Time Series Chart Called")
    return dcc.Graph(
        figure=px.bar(df.groupby('date')['sentiment'].value_counts().reset_index(), 
                      x="date", 
                      y="count", 
                      color="sentiment",
                      template='plotly_dark',
                      title='Posts per Day Broken Down By Sentiment'
                    )
        ), \
        "How has the Sentiment of Posts Changed Over Time?\n(PS: You might need to zoom in based off subreddit)"

@callback(
    Output('boxplot_scores_ratio_div', 'children'),
    Input('stacked_sentiment_bar_chart_time_div','children'),
    prevent_initial_call=True
)
def add_boxplots_votes_ratios(children):
    return dcc.Graph(
        figure=px.strip(
            df, 
            x='sentiment', 
            y='score',
            template='plotly_dark',
            title='Density of Posts - Scores vs Sentiment',
            width=500,
            height=400
        )
    ), \
    dcc.Graph(
        figure=px.strip(
            df, 
            x='sentiment', 
            y='upvote_ratio',
            template='plotly_dark',
            title='Density of Posts - Upvote Ratio vs Sentiment',
            width=500,
            height=400
        )
    )

    # Output('freqdist_neutral_bar_chart_div', 'children'),
    # Output('freqdist_negative_bar_chart_div', 'children'),
    
@callback(
    Output('freqdist_positive_bar_chart_div', 'children'),
    Input('boxplot_scores_ratio_div','children'),
    prevent_initial_call=True
)
def add_freqdist_bar_plot_pos(children):
    
    tokens_positive = df[df['sentiment'] == 'Positive']['tokens'].dropna().reset_index(drop=True) 
    fdist_pos = FreqDist(np.concatenate(tokens_positive))

    df_pos_fdist = pd.DataFrame(list(fdist_pos.items()), columns=['Word', 'Count']).sort_values(by='Count', ascending=False).head(10)

    
    print(df_pos_fdist.head())

    return dcc.Graph(
        figure=px.bar(
            df_pos_fdist,
            x='Word',
            y='Count',
            title='Most Commonly Used Words in Positive Posts',
            template='plotly_dark'
        )
    )
    
@callback(
    Output('freqdist_neutral_bar_chart_div', 'children'),
    Input('boxplot_scores_ratio_div','children'),
    prevent_initial_call=True
)
def add_freqdist_bar_plot_neu(children):
    tokens_neutral = df[df['sentiment'] == 'Neutral']['tokens'].dropna().reset_index(drop=True)
    if tokens_neutral.empty:
        return None
    
    fdist_neu = FreqDist(np.concatenate(tokens_neutral))
    df_neu_fdist = pd.DataFrame(list(fdist_neu.items()), columns=['Word', 'Count']).sort_values(by='Count', ascending=False).head(10)
    return dcc.Graph(
                figure=px.bar(
                    df_neu_fdist,
                    x='Word',
                    y='Count',
                    title='Most Commonly Used Words in Neutral Posts',
                    template='plotly_dark'
                )
            )
    

@callback(
    Output('freqdist_negative_bar_chart_div', 'children'),
    Input('boxplot_scores_ratio_div','children'),
    prevent_initial_call=True
)
def add_freqdist_bar_plot_neg(children):
    tokens_negative = df[df['sentiment'] == 'Negative']['tokens'].dropna().reset_index(drop=True)
    if tokens_negative.empty:
        return None
    
    fdist_neg = FreqDist(np.concatenate(tokens_negative))
    df_neg_fdist = pd.DataFrame(list(fdist_neg.items()), columns=['Word', 'Count']).sort_values(by='Count', ascending=False).head(10)
    
    return dcc.Graph(
                figure=px.bar(
                    df_neg_fdist,
                    x='Word',
                    y='Count',
                    title='Most Commonly Used Words in Negative Posts',
                    template='plotly_dark'
                )
            )
    
    
if __name__ == '__main__':
    app.run(debug=True)
    