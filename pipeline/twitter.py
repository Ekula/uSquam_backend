from datetime import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
from flask_restful import Resource
from flask import request, jsonify


# Get request to:
# localhost:9000/requesters/crawlTweets?hashtag=tudelft&number=3
# will return a json with the last 3 tweets that contain #tudelft.
class TwitterCrawler(Resource):
    def get(self, hashtag='#tudelft', number=3):
        hashtag = request.args.get('hashtag')
        number = request.args.get('number')

        if hashtag is not None and number is not None and number.isdigit():
            hashtag = str(hashtag)
            number = int(number)
        else:
            # Error
            return 'Wrong input parameters, try ?hashtag=tudelft&number=50', 404

        # Successful request
        print 'GET request:  Requested ' + str(number) + ' tweets with #' + str(hashtag) + '.'

        crawled_tweets_list = []

        consumer_key = '0tqrIxEVCdJiziTsng9QcOoEJ'
        consumer_secret = 'H4JgzHBDhLtKxuYg9tDuXySVxMioYYoqZCXL1cCn2POAPkVfdh'
        access_token = '774227310367109120-VvqXuw2b5bjqar6EiML5lJL7xprwNsi'
        access_token_secret = 'Ms295kCa0YV0NeFOwU0BpF23ElEkX0Wv7p8lQQH2jUm5v'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        search_results = api.search(hashtag, count=number)

        for tweet in search_results:
            tweet_json = tweet._json

            # Get hashtags list
            hashtags_list = []
            for item in tweet_json['entities']['hashtags']:
                hashtags_list.append(item['text'])

            # Reformat json to contain less properties
            crawled_tweet = {'user_name': tweet_json['user']['screen_name'],
                             'tweet_text': tweet_json['text'],
                             'hashtags_list': hashtags_list,
                             'created_at': tweet_json['created_at']}
            crawled_tweets_list.append(crawled_tweet)


            # print 'user_name: ' + tweet_json['user']['screen_name']
            # print 'tweet_text: ' + tweet_json['text']
            # print 'hashtags_list: ' + str(hashtags)
            # print 'created_at: ' + str(tweet_json['created_at'])
            # # print 'timestamp: ' + str(datetime.fromtimestamp(int(float(data['timestamp_ms']) / 1000.0)))
            # print '--------------------------------'

        # If list is not empty
        if crawled_tweets_list:
            return jsonify(results=crawled_tweets_list)
        else:
            return None, 404

# # Test
# print TwitterCrawler().get('#tudelft', 3)

# # This can be used to crawl tweets from stream
# class CustomStreamListener(StreamListener):
#     def on_data(self, data):
#         data = json.loads(data)
#
#         hashtags = []
#         for item in data['entities']['hashtags']:
#             hashtags.append(item['text'])
#
#         print 'user_name: ' + data['user']['screen_name']
#         print 'tweet_text: ' + data['text']
#         print 'hashtags_list: ' + str(hashtags)
#         # print 'timestamp: ' + str(datetime.fromtimestamp(int(float(data['timestamp_ms']) / 1000.0)))
#         print 'created_at: ' + str(data['created_at'])
#         print '--------------------------------'
#         return True
#
#     def on_error(self, status):
#         print(status)
#         return False  # disconnect the stream
#
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#
# stream = Stream(auth, CustomStreamListener())
# stream.filter(track=['#tudelft'])
# # stream.filter(track=['#amsterdam'], async=True)
