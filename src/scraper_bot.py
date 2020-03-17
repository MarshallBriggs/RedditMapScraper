#!/usr/bin/env python3
"""
Module Docstring
"""

import praw
import pandas as pd
import wget
import pathlib
from pathlib import Path
import sys
import string

__author__ = "Marshall Briggs"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    # Get the current working directory of the script
    current_dir = Path.cwd()
    # Get path to images folder
    imagespath = pathlib.Path.cwd() / 'images'
    imagespath.mkdir(parents=True, exist_ok=True)

    reddit = praw.Reddit(client_id='YWdkCzRc9WGAGQ', client_secret='70AueOljfrE_524-7XJgWfEYbKE', user_agent='Reddit_Map_Scraper')

    subreddit = reddit.subreddit('dndmaps')
    # subreddit = reddit.subreddit('battlemaps')
    # subreddit = reddit.subreddit('dndmaps+battlemaps')

    posts = []
    downloaded_posts = 0
    new_posts = 0
    download_error_posts = 0

    for submission in subreddit.top('all', limit=10):
        print(submission.title)
        submission_path = pathlib.Path(submission.url)
        submission_name = submission_path.stem
        submission_ext = submission_path.suffix
        if submission.link_flair_text:
            image_save_folder = imagespath / submission.link_flair_text
        else:
            image_save_folder = imagespath / 'noflair'
        # print(image_save_folder)
        image_save_folder.mkdir(parents=True, exist_ok=True)
        submission_savename = submission.title + submission_ext
        image_save_path = image_save_folder / format_filename(submission_savename)
        save_path_exists = False
        try:
            save_path_exists = image_save_path.exists()
            print("Save Path Exists: " + str(save_path_exists))
            if image_save_path.exists():
                print(submission_name + " already exists")
                downloaded_posts = downloaded_posts + 1
            else:
                try:
                    submission_image = wget.download(submission.url, str(image_save_path))
                    posts.append([submission.title, submission.score, submission.id, submission.subreddit, submission.url, 
                            submission.num_comments, submission.selftext, submission.created, submission.link_flair_text, image_save_path])
                    new_posts = new_posts + 1
                except OSError as err:
                    print("OS error: {0}".format(err))
                    download_error_posts = download_error_posts + 1
        except OSError as err:
            print("Save Path Exists: Error")
            print("OS error: {0}".format(err))
            download_error_posts = download_error_posts + 1
        print()
    
    if posts:
        posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'flair', 'image_save_path'])
        print()
        print("Posts:")
        print(posts)
    elif not posts:
            print("No new posts")
    
    print("Posts from list already downloaded: " + str(downloaded_posts))
    print("New Posts downloaded in this script: " + str(new_posts))
    print("Errors downloading Posts in this script: " + str(download_error_posts))

def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.
 
Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.
 
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

if __name__ == "__main__":
    main()