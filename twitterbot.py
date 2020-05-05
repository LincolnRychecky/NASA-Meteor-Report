import tweepy
import requests
import json
# Authenticate to Twitter
auth = tweepy.OAuthHandler("i1Uhg4JlVD9ce3Nq6AVrHHcDx", "chD57OvgbzulKOaUsEFosyFJj0llKIqAJf73oi0XGAbCIUDyHm")
auth.set_access_token("1250474930178670593-Nm4zBI8sIB4S14mTyQ6Cbyq6vvie0f", "szTNXDOpipi2za5hcETflqNiJDn0cFmQxVN9eeD673U8k")

# Create API object
api = tweepy.API(auth)

# Create a tweet
#api.update_status("Hello Tweepy this is my second call to this asdfa asdjfaksjdhfkajhfk aksjdb ugcvugcvujgcjg")
# Make request from nasa json
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2020-04-14&end_date=2020-04-15&api_key=nTiezUKlDZQpC3TNQ1NUxGuLqQRDhfQYOdd3HBFa"
asteroidDict = requests.get(url)
json_data = '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'
pasrsed_json = (json.loads(asteroidDict.text))
print()
