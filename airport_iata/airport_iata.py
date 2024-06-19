import pandas as pd

def get_iata_code(airport_name):
    airport_dict = {
        'Airport name': {0: 'مهرآباد', 1: 'مشهد', 2: 'شيراز', 3: 'تبريز', 4: 'اصفهان', 5: 'اهواز', 6: 'بوشهر',
                         7: 'کرمان',
                         8: 'ساري', 9: 'يزد', 10: 'کرمانشاه', 11: 'رشت', 12: 'زاهدان', 13: 'آبادان', 14: 'بندرعباس',
                         15: 'گرگان', 16: 'همدان', 17: 'اردبيل', 18: 'ايلام', 19: 'اروميه', 20: 'بيرجند', 21: 'سنندج',
                         22: 'شهرکرد', 23: 'بجنورد', 24: 'لارستان', 25: 'خرم آباد', 26: 'پارس آبادمغان', 27: 'سمنان',
                         28: 'شاهرود', 29: 'نوشهر', 30: 'ياسوج', 31: 'زنجان', 32: 'اراک', 33: 'زابل'},
        'IATA code': {0: 'THR', 1: 'MHD', 2: 'SYZ', 3: 'TBZ', 4: 'IFN', 5: 'AWZ', 6: 'BUZ', 7: 'KER', 8: 'SRY',
                      9: 'YZD',
                      10: 'KSH', 11: 'RAS', 12: 'ZAH', 13: 'ABD', 14: 'BND', 15: 'GBT', 16: 'HDM', 17: 'ARD', 18: 'ILM',
                      19: 'OMH', 20: 'XBJ', 21: 'SDG', 22: 'CKD', 23: 'BJN', 24: 'LRR', 25: 'KHM', 26: 'BDM', 27: 'SMN',
                      28: 'SHD', 29: 'NSA', 30: 'YJK', 31: 'ZJN', 32: 'AJK', 33: 'ZBL'}}

    airport_df = pd.DataFrame(airport_dict)
    if airport_name in airport_df['Airport name'].values:
        return airport_df[airport_df['Airport name'] == airport_name]['IATA code'].values[0]
    else:
        return ''


# print(get_iata_code('مهرآباد'))






