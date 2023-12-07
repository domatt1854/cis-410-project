# CIS 410 - Group Project: Reddit Sentiment Analysis DashBoard

**Group Name** - Grade Simps

**Team Members** - Gautum Samudrala, Ansh Bhalla, Yiting Zhao, Matthew Do

**Captain** - Matthew Do

# Getting Started

### Signing up for Credentials to Authenticate to Reddit API

Our dashboard requires access to the Reddit API. 

Before you can run this program, you must create a `Reddit Application` using this link [here](https://www.reddit.com/prefs/apps).

After creating your application, navigate to the `secret.py` module and substitute in the values for `CLIENT_SECRET` and `CLIENT_ID`.

![Reddit Developer Application](images/reddit_developer_application.png)

The `USER_AGENT` can be any value you desire.

### Installing Dependencies

To install dependencies required to run all notebooks and applications, run the script in your terminal where `requirements.txt` is located.

```
pip install -r requirements.txt
```

# Running the Application

To run the application, run the following command in your terminal

```
python app.py
```

This will launch your `Dash Plotly` Application, and can usually be accessed using the following localhost link: http://127.0.0.1:8050/

# Web Application Architecture

![Web Application Architecture](images/web_application_diagram.png)

## Components

### Python Reddit API Wrapper(PRAW)

The Python Reddit API Wrapper allows our application to fetch posts from a specified subreddit. We then run some functions that clean the text data.

### Scikit-Learn NLTK

We pickled our models and encapsulated them in `models.py` and took an Object-Oriented approach to allow for easy use in our web application. These components are responsible for classifying and pre-processing text data.

### Dash Plotly

This is the front-end of our application. It is responsible for integrating our modules for analyzing sentiment and passing the data fetched from the Reddit API.