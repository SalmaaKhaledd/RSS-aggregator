import feedparser
from flask import Flask, render_template, request

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'nytimes': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
}

@app.route('/')
def index():
  articles = []
  for source, feed in RSS_FEEDS.items():
    parsed_feed = feedparser.parse(feed) #downloads the RSS XML content from the URL and converts it into a Python object.
    entries = [(source, entry) for entry in parsed_feed.entries] #parsed_feed.entries--> list of news items from feed.
    articles.extend(entries)

  articles.sort(key=lambda x: x[1].published_parsed, reverse=True) #sorts the articles by published date in descending order.

  page= request.args.get('page', 1, type=int) #get the page number from the URL query string.
  per_page = 10
  total_articles = len(articles)
  start= (page - 1) * per_page
  end = start + per_page 
  paginated_articles = articles[start:end]
  total_pages = (total_articles + per_page - 1) // per_page

  return render_template('index.html', articles=paginated_articles, page=page, total_pages=total_pages)


@app.route('/search')
def search():
  query = request.args.get('q') 
  articles = []
  for source, feed in RSS_FEEDS.items():
    parsed_feed = feedparser.parse(feed)
    entries = [(source, entry) for entry in parsed_feed.entries if query.lower() in entry.title.lower()]
    articles.extend(entries)

  articles.sort(key=lambda x: x[1].published_parsed, reverse=True)

  page= request.args.get('page', 1, type=int)
  per_page = 10
  total_articles = len(articles)
  start= (page - 1) * per_page
  end = start + per_page 
  paginated_articles = articles[start:end]
  total_pages = (total_articles + per_page - 1) // per_page

  return render_template('search.html', articles=paginated_articles, query=query)

if __name__ == '__main__':  
  app.run(debug=True)
  

