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

For Windows Users: 
```
pip install -r requirements_windows.txt
```
For Mac Users
```
For Mac Users: pip install -r requirements_macos.txt
```

# Running the Application

To run the application, run the following command in your terminal

```
python app.py
```

This will launch your `Dash Plotly` Application, and can usually be accessed using the following localhost link: http://127.0.0.1:8050/

