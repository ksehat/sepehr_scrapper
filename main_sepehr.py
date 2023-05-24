import os
import pandas as pd
import ast
import json
import logging
import requests
from datetime import datetime as dt
import datetime
from request_APIs import call_sepehr, call_login_token, call_input_setting_db


def api_token_handler():
    if 'token_expire_date.txt' in os.listdir():
        with open('token_expire_date.txt', 'r') as f:
            te = f.read()
        expire_date = te.split('token:')[0]
        token = te.split('token:')[1]
        if dt.now() >= dt.strptime(expire_date, '%Y-%m-%d'):
            token, expire_date = call_login_token()
            expire_date = expire_date.split('T')[0]
            with open('token_expire_date.txt', 'w') as f:
                f.write(expire_date + 'token:' + token)
    else:
        token, expire_date = call_login_token()
        expire_date = expire_date.split('T')[0]
        with open('token_expire_date.txt', 'w') as f:
            f.write(expire_date + 'token:' + token)
    return token


def main():
    # Create logger and assign handler
    logging.basicConfig(filename='log.log', filemode='a', format="%(asctime)s|%(levelname)s|%(name)s|%(message)s")
    logger = logging.getLogger("flight_scraper")
    # handler = logging.FileHandler('log.log')
    # handler.setFormatter(logging.Formatter())
    # logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info('Application started.')
    token = api_token_handler()
    # region API request for input setting
    logger.info('Calling input setting API.')
    data = call_input_setting_db(token)
    logger.info('Calling input setting API was successful.')
    # endregion

    # region controlling df_routes for handling start process time
    logger.info('Handling routes_start_time.csv file.')
    if 'routes_start_time.csv' in os.listdir():
        df_routes = pd.read_csv('routes_start_time.csv')
        df_routes['route'] = df_routes['route'].map(lambda x: ast.literal_eval(x))
        df_routes['start_process_time'] = pd.to_datetime(df_routes['start_process_time'])
    else:
        df_routes = pd.DataFrame({
            'route': json.loads(data.text)['getAllRouteMonitoringResponseItemViewModels'],
            'start_process_time': [dt.now() - datetime.timedelta(1)] * len(
                json.loads(data.text)['getAllRouteMonitoringResponseItemViewModels'])
        })
        df_routes.to_csv('routes_start_time.csv', index=False)
    # endregion

    while True:
        token = api_token_handler()
        for index, row in df_routes.iterrows():
            if ((dt.now() - row[1]).total_seconds() / 60) >= row[0]['interval']:
                logger.info(
                    f'Scraping the route {row[0]["iataCodeOrigin"]} to {row[0]["iataCodeDestination"]} for {row[0]["monitoringDays"]} days(day) with interval of {row[0]["interval"]} minutes started.')
                request_time = dt.now().strftime("%d-%m-%Y %H:%M:%S")
                try:
                    result = call_sepehr(json.dumps(row[0]))
                except:
                    error_message = 'There occured an error in the call_sepehr function.'
                response_time = dt.now().strftime("%d-%m-%Y %H:%M:%S")
                if result:
                    logger.info(
                        f'Scraping the route {row[0]["iataCodeOrigin"]} to {row[0]["iataCodeDestination"]} for {row[0]["monitoringDays"]} days(day) with interval of {row[0]["interval"]} minutes finished successfuly.')
                    error_message = None
                    df_routes.loc[index, 'start_process_time'] = request_time
                    df_routes.to_csv('routes_start_time.csv', index=False)
                    result_dict = json.loads(result.text) if json.loads(result.text)['data'] != '[]' else {'data':[{}]}
                    result_dict['createRouteMonitoringResultRequestItemViewModels'] = result_dict.pop('data')
                    if result_dict['createRouteMonitoringResultRequestItemViewModels'] != [{}]:
                        result_dict['createRouteMonitoringResultRequestItemViewModels'] = json.loads(
                            result_dict['createRouteMonitoringResultRequestItemViewModels'])
                    result_dict["requestTime"] = str(request_time).split(".")[0]
                    result_dict['responseTime'] = str(response_time).split(".")[0]
                    result_dict['errorMessage'] = f'{error_message}'
                    result_dict['fkRouteMonitoringDetail'] = row[0]["pkRouteMonitoringDetail"]
                    r = requests.post(url='http://192.168.115.10:8083/api/RouteMonitoringResult/CreateRouteMonitoringResult',
                                      json=result_dict,
                                      headers={'Authorization': f'Bearer {token}',
                                               'Content-type': 'application/json',
                                               })
                else:
                    logger.error(
                        f'Scraping the route {row[0]["iataCodeOrigin"]} to {row[0]["iataCodeDestination"]} for {row[0]["monitoringDays"]} days(day) with interval of {row[0]["interval"]} minutes was unsuccessful.')
                    error_message = 'Error in Scraper'
                    r = requests.post(url='http://192.168.115.10:8083/api/RouteMonitoringResult/CreateRouteMonitoringResult',
                                      json={'createRouteMonitoringResultRequestItemViewModels': [{}],
                                            'requestTime': str(request_time).split(".")[0],
                                            'responseTime': str(response_time).split(".")[0],
                                            'errorMessage': error_message,
                                            'fkRouteMonitoringDetail': row[0]["pkRouteMonitoringDetail"]},
                                      headers={'Authorization': f'Bearer {token}',
                                               'Content-type': 'application/json',
                                               })


if __name__ == '__main__':
    main()
