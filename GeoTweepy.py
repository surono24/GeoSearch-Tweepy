
# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import MySQLdb
import logging
import random

# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret along as well as the access_token and secret will be generated for you after you register with Twitter Developers
consumer_key="insert your key"
consumer_secret="insert your secret"

access_token="insert your token"
access_token_secret="insert your secret"

# Create your MySQL schema and connect to database
db=MySQLdb.connect(host='..', user='..', passwd='..', db='..') 
db.set_character_set('utf8')

Coords = dict()
Place = dict()
PlaceCoords = dict()
ReTweets = dict()
XY = []
curr=db.cursor()

class StdOutListener(StreamListener):
                """ A listener handles tweets that are the received from the stream. 
                This is a basic listener that inserts tweets into MySQLdb.
                """
                def on_status(self, status):
                                #print "Tweet Text: ",status.text
                                text = status.text
                                #print "Time Stamp: ",status.created_at
                                try:
                                    Coords.update(status.coordinates)
                                    XY = (Coords.get('coordinates'))  #Place the coordinates values into a list 'XY'
                                    #print "X: ", XY[0]
                                    #print "Y: ", XY[1]
                                except:
                                    Place.update(status.place)
                                    PlaceCoords.update(Place['bounding_box'])
                                    Box = PlaceCoords['coordinates'][0]
                                    XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
                                    #print "X: ", XY[0]
                                    #print "Y: ", XY[1] 
                                    pass
                                # Comment out next 4 lines to avoid MySQLdb and Uncomment print statements to simply read stream
                                curr.execute("""INSERT INTO TwitterFeed2 (UserID, Date, X, Y, Text) VALUES
                                    (%s, %s, %s, %s, %s);""",
                                    (status.id_str,status.created_at,XY[0],XY[1],text))
                                db.commit()
                      

def main():
    l = StdOutListener()    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, timeout=30.0)
    #Only tracks locations OR tracks, NOT tracks with locations
    while True:
        try:
            # Call tweepy's userstream method 
            stream.filter(locations=[-125,25,-65,48], async=False)##These coordinates are approximate North and Western hemosphere [long1(-180),lat1(0),long2(-60),lat2(72](generally a bounding box around USA)
            #stream.filter(track=['obama'])## This will feed the stream all mentions of 'keyword'       
            break
        except Exception, e:
             # Abnormal exit: Reconnect
             nsecs=random.randint(60,63)
             time.sleep(nsecs)            

if __name__ == '__main__':
    main()
                
