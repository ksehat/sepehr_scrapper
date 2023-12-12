from flask import Flask, request, Response
import json
from flask_caching import Cache
from concurrent.futures import ThreadPoolExecutor
import hashlib
import time
from sepehr_scraper import sepehr_scrapper
from flight724_scrapper import Flight724Scrapper
from alameer.alameer_scrapper import AlameerScrapper
from trampoline import trampoline
from waitress import serve
from concurrent.futures import ThreadPoolExecutor

app1 = Flask(__name__)
executor = ThreadPoolExecutor()
cache = Cache(app1, config={'CACHE_TYPE': 'simple'})
def generate_request_hash(data):
    hash_object = hashlib.sha256(json.dumps(data, sort_keys=True).encode())
    return hash_object.hexdigest()

@app1.route('/call_from_backend_to_scrap', methods=['POST'])
def call_from_backend():
    if request.method == 'POST':
        data = json.loads(request.data)
        filtered_dict = {key: data[key] for key in ['Orig', 'Dest', 'date'] if key in data}
        request_hash = generate_request_hash(filtered_dict)

        if cache.get(request_hash):
            return Response(status=429)
        cache.set(request_hash, True, timeout=900)
        result_future = executor.submit(alameer_scrapper, data)
        result = result_future.result()
        return json.dumps({
            'id': data['id'],
            'Message': "ok",
            'data': json.dumps(result.to_dict('records'))
        })


# @app1.route('/sepehr360', methods=['POST'])
# def home():
#     if (request.method == 'POST'):
#         data = json.loads(request.data)
#         result = sepehr_scrapper(data)
#         try:
#             return jsonify({'data': (result.to_json(orient='records', force_ascii=False))}).json
#         except:
#             return Response(
#                 "Error in scraper",
#                 status=400,
#             )
#
#
# @app1.route('/flight724', methods=['POST'])
# def flight724_api():
#     if (request.method == 'POST'):
#         data = json.loads(request.json)
#         f_scrapper = Flight724Scrapper(data[0], data[1], data[2])
#         result = trampoline(f_scrapper.get_flight724_route)
#         if result:
#             return Response(
#                 "Success.",
#                 status=200,
#             )
#         else:
#             return Response(
#                 "Error occured.",
#                 status=400,
#             )


def alameer_scrapper(data):
    f_scrapper = AlameerScrapper(orig=data['Orig'], dest=data['Dest'], days_num=1, scraping_date=data['date'],
                                 id_from_backend=data['id'])
    result = trampoline(f_scrapper.get_alameer_route)
    return result


# @app1.route('/scrap_runner', methods=['POST'])
# def scrap_runner():
#     if (request.method == 'POST'):
#         data = json.loads(request.json)
#         if data[0] == 'alameer.ir':
#             f_scrapper = AlameerScrapper(data[1], data[2], data[3])
#             result = trampoline(f_scrapper.get_alameer_route)
#         # if data[0] == 'www.flytodayir.com':
#         #     f_scrapper = AlameerScrapper(data[0], data[1], data[2])
#         #     result = trampoline(f_scrapper.get_alameer_route())
#         # if data[0] == 'www.alibaba.ir':
#         #     f_scrapper = AlameerScrapper(data[0], data[1], data[2])
#         #     result = trampoline(f_scrapper.get_alameer_route())
#         if result:
#             return Response(
#                 "Success.",
#                 status=200,
#             )
#         else:
#             return Response(
#                 "Error occured.",
#                 status=400,
#             )


if __name__ == '__main__':
    print('app.py started.')
    serve(app1, host='192.168.115.17', port='3000', threads=10)
