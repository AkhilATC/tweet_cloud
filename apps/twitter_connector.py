import tweepy
import yaml
import json
import apps.data_generation as dg
import apps.tweet_processing as TweetProcessor


class StreamListener(tweepy.StreamListener):

    def __init__(self, count, api=None):
        super(StreamListener, self).__init__(api)
        self.count = count
        self.clean = []

    def put_it_on(self, data):

        if len(self.clean) < self.count:
            self.clean.append(data)
            return True
        else:
            return False

    def on_status(self, status):
        data = status.text
        # print(self.clean)
        check = self.put_it_on(data)
        if not check:
            return False

    def on_error(self, status_code):
        if status_code == 420:
            return False


class GrabTweets(StreamListener):

    def __init__(self, count=10):

        with open(r'apps/config/settings.yml') as file_:
            get_auth_data = yaml.load(file_, Loader=yaml.FullLoader)

        consumer_key = get_auth_data['twitter_settings']['consumer_key']
        consumer_secret = get_auth_data['twitter_settings']['consumer_secret']
        access_token_key = get_auth_data['twitter_settings']['access_token_key']
        access_token_secret = get_auth_data['twitter_settings']['access_token_secret']
        # get_auth_data['twitter_settings']['user_name']
        self.count = count
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        self.api = tweepy.API(auth)
        self.stream_listener = StreamListener(count=self.count)
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self.stream_listener)

    def data_collector(self, payload):
        """
        parse data
        """
        data = payload._json
        result = dict({})
        entities = data.get('entities')
        entities.pop('urls')
        entities.pop('user_mentions')
        result.update(text=data.get('text'), entities=entities)
        return result

    def get_home_timeline_tweets(self, hasImage):
        """
        get home timeline tweets
        api.home_timeline()
        """
        tweets = self.api.home_timeline(count=self.count)
        data = map(self.data_collector, tweets)
        new_data = list(data)
        new_data = [each.get('text') for each in new_data]
        # print('--->{}'.format(new_data))
        pre_processed_data = map(TweetProcessor.clean_text, new_data)
        # print('--->{}'.format(pre_processed_data))
        new_data_processed = map(TweetProcessor.tweet_extractor, list(pre_processed_data))
        #print('----{}'.format(list(new_data_processed)))

        if hasImage is True:

            test_list = [' '.join(x.get('words')) for x in list(new_data_processed)]
            # print(test_list)
            test_list = [i for i in test_list if i]
            file_ = dg.generate_cloud_image(test_list)
            return file_
        else:
            return list(new_data_processed)

    def stremming(self, track, lang, hasImage):
        """
        track
        lang
        tweeter Stream block
        """
        print("HERE---------")

        connect = self.stream.filter(track=[track],
                                     languages=[lang])
        if hasImage is True:
            file_ = dg.generate_cloud_image(self.stream_listener.clean)
            return file_
        else:
            pre_processed_data = map(TweetProcessor.clean_text, self.stream_listener.clean)
            # print('--->{}'.format(pre_processed_data))
            new_data_processed = map(TweetProcessor.tweet_extractor, list(pre_processed_data))
            return list(new_data_processed)

    def user_info(self):
        """
        # get user info
        # name,
        # screen_name,
        # location.
        """
        info = self.api.me()
        user = dict(info._json)
        name = user.pop('name')
        screen_name = user.pop('screen_name')
        loc = user.pop('location')
        return {
            "name": name,
            "screen_name": screen_name,
            "location": loc
        }

    def search(self, query, hasImage, geocode=None):
        """
        params:query,geocode
        """
        Tweet = tweepy.Cursor(self.api.search, q=query, geocode=geocode).items(self.count)
        data = map(self.data_collector, Tweet)
        new_data = list(data)
        #print(new_data)
        new_data = [each.get('text') for each in new_data]
        # print(new_data)
        pre_processed_data = map(TweetProcessor.clean_text,new_data)
        new_data_processed = map(TweetProcessor.tweet_extractor, pre_processed_data)
        # file_ = dg.generate_cloud_image(list(new_data_processed))
        if hasImage is True:
            test_list = [' '.join(x.get('words')) for x in list(new_data_processed)]
            test_list = [i for i in test_list if i]
            file_ = dg.generate_cloud_image(test_list)

            return file_
        else:
            return list(new_data_processed)


if __name__ == '__main__':
    print('iiii')
    track = ['CAB']
    x = GrabTweets().serch("mohanlal",
                           geocode="40.7142700,-74.0059,5000km")
    print(x)