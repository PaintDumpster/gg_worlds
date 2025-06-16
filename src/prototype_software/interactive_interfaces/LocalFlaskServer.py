import os
from flask import Flask, request

PORT = 8765
STORAGE_FOLDER = "/home/salvador_cb/3_term/gg_worlds/data/storage"

app = Flask(__name__)

@app.route('/<path:subpath>', methods=['GET', 'POST'])
def main(subpath):
    filename = f"{STORAGE_FOLDER}/{subpath}"
    if request.method == 'POST':
        dataRaw = request.get_data()
        with open(filename, "wb") as f:
            f.write(dataRaw)
    elif request.method == 'GET':
        file = open(filename, 'r')
        dataRaw = file.read()
        file.close()
        return dataRaw
    
if __name__ == '__main__':
    try:
        app.run(debug=True, port=PORT)
    except KeyboardInterrupt:
        pass