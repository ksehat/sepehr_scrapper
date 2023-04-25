from flask import Flask, request, jsonify, Response
import json
from sepehr_scraper import get_booking_sepehr
# from flask import Flask
from waitress import serve

app1 = Flask(__name__)


@app1.route('/', methods=['POST'])
def home():
    if (request.method == 'POST'):
        data = json.loads(request.data)
        result = get_booking_sepehr(data)
        try:
            return jsonify({'data': (result.to_json(orient='records', force_ascii=False))}).json
        except:
            return Response(
                "Error in scraper",
                status=400,
            )


if __name__ == '__main__':
    serve(app1, host='192.168.40.155', port='3000')
# if __name__ == '__main__':
#     # Use Gunicorn to run the Flask application
#     from gunicorn.app.base import BaseApplication
#
#
#     class WindowsApplication(BaseApplication):
#         def __init__(self, app, options=None):
#             self.options = options or {}
#             self.application = app
#             super().__init__()
#
#         def init(self, parser, opts, args):
#             pass
#
#         def load_config(self):
#             config = {key: value for key, value in self.options.items()
#                       if key in self.cfg.settings and value is not None}
#             for key, value in config.items():
#                 self.cfg.set(key.lower(), value)
#
#         def load(self):
#             return self.application
#
#         def run(self):
#             # Set the file handle flags to prevent the server from blocking
#             handle = win32api.GetStdHandle(win32api.STD_OUTPUT_HANDLE)
#             mode = win32con.ENABLE_PROCESSED_OUTPUT | win32con.ENABLE_WRAP_AT_EOL_OUTPUT
#             win32api.SetConsoleMode(handle, mode)
#
#             # Call the BaseApplication.run() method to start the server
#             super().run()
#
#
#     options = {
#         'bind': '192.168.40.155:3000',
#         'workers': 4,
#     }
#     MyApplication(app, options).run()
