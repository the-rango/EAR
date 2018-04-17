import os
import tweepy
import time
import redis

def parse_json(tweet):
    #        'id','time stamp',
    #        'text','images','videos,'hashtag',
    #        'retweets','likes',
    #        'join date','followers','following','total tweets'
    result = []
    
    result.append(tweet['id'])
    result.append(tweet['created_at'])
    
    result.append(tweet['full_text'])
    images, videos = [], []
    if 'media' in tweet['entities']:
        for medium in tweet['entities']['media']:
            if medium['type'] == 'photo':
                images.append(medium['media_url_https'])
    if 'extended_entities' in tweet:
        if 'media' in tweet['extended_entities']:
            for medium in tweet['extended_entities']['media']:
                if medium['type'] == 'video':
                    videos.append(medium['video_info']['variants'][0]['url'])
    result.append(str(images))
    result.append(str(videos))
    result.append(' '.join(d['text'] for d in tweet['entities']['hashtags']))
    
    result.append(tweet['retweet_count'])
    result.append(tweet['favorite_count'])
    
    result.append(tweet['user']['created_at'])
    result.append(tweet['user']['followers_count'])
    result.append(tweet['user']['friends_count'])
    result.append(tweet['user']['statuses_count'])

    return result            

# generator
class Retriever:
    api = []
    account = 0

    for i in range(2):
        consumer_key = os.environ.get('{}_C_Key'.format(i+1))
        consumer_secret = os.environ.get('{}_C_Secret'.format(i+1))
        access_token = os.environ.get('{}_A_Token'.format(i+1))
        access_token_secret = os.environ.get('{}_A_Token_Secret'.format(i+1))

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api.append(tweepy.API(auth))
    
    def get_tweets(self, user, l_id):
        #print(user)
        cursor = tweepy.Cursor(self.api[self.account].user_timeline,
                               screen_name=user,
                               include_rts='false',
                               exclude_replies='true',
                               tweet_mode='extended',
                               since_id=l_id,
                               count=200).items()
        last_id = ''
        while True:
            try:    
                tweet = cursor.next()._json
                last_id = tweet['id']
                yield parse_json(tweet)
            except Exception as e:
                if '429' in str(e):
                    print('***HIT RATE LIMIT***')
                    time.sleep(6.7 * 60)
                    if self.account == 0:
                        self.account = 1
                    else:
                        self.account = 0
                    if last_id == '':
                        cursor = tweepy.Cursor(self.api[self.account].user_timeline,
                                               screen_name=user,
                                               count=200,
                                               include_rts='false',
                                               exclude_replies='true',
                                               since_id=l_id,
                                               tweet_mode='extended').items()
                    else:
                        cursor = tweepy.Cursor(self.api[self.account].user_timeline,
                                               screen_name=user,
                                               max_id=str(last_id-1),
                                               count=200,
                                               include_rts='false',
                                               exclude_replies='true',
                                               since_id=l_id
                                               tweet_mode='extended').items()
                elif str(e).strip() == '':
                    return[]
                else:
                    print('bad handle: {}'.format(user))
                    print(e)
                    return []
