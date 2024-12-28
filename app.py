from flask import Flask, render_template, redirect, url_for
from scrape_twitter import scrape_twitter_data
from datetime import datetime
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_scraper"]
collection = db["tweets"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run')
def run_script():
    trends, timestamp = scrape_twitter_data()
    last_record = collection.find_one(sort=[("timestamp", -1)]) 
    json_extract = {
        "_id": str(last_record["_id"]),
        "timestamp": last_record["timestamp"],
        "trends": last_record["trends"]
    }

    return render_template(
        'results.html',
        trends=trends,
        timestamp=timestamp,
        ip_address="127.0.0.1", 
        json_extract=json_extract
    )

if __name__ == "__main__":
    app.run(debug=True)
