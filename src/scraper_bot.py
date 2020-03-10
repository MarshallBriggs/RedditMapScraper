#!/usr/bin/env python3
"""
Module Docstring
"""

import praw
import pandas as pd
import wget
import pathlib

__author__ = "Marshall Briggs"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    # Path to script currently
    root_path = pathlib.Path().absolute()
    print(root_path)
    images_path = root_path/"images"
    print(images_path)

    # Create Reddit Instance
    reddit = praw.Reddit(client_id='YWdkCzRc9WGAGQ', client_secret='70AueOljfrE_524-7XJgWfEYbKE', user_agent='Reddit_Map_Scraper')

    subreddit = reddit.subreddit('dndmaps')
    # subreddit = reddit.subreddit('battlemaps')
    # subreddit = reddit.subreddit('dndmaps+battlemaps')

    posts = []

    """for submission in subreddit.top('all', limit=10):
        print(submission.title)
        print(submission.score)
        print(submission.id)
        print(submission.url) # this is the picture
        print(submission.link_flair_text)
        # print(vars(submission))"""

    for submission in subreddit.top('all', limit=3):
        posts.append([submission.title, submission.score, submission.id, submission.subreddit, submission.url, submission.num_comments, submission.selftext, submission.created, submission.link_flair_text])
        wget.download(submission.url, str(images_path))
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'flair'])
    print(posts)
    

if __name__ == "__main__":
    main()