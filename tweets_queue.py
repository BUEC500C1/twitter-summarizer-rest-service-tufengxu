import threading
import queue
from queue import *
import multiprocessing
import time
from tweets_to_video import *


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
        print('\n' + "Finished." + '\n')
        q.task_done()

        
        
