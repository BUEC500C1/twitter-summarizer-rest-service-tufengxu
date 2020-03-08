# -*- coding:utf-8 -*-

import threading
import queue
from queue import *
import multiprocessing
import time
from PIL import Image, ImageDraw, ImageFont
import tweepy
from tweepy import OAuthHandler, Stream
import re
from nltk.tokenize import WordPunctTokenizer
from keys import *
from flask import Flask
from flask import render_template
from flask import send_file
from flask import send_from_directory
from app import app
import os


def get_feeds(name):
    tweets_list = []
    if consumer_key == '':
        f = open("example.txt")
        ttt = f.readlines()
        for t in ttt:
            tweets_list.extend(t)
        return tweets_list
    else:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        new_tweet = api.user_timeline(screen_name=name, count=50)
        tweets_list.extend(new_tweet)
    # Processing the tweets
        cleaned_tweets_list = []  # All cleaned tweets are stored in this list
        for status in tweets_list:
            tweet_i = status.text.encode('utf-8')
            removed = re.sub(r'@[A-Za-z0-9]+', '', tweet_i.decode('utf-8'))
            link_rm = re.sub('https?://[A-Za-z0-9./]+', '', removed)
            number_rm = re.sub('[^a-zA-Z]', ' ', link_rm)
            lower = number_rm.lower()
            tok = WordPunctTokenizer()
            words = tok.tokenize(lower)
            cleaned = (' '.join(words)).strip()
            cleaned_tweets_list.append(cleaned)
        return cleaned_tweets_list


def text_to_image(raw, th):
    text = ''
    col = 0
    while col < len(raw):
        text += raw[col: col + 40] + '\n'
        col += 40
    # set the fonts
    font = ImageFont.truetype("0.ttf", 25)
    image = Image.open("BU_Twitter.png")
    height, width = image.size
    draw = ImageDraw.Draw(image)
    draw.text((150, 300), text, (30 * th % 255, 10 * th % 165, 400 * th % 155), font=font)
    image.save("./text_to_image_" + str(th) + ".png")


def image_to_video(name):
    with open('videos.txt', 'w') as f:
        for i in range(20):
            command = "ffmpeg -ss 0 -t 3 -f lavfi -i color=c=0x000000:s=830x794:r=30  " \
                      "-i /Users/fengxutu/Documents/BU/EC500/Code/text_to_image_" + str(i+1) \
                      + ".png -filter_complex \"[1:v]scale=830:794[v1];[0:v][v1]overlay=0:0[outv]\"  " \
                      "-map [outv] -c:v libx264 /Users/fengxutu/Documents/BU/EC500/Code/video" \
                      + str(i+1) + ".mp4 -y"
            p = os.popen(command)
            p.close()
            f.write("file video" + str(i+1) + ".mp4" + '\n')
        f.close()
    cd = "ffmpeg -f concat -i videos.txt -c copy OutputVideo" + name + ".mp4"
    pp = os.popen(cd)
    pp.close()


def in_queue(q):
    while True:
        q_item = q.get()
        nn = 0
        q_size = q.qsize()
        if q_item is None:
            print("There is 0 item!")
            nn = 0
            break
        nn += 1
        print("Processing on the " + str(nn) + "th from " + str(q_size) + " items")
        tweets = get_feeds(q_item)
        for ii in range(20):
            text_to_image(tweets[ii], ii + 1)
        image_to_video(q_item)
        print("Finished.")
        q.task_done()


names = ['@BU_Tweets', '@Lakers', '@NBA', '@universal_sci', '@sciencemagazine']

q = queue.Queue()
N = 3
ths = []

for item in names:
    q.put(item)

for ii in range(N):
    tt = threading.Thread(target=in_queue(q))
    tt.daemon = True
    tt.start()
    ths.append(tt)
q.join()

for jj in range(N):
    q.put(None)

for ll in ths:
    tt.join()
