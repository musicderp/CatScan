from io import open as iopen
from urllib.parse import urlsplit

import praw
import requests

reddit = praw.Reddit()

subreddit = reddit.subreddit('blurrypicturesofcats')
posts = subreddit.top(limit=100)

filename = "urls.txt"
f = open(filename, 'r+')
urlList = f.read().splitlines()

for post in posts:
    print(post.url)
    file_url = post.url

    if file_url[-3:] != "jpg":
        print("Not an image")

    else:
        if file_url in urlList:
            print("Url has already been used")
        else:
            f.write(file_url + "\n")

            urlList.append(file_url)

            suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', ]
            file_name = urlsplit(file_url)[2].split('/')[-1]
            file_suffix = file_name.split('.')[1]
            print(file_name)
            folderName = "images/raw/" + file_name
            print(folderName)

            i = requests.get(file_url)
            if file_suffix in suffix_list and i.status_code == requests.codes.ok:
                with iopen(folderName, 'wb') as file:
                    file.write(i.content)
            else:
                print("we goofed boys")
f.close()
