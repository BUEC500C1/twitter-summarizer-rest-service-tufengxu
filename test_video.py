# from tweets_to_video import get_feeds
# from tweets_to_video import text_to_image
# from tweets_to_video import image_to_video
from tweets_to_video import *
import queue


def test_twitter_video():
    names = ['@BU_Tweets', '@Lakers', '@NBA', '@universal_sci', '@sciencemagazine']
    tweets = get_feeds(names[0])
    assert tweets != ''
