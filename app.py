from flask import Flask, render_template, redirect
from pymongo import MongoClient
import scrape

# Flask app
app = Flask(__name__)

# Mongo connection
db_url = "mongodb://localhost:27017"
client = MongoClient(db_url)

collection = db.mars_data

@app.route("/")
def index():
    mars_data = db.collection.find_one()
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scraper():
    db.collection.remove({})
    mars_data = scrape.scrape()
    db.collection.insert_one(mars_data)
    return  render_template('scrape.html')

if __name__ == "__main__":
    app.run(debug=True)