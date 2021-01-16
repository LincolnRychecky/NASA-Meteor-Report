import tweepy
import requests
import json
from datetime import datetime, timedelta

def retweetAccount(ID, api):
    #retrieve user using twitter id
    userID = ID
    #fetch most recent tweeet from @apod
    tweets = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=1,
                               include_rts = False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
    #retweet the retrieved status
    api.retweet(tweets[0].id)

def authenticate():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("i1Uhg4JlVD9ce3Nq6AVrHHcDx", "chD57OvgbzulKOaUsEFosyFJj0llKIqAJf73oi0XGAbCIUDyHm")
    auth.set_access_token("1250474930178670593-Nm4zBI8sIB4S14mTyQ6Cbyq6vvie0f", "szTNXDOpipi2za5hcETflqNiJDn0cFmQxVN9eeD673U8k")
    # Create API object
    api = tweepy.API(auth)
    return api

def retrieveNEOs():
    #Retrieve current date in UTC time to account for Heroku system time
    curDate = datetime.date(datetime.utcnow() - timedelta(days=1))
    #Make request from nasa json for data on current date
    url = "https://api.nasa.gov/neo/rest/v1/feed?start_date="+str(curDate)+"&end_date="+str(curDate)+"&api_key=nTiezUKlDZQpC3TNQ1NUxGuLqQRDhfQYOdd3HBFa"
    reqJson = requests.get(url)
    #Parse json into a dictionary
    parsed_json = (json.loads(reqJson.text))
    return parsed_json

api = authenticate()

parsed_json = retrieveNEOs()

curDate = datetime.date(datetime.utcnow() - timedelta(days=1))
numberNeos = parsed_json['element_count']
#Calculate how many days to subtract from current to see rest of week (week means monday-sunday)
subtractDays = 0
if curDate.weekday() == 0:
    subtractDays = 0
elif curDate.weekday() == 1:
    subtractDays = 1
elif curDate.weekday() == 2:
    subtractDays = 2
elif curDate.weekday() == 3:
    subtractDays = 3
elif curDate.weekday() == 4:
    subtractDays = 4
elif curDate.weekday() == 5:
    subtractDays = 5
elif curDate.weekday() == 6:
    subtractDays = 6
#Make request from nasa json for data on current week
urlTwo = "https://api.nasa.gov/neo/rest/v1/feed?start_date="+str(curDate-timedelta(days=subtractDays))+"&end_date="+str(curDate)+"&api_key=nTiezUKlDZQpC3TNQ1NUxGuLqQRDhfQYOdd3HBFa"
reqJsonTwo = requests.get(urlTwo)
#Parse json into a dictionary
parsed_json_two = (json.loads(reqJsonTwo.text))
#Create dictionary with the number of NEOs each day in the last week had
neosPerDate = []
for key in parsed_json_two['near_earth_objects']:
    neosPerDate.append(len(parsed_json_two['near_earth_objects'][key]))
#Count the number of days with more NEO activity this calendar week
daysGreater = 0
for day in neosPerDate:
    if int(numberNeos) > day:
        daysGreater += 1
#Calculate number of days with more NEOs observed in the last calendar week
numberDaysExceeding = len(neosPerDate) - daysGreater - 1
#If a monday, nothing to compare to so tweet. Else, figure out what number to use to describe standing
standing = "most"
tweeted = False
if curDate.weekday() == 0:
    #Create Tweet
    api.update_status(str(numberNeos) + " NEOs passed earth today, " + str(curDate) + ". " + "Not a bad monday in near earth space!")
    tweeted = True
elif curDate.weekday() == 6:
    #End of week roundup
    if numberDaysExceeding == 1:
        standing = "2nd"
    elif numberDaysExceeding == 2:
        standing = "3rd"
    elif numberDaysExceeding == 3:
        standing = "4th"
    elif numberDaysExceeding == 4:
        standing = "5th"
    elif numberDaysExceeding == 5:
        standing = "6th"
    elif numberDaysExceeding == 6:
        standing = "least"
    api.update_status(str(numberNeos) + " NEOs passed earth today, " + str(curDate) + ". " + "That is the " + str(standing) + " most active day so far this week! Now its time for the sunday roundup. This week " + parsed_json_two['element_count'] + " total NEOs were detected by NASA instruments!")
    tweeted = True
else:
    if numberDaysExceeding == 1:
        standing = "2nd"
    elif numberDaysExceeding == 2:
        standing = "3rd"
    elif numberDaysExceeding == 3:
        standing = "4th"
    elif numberDaysExceeding == 4:
        standing = "5th"
    elif numberDaysExceeding == 5:
        standing = "6th"
    elif numberDaysExceeding == 6:
        standing = "least"
if tweeted == False:
    api.update_status(str(numberNeos) + " NEOs passed earth today, " + str(curDate) + ". " + "That is the " + str(standing) + " most active day so far this week!")
    tweeted = True

retweetAccount("@apod", api)
