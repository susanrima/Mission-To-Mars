#dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Connect to MongoDB
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")



# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def home():
    # Find one record of data from the mongo database
    destination_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=destination_data)

# Create route called /scrape
@app.route('/scrape')
def scrape():
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)