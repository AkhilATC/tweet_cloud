
import twitter

class TwittyCrow:

    def __init__(self):
       
        self.api = twitter.Api(consumer_key=<customer_key>,#pass customer key
                consumer_secret=<consumer_secret>,#pass consumer_secret
                access_token_key=<access_token_key>,#pass access_token_key
                access_token_secret=<access_token_key>)#pass access_token_key
        #'lang': 'en' - geo - location
        #['68.116667 ,8.066667,97.416667,37.100000']

    def strem_processor(self,data):
        print('stream -- processing')
        strem_= data.get('entities').get('hashtags')
        if strem_ != []:
            tags = [x.get('text') for x in strem_]
            tweet = data.get('user')['description']
            return {'hash tags':tags,'tweet':tweet}

    def get_strems(self):
        print("--- Fetching tweeter data --- GetStreamFilter")
        raw_data = self.api.GetStreamFilter(locations=['68.116667 ,8.066667,97.416667,37.100000'],languages=['en'],filter_level=['low'])
        print(len(list(raw_data)))
        data = map(self.strem_processor,raw_data)
        print(list(data))
    
    def get_sample_strems(self):
        print("--- Fetching tweeter data --- GetStreamSample")
        raw_data = self.api.GetStreamSample()
        print(len(list(raw_data)))
        data = map(self.strem_processor,raw_data)
        print(list(data))



if __name__ == '__main__':
    TwittyCrow().get_strems()
