from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

# Establish Flask app & mongodb connection
app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Connect to mongo db and mars_info collection
db = client.mars
collection = db.mars_info


@app.route("/")
def index():
    mars = db.mars_info.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    collection = db.mars_info
    mars_data = scrape_mars.scrape()
    collection.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
