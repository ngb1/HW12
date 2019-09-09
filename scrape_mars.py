from flask import Flask, render_template
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo


def NASA_Mars_News():
    url = "https://mars.nasa.gov/news/"
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news = soup.find("div", class_='list_text')
    news_date = news.find("div", class_ ="list_date").text
    news_title = news.find("div", class_="content_title").text
    news_p = news.find("div", class_ ="article_teaser_body").text
    print(news_date)
    print(news_title)
    print(news_p)
    return (news_date, news_title, news_p)

def JPL_Mars_Imgs():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image_url = "https://www.jpl.nasa.gov" + soup.find("img", class_="thumb")["src"]
    print(featured_image_url)

    featured_image_date = soup.find("h3", class_="release_date").text
    print(featured_image_date)

    featured_image_title = soup.find("img", class_="thumb")["title"]
    print(featured_image_title)

    return ( featured_image_url, featured_image_date, featured_image_title)

def Mars_Weather():
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[1].text
    print(weather)

    weather_date = soup.find_all("span", class_="_timestamp js-short-timestamp")[1].text
    print( weather_date)

    return (weather, weather_date)

def Mars_Facts():
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    html_table = df.to_html()
    df.to_html('table.html')

    return ( html_table)

def Mars_Hemispheres():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img_header = soup.find_all("h3")

    title_list = []
    imgs_url_list = []

    for i in img_header:

    try:   
        title = i.get_text()
        browser.click_link_by_partial_text(title)
        imgs_url = browser.find_link_by_partial_href('download')['href']
        title_list.append(title)
        imgs_url_list.append(imgs_url)
        browser.visit(hemisphere_url)

        print('-----------')
        print(title)
        print(img_url)

# Click the 'Next' button on each page
#try:
#    browser.click_link_by_partial_text('next')
          
    except:
        print("Scraping Complete")

    hemisphere_dict = [{"title": title_list[i], "img_url": imgs_url_list[i]}  for i in range(len(img_header))]
    
    return(hemisphere_dict)

def scrape():
    mars_w = {}

    mars_w = {
        "weather":mars_weather()
    }
    mars_w["weather"] = Mars_Weather()

####################################################################################

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.team_db

# Drops collection if available to remove duplicates
db.team.drop()

# Creates a collection in the database and inserts two documents
db.team.insert_many(
    [
        {
            'player': 'Jessica',
            'position': 'Point Guard'
        },
        {
            'player': 'Mark',
            'position': 'Center'
        }
    ]
)


# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    teams = list(db.team.find())
    print(teams)

    # Return the template with the teams list passed in
    return render_template('index.html', teams=teams)


if __name__ == "__main__":
    app.run(debug=True)

##############################################################3

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = scrape_craigslist.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)