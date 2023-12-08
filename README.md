# CIS 410 - Group Project: Reddit Sentiment Analysis Dashboard

**Group Name** - Grade Simps

**Team Members** - Gautum Samudrala, Ansh Bhalla, Yiting Zhao, Matthew Do

**Captain** - Matthew Do

# Table of Contents

1. [Getting Started](#introduction)
2. [Web Application Architecture](#architecture)
3. [Challenges](#challenges)

<a name="introduction"></a>
# Getting Started 

Welcome to our CIS 410 Group project! Over the last few months, we have worked diligently on building an application to provide users with useful metrics and visualizations of their favorite subreddit. Follow the steps below to run the application locally on your computer.

## Signing up for Credentials to Authenticate to Reddit API

Our dashboard requires access to the Reddit API. Before you can run this program, you must create a `Reddit Application`

1. Click on this link to begin: [Reddit Application Creation](https://www.reddit.com/prefs/apps)
2. Login in to your Reddit account, if not already logged in
3. Select `are you a developer? create an app...`
4. You will be prompted to fill in a couple of fields, which will be discussed in the next steps

![Create Application Page](images/create_application_page.png)

5. Fill in the field for `name` (can be anything)
6. Select `web app`
7. Fill in the field for `description` (can be anything) 
8. Fill in the fields for `about url` and `redirect url` (can be anything). If any error occurs, ensure 'https://' is at the beginning of your link.
9. Select `Create App`
10. You will see the following page

![Reddit Developer Application](images/reddit_developer_application.png)

11. Based on the above image, save your `CLIENT_ID` and `CLIENT_SECRET`
12. Navigate to the `secret.py` module
13. Substitute in the respective values for `CLIENT_ID`and `CLIENT_SECRET`. The value for `USER_AGENT` can be any value you desire
14. Save secret.py


## Installing Dependencies

To install dependencies required to run all notebooks and applications, run the script in your terminal where `requirements.txt` is located.

```
pip install -r requirements.txt
```

## Running the Application

To run the application, run the following command in your terminal

```
python app.py
```

This will launch your `Dash Plotly` Application, and can usually be accessed using the following localhost link: http://127.0.0.1:8050/

<a name="architecture"></a>
# Web Application Architecture 

![Web Application Architecture](images/web_application_diagram.png)

## Components

### Python Reddit API Wrapper(PRAW)

The Python Reddit API Wrapper allows our application to fetch posts from a specified subreddit. We then run some functions that clean the text data.

### Scikit-Learn NLTK

We pickled our models and encapsulated them in `models.py` and took an Object-Oriented approach to allow for easy use in our web application. These components are responsible for classifying and pre-processing text data.

### Dash Plotly

This is the front-end of our application. It is responsible for integrating our modules for analyzing sentiment and passing the data fetched from the Reddit API.


<a name="challenges"></a>
# Challenges

## Code Optimization

### Reddit API Limitations

Fetching posts is limited to 100 posts per call. For each batch of 100 posts, there is a delay of about 1 second. After testing with different amounts of posts, we discovered that about 300 posts offers the best balance between application performance and analytic utility. 

### Text Pre-Processing

TODO: Add what we did to optimize performance on ML Algos