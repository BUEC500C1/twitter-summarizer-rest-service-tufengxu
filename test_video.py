from video import get_feeds
from video import text_to_image
from video import image_to_video
import queue


def test_twitter_video():
    names = ['@BU_Tweets', '@Lakers', '@NBA', '@universal_sci', '@sciencemagazine']
    tweets = get_feeds(names[0])
    assert tweets != ''
