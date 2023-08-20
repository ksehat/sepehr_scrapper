import datetime
from flask import Flask, request, jsonify, Response
import json
from sepehr_scraper import sepehr_scrapper
from flight724_scrapper import Flight724Scrapper, trampoline
# from flask import Flask
from waitress import serve

app1 = Flask(__name__)


@app1.route('/', methods=['POST'])
def home():
    if (request.method == 'POST'):
        data = json.loads(request.data)
        result = sepehr_scrapper(data)
        try:
            return jsonify({'data': (result.to_json(orient='records', force_ascii=False))}).json
        except:
            return Response(
                "Error in scraper",
                status=400,
            )


@app1.route('/flight724', methods=['POST'])
def flight724_api():
    if (request.method == 'POST'):
        data = json.loads(request.json)
        f_scrapper = Flight724Scrapper(data[0], data[1], data[2])
        result = trampoline(f_scrapper.get_flight724_route)
        if result:
            return Response(
                "Success.",
                status=200,
            )
        else:
            return Response(
                "Error occured.",
                status=400,
            )


if __name__ == '__main__':
    print('app.py started.')
    serve(app1, host='192.168.115.17', port='3000', threads=30)
