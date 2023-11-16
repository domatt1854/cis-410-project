import praw
import secret
import pandas as pd

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=secret.client_id,
            client_secret=secret.client_secret,
            user_agent=secret.user_agent
        )
    

    def scrape_subreddit_submissions(self, subreddit: str, kind='hot', text_type ='submissions') -> pd.DataFrame:
        
        if kind not in ('hot', 'top', 'controversial', 'new'):
            raise Exception("kwarg 'kind' should be of: ['hot', 'top', 'controversial', 'new']")
    
        if text_type not in ('submissions', 'comments'):
            raise Exception("Kwarg 'text_type' should be of ['submissions', 'comments']")
    
        subreddit = self.reddit.subreddit(subreddit)
        
        if kind == 'hot':
            submissions = subreddit.hot()
        elif kind == 'controversial':
            submissions = subreddit.controversial()
        elif kind == 'top':
            submissions = subreddit.top()
        elif kind == 'new':
            submissions = subreddit.new()
        
        if text_type == 'submissions':
            return self.process_submissions(submissions)
        elif text_type == 'comments':
            return self.process_comments(submissions)
    
    
    ##################################
    ###### HELPER METHODS ############
    ##################################
    
    def process_submissions(self, submissions: praw.Reddit.submission) -> pd.DataFrame:
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
        
        return pd.DataFrame(
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
            
    
    def process_comments(self, submissions: praw.Reddit.submission) -> pd.DataFrame:
        
        body_markdown = []
        body_html = []
        comment_date = []
        ids = []
        comment_author = []
        comment_score = []
        
        for submission in submissions:
            for comment in submission.comments:
                body_markdown.append(comment.body)
                body_html.append(comment.body_html)
                comment_date.append(comment.created_utc)
                ids.append(comment.id)
                comment_author.append(comment.author)
                comment_score.append(comment.score)

        
        return pd.DataFrame(
            {
                'id': ids,
                'created_utc': comment_date,
                'body_markdown': body_markdown,
                'body_html': body_html,
                'author': comment_author,
                'score': comment_score
            }
        )


