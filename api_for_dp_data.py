import pandas as pd
from flask import Flask, request, Response
import json
from flask_caching import Cache
import hashlib
from alameer.alameer_scrapper import AlameerScrapper
from flight724.flight724_scrapper import Flight724Scrapper
from flightio.flightio_scrapper import FlightioScrapper
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
        result_future1 = executor.submit(alameer_scrapper, data)
        result_future2 = executor.submit(flight724_scrapper, data)
        result_future3 = executor.submit(flightio_scrapper, data)
        result1 = result_future1.result()
        result2 = result_future2.result()
        result3 = result_future3.result()
        return json.dumps({
            'id': data['id'],
            'Message': "ok",
            'data': {'alameer_data': result1.to_dict('records') if isinstance(result1, pd.DataFrame) else result1,
                     'flight724_data': result2.to_dict('records') if isinstance(result2, pd.DataFrame) else result2,
                     'flightio_data': result3.to_dict('records') if isinstance(result3, pd.DataFrame) else result3}
        }, ensure_ascii=False)


def alameer_scrapper(data):
    f_scrapper = AlameerScrapper(orig=data['Orig'], dest=data['Dest'], days_num=1, flight_date=data['date'],
                                 id_from_backend=data['id'])
    result = trampoline(f_scrapper.get_alameer_route)
    return result


def flight724_scrapper(data):
    f_scrapper = Flight724Scrapper(orig=data['Orig'], dest=data['Dest'], days_num=1, flight_date=data['date'],
                                   id_from_backend=data['id'])
    result = trampoline(f_scrapper.get_flight724_route)
    return result

def flightio_scrapper(data):
    f_scrapper = FlightioScrapper(orig=data['Orig'], dest=data['Dest'], days_num=1, flight_date=data['date'],
                                   id_from_backend=data['id'])
    result = trampoline(f_scrapper.get_flightio_route)
    return result


if __name__ == '__main__':
    print('app.py started.')
    serve(app1, host='192.168.115.17', port='3000', threads=10)
