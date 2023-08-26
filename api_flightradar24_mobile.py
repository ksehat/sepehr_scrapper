from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from pymongo import MongoClient
import waitress


def search_in_mongo(airport):
    MONGODB_HOST = '192.168.115.17'
    MONGODB_PORT = 27017
    MONGODB_USER = 'kanan'
    MONGODB_PASS = '123456'
    MONGODB_DB = 'flightradar24_DB'
    client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                         username=MONGODB_USER,
                         password=MONGODB_PASS,
                         authSource=MONGODB_DB)
    db = client['flightradar24_DB']
    collection = db['flightradar24']

    filters = {'airport': airport}

    mongo_result = collection.find(filters, sort=[('insert_date', -1)])
    docs = [doc for doc in mongo_result]
    arrivals_doc = [item for sublist in docs for item in
                    sublist['result']['pluginData']['schedule']['arrivals']['data']]
    departures_doc = [item for sublist in docs for item in
                      sublist['result']['pluginData']['schedule']['departures']['data']]
    grounds_doc = [item for sublist in docs for item in sublist['result']['pluginData']['schedule']['ground']['data']]
    result_dict = {
        'arrivals': arrivals_doc,
        'departures': departures_doc,
        'ground': grounds_doc
    }
    return result_dict


app = Flask(__name__)
api = Api(app)

# Define the expected input payload using a model
input_model = api.model('InputModel', {
    'airport': fields.String(required=True, description='The acronym of the name of airport'),
})


@api.route('/')
class Process(Resource):
    @api.expect(input_model)
    def post(self):
        try:
            data = request.get_json()
            result = search_in_mongo(data['airport'])
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)})


# @api.route('/get-airports')
# def get_airports_dict():
#     return jsonify({'airports': ['ika', 'thr', 'mhd', 'syz', 'kih']})

if __name__ == '__main__':
    app.run(host='192.168.115.17', port=8086)
