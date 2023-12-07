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
    

    def scrape_subreddit_submissions(self, subreddit: str, kind='Hot', text_type ='submissions', limit=300) -> pd.DataFrame:
        
        if kind not in ('Hot', 'Top', 'Controversial', 'New'):
            raise Exception("kwarg 'kind' should be of: ['hot', 'top', 'controversial', 'new']")
    
        kind = kind.lower()
        
        if text_type not in ('submissions', 'comments'):
            raise Exception("Kwarg 'text_type' should be of ['submissions', 'comments']")
    
        subreddit = self.reddit.subreddit(subreddit)
        
        if kind == 'hot':
            submissions = subreddit.hot(limit=limit)
        elif kind == 'controversial':
            submissions = subreddit.controversial(limit=limit)
        elif kind == 'top':
            submissions = subreddit.top(limit=limit)
        elif kind == 'new':
            submissions = subreddit.new(limit=limit)
        
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
        id = []

        for submission in submissions:
            
            # pretty crude way of handling exceptions but it will do for now
            try:
                text.append(submission.selftext)
            except Exception:
                text.append(None)
            try:
                date.append(submission.created_utc)
            except Exception:
                date.append(None)
            try:
                author.append(submission.author)
            except Exception:
                author.append(None)
            try:
                score.append(submission.score)
            except Exception:
                score.append(None)
            try:
                upvote_ratio.append(submission.upvote_ratio)
            except Exception:
                upvote_ratio.append(None)
            try:
                title.append(submission.title)
            except Exception:
                title.append(None)
            try:
                url.append(submission.url)
            except Exception:
                url.append(None)
            try:
                num_comments.append(submission.num_comments)
            except Exception:
                num_comments.append(None)
            
            try:
                id.append(submission.id)
            except Exception:
                id.append(None)
                
        df = pd.DataFrame(
            {
                'id': id,
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
        
        df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')           
        df['date'] = pd.to_datetime(df['created_utc']).dt.date
        
        return df.dropna(subset=['text'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
            
    
    def process_comments(self, submissions: praw.Reddit.submission) -> pd.DataFrame:
        
        body_markdown = []
        body_html = []
        comment_date = []
        ids = []
        comment_author = []
        comment_score = []
        
        for submission in submissions:
            for comment in submission.comments:
                try:
                    body_markdown.append(comment.body)
                except Exception:
                    body_markdown.append(None)
                try:
                    body_html.append(comment.body_html)
                except Exception:
                    body_html.append(None)
                try:
                    comment_date.append(comment.created_utc)
                except Exception:
                    comment_date.append(None)
                try:
                    ids.append(comment.id)
                except Exception:
                    ids.append(None)
                try:
                    comment_author.append(comment.author)
                except Exception:
                    comment_author.append(None)
                try:
                    comment_score.append(comment.score)
                except Exception:
                    comment_score.append(None)

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


