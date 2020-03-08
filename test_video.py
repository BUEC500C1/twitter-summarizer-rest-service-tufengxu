import tweets_queue
from tweets_queue import *
import tweets_to_video
from tweets_to_video import *
import queue


def test_twitter_video():
    names = ['@BU_Tweets', '@Lakers', '@NBA', '@universal_sci', '@sciencemagazine']
    tweets = get_feeds(names[0])
    assert tweets != ''
