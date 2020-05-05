import tweepy
import requests
import json
from datetime import datetime
#DateTime==4.3

# Authenticate to Twitter
auth = tweepy.OAuthHandler("i1Uhg4JlVD9ce3Nq6AVrHHcDx", "chD57OvgbzulKOaUsEFosyFJj0llKIqAJf73oi0XGAbCIUDyHm")
auth.set_access_token("1250474930178670593-Nm4zBI8sIB4S14mTyQ6Cbyq6vvie0f", "szTNXDOpipi2za5hcETflqNiJDn0cFmQxVN9eeD673U8k")
# Create API object
api = tweepy.API(auth)

#Retrieve current date
curDate = str(datetime.date(datetime.now()))
#Make request from nasa json for data on current date
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date="+curDate+"&end_date="+curDate+"&api_key=nTiezUKlDZQpC3TNQ1NUxGuLqQRDhfQYOdd3HBFa"
reqJson = requests.get(url)
#Parse json into a dictionary
parsed_json = (json.loads(reqJson.text))
numberNeos = str(parsed_json['element_count'])

# Create a tweet
api.update_status(numberNeos + " NEOs passed earth today. That is a slow day in near earth space!")
