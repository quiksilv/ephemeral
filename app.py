import os
from zipfile import ZipFile
from flask import Flask, render_template, jsonify

app = Flask(__name__)
@app.route('/download', methods=['GET', 'POST'])
def download():
    filepath = "static/tmp/download.zip"
    with ZipFile(filepath, 'w') as zip:
       for path, directories, files in os.walk("static/images/"):
           for file in files:
               file_name = os.path.join(path, file)
               zip.write(file_name)
    return {"status": 0, "message": "Download ready.", "filepath": "/"+filepath}, 200
@app.route('/')
def main():
    images = os.listdir("static/images/")
    return render_template("index.html", data = {'images': images} )
if __name__ == '__main__':
    app.run()
