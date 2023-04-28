# Webscraping
import requests
from bs4 import BeautifulSoup
import json

"""
In this script we will scrape data from below RSS feed link, that is in XML format. 
Then we will list out the contents and save the content to .txt file for further analisys.
We are creating two functions for the same. 1st function will list out all the contents using requests,BeautifulSoup module.
second function will save the content to .txt file using JSON module
We will call the 2nd function inside 1st function itself.
"""

def hackernews_rss():
    article_list = []  # We will save each article to this list
    try:
        r = requests.get('https://news.ycombinator.com/rss') # Fetch the full site (given link)
        soup = BeautifulSoup(r.content, features='xml')  # Read the content from the above response using the module BeautifulSoup using xml parser
        articles = soup.findAll('item')  # Find all the elements with <item> tag
        for a in articles:
            title = a.find('title').text  # From each item fidn out the titles
            link = a.find('link').text # From each item fidn out the link value
            published = a.find('pubDate').text # From each item fidn out the published value . .text will remove the <> and give us exact content
            article = {               # Saving the above values to one dictionary named 'article'
                'title': title,
                'link': link,
                'published': published
                }
            article_list.append(article)  # Appending each element to the article_list.
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)


def save_function(article_list):
    with open('articles.txt', 'w') as outfile:
        json.dump(article_list, outfile)


# Calling the function
hackernews_rss()
