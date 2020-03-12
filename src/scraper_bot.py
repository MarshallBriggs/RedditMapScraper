#!/usr/bin/env python3
"""
Module Docstring
"""

import praw
import pandas as pd
import wget
import pathlib
from pathlib import Path
import os.path
from os import path
import sys

__author__ = "Marshall Briggs"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    # Path to script currently
    root_path = pathlib.Path().absolute()
    # print(root_path)
    # Path to images folder
    images_path = root_path/"images"
    Path(images_path).mkdir(parents=True, exist_ok=True)
    # print(images_path)

    reddit = praw.Reddit(client_id='YWdkCzRc9WGAGQ', client_secret='70AueOljfrE_524-7XJgWfEYbKE', user_agent='Reddit_Map_Scraper')

    subreddit = reddit.subreddit('dndmaps')
    # subreddit = reddit.subreddit('battlemaps')
    # subreddit = reddit.subreddit('dndmaps+battlemaps')

    posts = []

    for submission in subreddit.top('all', limit=10):
        submission_name, submission_ext = os.path.splitext(submission.url)
        if submission.link_flair_text:
            save_folder = str(images_path) + "\\" + submission.link_flair_text
        else:
            save_folder = str(images_path) + "\\noflair"
        Path(save_folder).mkdir(parents=True, exist_ok=True)
        save_path = save_folder + "\\" + submission.title + submission_ext
        if path.exists(save_path) is not False:
            print(submission_name + " already exists")
        else:
            try:
                submission_image = wget.download(submission.url, save_path)
                posts.append([submission.title, submission.score, submission.id, submission.subreddit, submission.url, 
                        submission.num_comments, submission.selftext, submission.created, submission.link_flair_text, save_path])
            except OSError as err:
                print()
                # print("Error fetching " + submission.title + " from reddit")
                print("OS error: {0}".format(err))
            """except:
                e = sys.exc_info()[0]
                print()
                print("Error fetching " + submission.title + " from reddit")
                print("Error: %s" % e)"""
    
    if posts:
        posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'flair', 'save_path'])
        print("Posts:")
        print(posts)
    elif not posts:
            print("No new posts")
    

if __name__ == "__main__":
    main()