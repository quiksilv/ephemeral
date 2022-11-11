import os
from flask import Flask, render_template

app = Flask(__name__)
# Had to do this stuff in a try-finally, since some testing 
# went a little wrong.....
@app.route('/')
def main():
    images = os.listdir("static/images/")
    return render_template("index.html", data = {'images': images} )

if __name__ == '__main__':
    app.run()
