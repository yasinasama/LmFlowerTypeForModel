# -*- coding: utf-8 -*-
import time

from flask import Flask, request, render_template
from PIL import Image

app = Flask(__name__)

@app.route('/upload',methods=['POST'])
def upload_image():
    model_image = request.files['model']
    flower_image = request.files['flower']
    try:
        fn = image_build(model_image,flower_image)
        return fn
    except Exception as e:
        return str(e)


@app.route('/')
def build():
    return render_template('index.html')


def image_build(m,f):
    model = Image.open(m)
    flower = Image.open(f)

    model = model.convert('RGB')
    flower = flower.convert('RGB')

    length, width = model.size
    flower.resize((length, width))

    model_px = model.load()
    flower_px = flower.load()

    for i in range(length):
        for j in range(width):
            p = model_px[i, j]
            if p != (255, 255, 255):
                flower_px[i, j] = p

    fn = str(int(time.time()))+'.jpg'
    path = './static/img/'
    abs_name = path+fn
    flower.save(abs_name)
    return abs_name


if __name__=='__main__':
    app.run()