import tweepy


class StreamListener(tweepy.StreamListener):

    def __init__(self,api=None):
        super(StreamListener, self).__init__(api)
        self.count = 10
        self.clean = []
    def put_it_on(self,data):

        if len(self.clean) < self.count:
            self.clean.append(data)
            return True
        else:
            return False
    def on_status(self, status):
        data = status.text
        #print(self.clean)
        check = self.put_it_on(data)
        if not check:
            return False
    def on_error(self, status_code):
        if status_code == 420:
            return False


import yaml
import json


class GrabTweets(StreamListener):

    def __init__(self):
        with open(r'config/settings.yml') as file_:
            get_auth_data = yaml.load(file_, Loader=yaml.FullLoader)

        consumer_key = get_auth_data['twitter_settings']['consumer_key']
        consumer_secret = get_auth_data['twitter_settings']['consumer_secret']
        access_token_key = get_auth_data['twitter_settings']['access_token_key']
        access_token_secret = get_auth_data['twitter_settings']['access_token_secret']
        # get_auth_data['twitter_settings']['user_name']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        self.api = tweepy.API(auth)

        self.stream_listener = StreamListener()
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self.stream_listener)

    def cool(self):
        connect = self.stream.filter(track=['python'])
        if not connect:
            print(len(self.stream_listener.clean))



if __name__ == '__main__':
    GrabTweets().cool()

