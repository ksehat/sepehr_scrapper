import datetime
from flask import Flask, request, jsonify, Response
import json
from sepehr_scraper import sepehr_scrapper
from flight724_scrapper import Flight724Scrapper
from alameer.alameer_scrapper import AlameerScrapper
from trampoline import trampoline
from waitress import serve
from concurrent.futures import ThreadPoolExecutor

app1 = Flask(__name__)
old_data = None

executor = ThreadPoolExecutor()

@app1.route('/call_from_backend_to_scrap', methods=['POST'])
def call_from_backend():
    if (request.method == 'POST'):
        data = json.loads(request.data)
        global old_data
        try:
            if old_data == data:
                return json.dumps({'Message':"Please wait. Your job is running."})
        except:
            pass
        old_data = data
        try:
            # future = executor.submit(alameer_scrapper, data)
            alameer_scrapper(data)
            # TODO: Here we should use parallel for to call all website scrappers at the same time
            old_data = None
            return json.dumps({'Message': "ok"})

        except:
            return {'Message': "An error occured in scraper."}


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
    f_scrapper = AlameerScrapper(orig=data['orig'], dest=data['dest'], days_num=1, scraping_date=data['date'])
    result = trampoline(f_scrapper.get_alameer_route)


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
