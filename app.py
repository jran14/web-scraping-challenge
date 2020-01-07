from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Flask app
app = Flask(__name__)

# Mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_data_db

#insert mars_data into Mongo
#db.marsdata.insert_one(scrape_mars)


@app.route("/")
def index():

    mars_data = db.mars_data.find_one()
    print('---------------------')
    print(mars_data)
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars_data= db.mars_data
    mars_data_update = scrape_mars.scrape()
    db.mars_data.remove({})
    db.mars_data.insert_one(mars_data_update)
    return  render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)