
import praw

reddit = praw.Reddit(
    client_id="JQ-Xy6H7nKEw6Q",
    client_secret="b3gHTs0Y3sMIy5c8_SrsJP-I851faA",
    user_agent="u/repulsive-bear503",
)
for comment in reddit.subreddit('redditdev').comments(extra_query="gme", limit=None):
    print(comment.created_utc)
    print(comment.body)