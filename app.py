from flask import Flask, request, jsonify, Response
import json
from sepehr_scraper import sepehr_scrapper
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


if __name__ == '__main__':
    serve(app1, host='192.168.40.155', port='3000')
