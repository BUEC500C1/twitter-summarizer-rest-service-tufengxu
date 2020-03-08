from flask import render_template
from flask import send_file
from flask import send_from_directory
from app import app
from video import *
import os
import request


myDict = {
    'BU': '@BU_Tweets',
    'Lakers': '@Lakers',
    'NBA': '@NBA',
    'UniSci': '@universal_sci',
    'Science': '@sciencemagazine'
}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route("/<abbr>", methods=['GET'])
def genLaga(abbr):
    user = myDict[abbr]
    filename = '{}.mp4'.format(user)
    tweets = get_feeds(user)
    for iii in range(20):
        text_to_image(tweets[iii], iii + 1)
    image_to_video(user)
    return send_from_directory(os.getcwd(), filename, as_attachment=True)
