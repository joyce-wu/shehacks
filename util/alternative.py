#given news article title and website

import sqlite3
import database
import random
import Algorithmia
import nltk
import requests

#must download beforehand
#nltk.download('averaged_perceptron_tagger')

#picks random news source from database with given rating
def get_news_source(rating):
    db = sqlite3.connect("../data/ratings.db")
    c = db.cursor()
    x = c.execute("SELECT url FROM news_sources WHERE rating=? ORDER BY RANDOM() LIMIT 1", [rating])
    for line in x:
        print(line[0])
        return line[0]
    db.close()
#get_news_source(1)

#extracts keywords/tags from text
def get_tags(title):
    # finds key words given article title
    client = Algorithmia.client('simflQNnfUnKf9qMHnRDWd75G6u1')
    algo = client.algo('nlp/AutoTag/1.0.1')
    tags = algo.pipe(title).result
    # identifies and removes adjectives
    result = nltk.pos_tag(tags)
    input = "" #returns string of keywords for google search
    for i in range(len(result)):
        print(i)
        if(result[i][1].find("J") == -1): #word is not an adjective (JJ, JJR, JJS)
            input += "+" + result[i][0]
    print(input)
    return input
# get_tags("Trump sought release of secret Nunes memo, putting him at odds with Justice Department")

#finds random article given a random number on the spectrum
def find_random(title):
    rating = random.randrange(-10, 10, 5) / 10.0
    news_source = get_news_source(rating)
    keywords = get_tags(title)
    query = keywords #+ " " + news_source
    url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCct5M0BgsjZ_Fl-QQXNjWfXuhWkYS91zY&cx=009075568653349274157:erwoj2uzova&q="+query
    # try:
    res = requests.get(url)
    data = res.json()
    for x in range(len(data['items'])):
        try:
            print(data['items'][x]['link'])#['pagemap']['metatags'][0]['og:url'])#['link'])#['formattedUrl'])#['og:url'])#['article']) #[0]['url'])
            print("=================================")
        except:
            print("uh doesn't work hun")

#find_random("Trump sought release of secret Nunes memo, putting him at odds with Justice Department")
find_random("Ald. Burke under ethics board investigation for possible conflict of interest")

#finds alternative article on the opposite side of the spectrum
def find_alternative(title, website):
    other_rating = database.get_rating(website) * -1 #gets rating from opposite end of spectrum
    news_source = get_news_source(rating)
    keywords = get_tags(title)
    return find_article(keywords + " " + news_source, other_rating)
