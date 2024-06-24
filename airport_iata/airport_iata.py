import pandas as pd
import json


def get_iata_code(airport_name):
    # airport_iata_df = pd.read_csv('E://Projects2//sepehr_scrapper//airport_iata//airport_to_iata.csv')
    # data_dict = airport_iata_df.to_dict(orient='records')
    # json_string = json.dumps(data_dict, ensure_ascii=False)

    json_string = [{"Airport name": "آبادان", "IATA code": "ABD"}, {"Airport name": "سهند", "IATA code": "ACP"},
                   {"Airport name": "زابل", "IATA code": "ACZ"}, {"Airport name": "آدانا", "IATA code": "ADA"},
                   {"Airport name": "ازمیر", "IATA code": "ADB"}, {"Airport name": "اردبیل", "IATA code": "ADU"},
                   {"Airport name": "جزیره ابوموسی", "IATA code": "AEU"},
                   {"Airport name": "آغاجاری", "IATA code": "AKW"},
                   {"Airport name": "قیصریه (قیصریه)", "IATA code": "ASR"},
                   {"Airport name": "ابوظبی", "IATA code": "AUH"}, {"Airport name": "اهواز", "IATA code": "AWZ"},
                   {"Airport name": "یزد", "IATA code": "AZD"}, {"Airport name": "بحرین", "IATA code": "BAH"},
                   {"Airport name": "بندرلنگه", "IATA code": "BDH"}, {"Airport name": "بیروت", "IATA code": "BEY"},
                   {"Airport name": "بغداد", "IATA code": "BGW"}, {"Airport name": "بجنورد", "IATA code": "BJB"},
                   {"Airport name": "بودروم (میلاس)", "IATA code": "BJV"},
                   {"Airport name": "بانکوک", "IATA code": "BKK"}, {"Airport name": "بندرعباس", "IATA code": "BND"},
                   {"Airport name": "باتومی", "IATA code": "BUS"}, {"Airport name": "بوشهر", "IATA code": "BUZ"},
                   {"Airport name": "بم", "IATA code": "BXR"}, {"Airport name": "گوانگ‌ژو", "IATA code": "CAN"},
                   {"Airport name": "پاریس", "IATA code": "CDG"}, {"Airport name": "کلن بن", "IATA code": "CGN"},
                   {"Airport name": "شهرکرد", "IATA code": "CQD"}, {"Airport name": "دمشق", "IATA code": "DAM"},
                   {"Airport name": "دزفول", "IATA code": "DEF"}, {"Airport name": "دهلی", "IATA code": "DEL"},
                   {"Airport name": "دالامان", "IATA code": "DLM"}, {"Airport name": "دنیزلی", "IATA code": "DNZ"},
                   {"Airport name": "دوحه", "IATA code": "DOH"}, {"Airport name": "دبی", "IATA code": "DXB"},
                   {"Airport name": "دوشنبه", "IATA code": "DYU"}, {"Airport name": "اربیل", "IATA code": "EBL"},
                   {"Airport name": "آنکارا (اَسَن‌بوغا)", "IATA code": "ESB"},
                   {"Airport name": "ایروان", "IATA code": "EVN"}, {"Airport name": "فرانکفورت", "IATA code": "FRA"},
                   {"Airport name": "گرگان", "IATA code": "GBT"}, {"Airport name": "گچساران", "IATA code": "GCH"},
                   {"Airport name": "قشم", "IATA code": "GSM"}, {"Airport name": "باکو", "IATA code": "GYD"},
                   {"Airport name": "هامبورگ", "IATA code": "HAM"}, {"Airport name": "همدان", "IATA code": "HDM"},
                   {"Airport name": "هنگ‌کنگ", "IATA code": "HKG"}, {"Airport name": "پوکت", "IATA code": "HKT"},
                   {"Airport name": "بهرگان", "IATA code": "IAQ"}, {"Airport name": "اصفهان", "IATA code": "IFN"},
                   {"Airport name": "ایرانشهر", "IATA code": "IHR"}, {"Airport name": "ایلام", "IATA code": "IIL"},
                   {"Airport name": "امام خمینی", "IATA code": "IKA"}, {"Airport name": "ماکو", "IATA code": "IMQ"},
                   {"Airport name": "استانبول", "IATA code": "IST"}, {"Airport name": "سلیمانیه", "IATA code": "ISU"},
                   {"Airport name": "جهرم", "IATA code": "JAR"}, {"Airport name": "جده", "IATA code": "JED"},
                   {"Airport name": "جاسک", "IATA code": "JSK"}, {"Airport name": "زنجان", "IATA code": "JWN"},
                   {"Airport name": "جیرفت", "IATA code": "JYR"}, {"Airport name": "کابل", "IATA code": "KBL"},
                   {"Airport name": "قندهار", "IATA code": "KDH"}, {"Airport name": "کرمان", "IATA code": "KER"},
                   {"Airport name": "خرم‌آباد", "IATA code": "KHD"}, {"Airport name": "خرم آباد", "IATA code": "KHD"},
                   {"Airport name": "کراچی", "IATA code": "KHI"}, {"Airport name": "خارگ", "IATA code": "KHK"},
                   {"Airport name": "خارک", "IATA code": "KHK"}, {"Airport name": "خوی", "IATA code": "KHY"},
                   {"Airport name": "كيش", "IATA code": "KIH"}, {"Airport name": "کرکوک", "IATA code": "KIK"},
                   {"Airport name": "کرمانشاه", "IATA code": "KSH"},
                   {"Airport name": "کوالا لامپور", "IATA code": "KUL"}, {"Airport name": "کویت", "IATA code": "KWI"},
                   {"Airport name": "پولکوو", "IATA code": "LED"}, {"Airport name": "لامرد", "IATA code": "LFM"},
                   {"Airport name": "لاهور", "IATA code": "LHE"}, {"Airport name": "لندن", "IATA code": "LHR"},
                   {"Airport name": "لارستان", "IATA code": "LRR"}, {"Airport name": "لاوان", "IATA code": "LVP"},
                   {"Airport name": "مسقط", "IATA code": "MCT"}, {"Airport name": "مدینه", "IATA code": "MED"},
                   {"Airport name": "ماکائو", "IATA code": "MFM"}, {"Airport name": "مشهد", "IATA code": "MHD"},
                   {"Airport name": "ماهشهر", "IATA code": "MRX"},
                   {"Airport name": "میلانو مالپنسا", "IATA code": "MXP"},
                   {"Airport name": "مزارشریف", "IATA code": "MZR"}, {"Airport name": "نجف", "IATA code": "NJF"},
                   {"Airport name": "نوشهر", "IATA code": "NSH"}, {"Airport name": "صحار", "IATA code": "OHS"},
                   {"Airport name": "ارومیه", "IATA code": "OMH"}, {"Airport name": "اروميه", "IATA code": "OMH"},
                   {"Airport name": "پکن", "IATA code": "PEK"}, {"Airport name": "پارس‌آباد", "IATA code": "PFQ"},
                   {"Airport name": "پارس آبادمغان", "IATA code": "PFQ"},
                   {"Airport name": "عسلویه", "IATA code": "PGU"}, {"Airport name": "داکسینگ پکن", "IATA code": "PKX"},
                   {"Airport name": "شانگهای پودنگ", "IATA code": "PVG"}, {"Airport name": "رشت", "IATA code": "RAS"},
                   {"Airport name": "رفسنجان", "IATA code": "RJN"}, {"Airport name": "رامسر", "IATA code": "RZR"},
                   {"Airport name": "اسپارتا", "IATA code": "SAR"},
                   {"Airport name": "استانبول (صبیحه گوکچن)", "IATA code": "SAW"},
                   {"Airport name": "آکتایو", "IATA code": "SCO"},
                   {"Airport name": "آقتائو اکتاوو", "IATA code": "SCO"}, {"Airport name": "سنندج", "IATA code": "SDG"},
                   {"Airport name": "شارجه", "IATA code": "SHJ"}, {"Airport name": "سمنان", "IATA code": "SNX"},
                   {"Airport name": "ساری", "IATA code": "SRY"}, {"Airport name": "سیری", "IATA code": "SXI"},
                   {"Airport name": "سیرجان", "IATA code": "SYJ"}, {"Airport name": "شیراز", "IATA code": "SYZ"},
                   {"Airport name": "شنژن بن", "IATA code": "SZX"}, {"Airport name": "تفلیس", "IATA code": "TBS"},
                   {"Airport name": "تبریز", "IATA code": "TBZ"}, {"Airport name": "طبس", "IATA code": "TCX"},
                   {"Airport name": "تهران", "IATA code": "THR"}, {"Airport name": "مهرآباد", "IATA code": "THR"},
                   {"Airport name": "اورومچی", "IATA code": "URC"}, {"Airport name": "وین", "IATA code": "VIE"},
                   {"Airport name": "ونوکووا", "IATA code": "VKO"}, {"Airport name": "بیرجند", "IATA code": "XBJ"},
                   {"Airport name": "یاسوج", "IATA code": "YES"}, {"Airport name": "زاهدان", "IATA code": "ZAH"},
                   {"Airport name": "چابهار", "IATA code": "ZBR"},
                   {"Airport name": "تنب بزرگ", "IATA code": "تنب بزرگ"},
                   {"Airport name": "سراوان", "IATA code": "سراوان"}]

    airport_df = pd.DataFrame(json_string)

    if airport_name in airport_df['Airport name'].values:
        return airport_df[airport_df['Airport name'] == airport_name]['IATA code'].values[0]
    else:
        return airport_name


# print(get_iata_code('یاسوج'))
