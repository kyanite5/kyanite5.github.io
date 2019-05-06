# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# instantiate Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection to our mars_app db in mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()
    print(mars_data)
    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    # Run the scrape function
    mars_data_2 = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_data_2, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
