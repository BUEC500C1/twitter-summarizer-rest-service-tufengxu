from tweets_queue import *
import threading
import queue
from queue import *
import multiprocessing


if __name__ == '__main__':
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

        
        
