from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set Up App Routes

#Define main route
@app.route("/")

def index():
    # find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
    # return html template and use mars collection in MongoDB
   return render_template("index.html", mars=mars)


# Define scrape route
@app.route("/scrape")
def scrape():
    # access the database
    mars = mongo.db.mars
    # referencing the scrape_all function in the scraping.py file
    mars_data = scraping.scrape_all()
    # update the database
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    # navigate our page back to '/' to see updated content 
    return redirect('/', code=302)

if __name__ == "__main__":
   app.run()
