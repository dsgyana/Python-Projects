from celery import Celery
import requests # pulling data
from bs4 import BeautifulSoup # xml parsing
import json # exporting to files
from datetime import datetime # for time stamps


app = Celery('tasks')


# save function
@app.task
def save_function(article_list):
    # timestamp and filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'articles-{}.json'.format(timestamp)
    
    # creating our articles file with timestamp
    with open(filename, 'w') as outfile:
        json.dump(article_list, outfile)


# scraping function
@app.task
def hackernews_rss():
    article_list = []
    try:
        # execute my request, parse the data using the XML 
        # parser in BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')
        # select only the "items" I want from the data      
        articles = soup.findAll('item')
        # for each "item" I want, parse it into a list
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'created_at': str(datetime.now()),
                'source': 'HackerNews RSS'
                }
            # append my "article_list" with each "article" object
            article_list.append(article)
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)




from celery.schedules import crontab # scheduler
# scheduled task execution
app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'tasks.hackernews_rss',
        'schedule': crontab()
    }
}
