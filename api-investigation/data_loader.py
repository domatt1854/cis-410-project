import praw
# temporary credentials file for local development
import secret
import pandas as pd
import sys


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Fail to provide the subreddit keywords")
        sys.exit(1)

    keywords = []
    for i in range(1, len(sys.argv)):
        keywords.append(sys.argv[i])

    # This authentication provides read-only Reddit instances to the API
    # To get credentials, need to make a bot here: https://www.reddit.com/prefs/apps/
    # PRAW Documentation https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#read-only-reddit-instances
    reddit = praw.Reddit(
        client_id=secret.client_id,
        client_secret=secret.client_secret,
        user_agent=secret.user_agent
        )
    
    for keyword in keywords:
        submissions = reddit.subreddit(keyword).hot(limit=500)
        # one for posts
        text = []
        author = []
        date = []
        title = []
        score = []
        upvote_ratio = []
        url = []
        num_comments = []
        
        for submission in submissions:
            text.append(submission.selftext)
            date.append(submission.created_utc)
            author.append(submission.author)
            score.append(submission.score)
            upvote_ratio.append(submission.upvote_ratio)
            title.append(submission.title)
            url.append(submission.url)
            num_comments.append(submission.num_comments)
    
        submissions_df = pd.DataFrame(
            {
                'created_utc': date,
                'title': title,
                'text': text,
                'author': author,
                'score': score,
                'upvote_ratio': upvote_ratio,
                'num_comments': num_comments,
                'url': url
            }
        )

        submissions_df.to_csv('data/{}_hot_posts.csv'.format(keyword))