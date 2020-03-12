#!/usr/bin/env python3
"""
Module Docstring
"""

import praw
import pandas as pd
import wget
import pathlib
import os.path
from os import path

__author__ = "Marshall Briggs"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    # Path to script currently
    root_path = pathlib.Path().absolute()
    print(root_path)
    # Path to images folder
    images_path = root_path/"images"
    print(images_path)

    reddit = praw.Reddit(client_id='YWdkCzRc9WGAGQ', client_secret='70AueOljfrE_524-7XJgWfEYbKE', user_agent='Reddit_Map_Scraper')

    subreddit = reddit.subreddit('dndmaps')
    # subreddit = reddit.subreddit('battlemaps')
    # subreddit = reddit.subreddit('dndmaps+battlemaps')

    posts = []

    for submission in subreddit.top('all', limit=3):
        posts.append([submission.title, submission.score, submission.id, submission.subreddit, submission.url, submission.num_comments, submission.selftext, submission.created, submission.link_flair_text])
        submission_name, submission_ext = os.path.splitext(submission.url)
        image_location = str(images_path)+"\\"+submission.title+submission_ext
        if path.exists(image_location) is not False:
            print("Image Exists")
        else:
            submission_image = wget.download(submission.url, image_location)
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'flair'])
    print(posts)
    

if __name__ == "__main__":
    main()