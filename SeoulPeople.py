import time

import requests
import json
import pandas as pd
import save_seoul_ppl_data
import schedule

df = pd.read_csv('./places.csv')

AREA_CD = df['AREA_CD'].tolist()
AREA_NM = df['AREA_NM'].tolist()


# print(AREA_CD)
# print(AREA_NM)


def send(placeID):
    host = f"http://openapi.seoul.go.kr:8088/4e574f4441796f7537316758474875/json/citydata_ppltn/1/5/{placeID}"
    res = requests.get(host)
    # print(res.text)
    data = json.loads(res.text)
    AREA_PPLTN_MIN = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MIN']
    AREA_PPLTN_MAX = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MAX']
    print(f"{AREA_NM[AREA_CD.index(placeID)]}의 현재 인구는 {AREA_PPLTN_MIN} ~ {AREA_PPLTN_MAX}명 입니다.")
    save_seoul_ppl_data.update(AREA_NM[AREA_CD.index(placeID)], AREA_PPLTN_MIN, AREA_PPLTN_MAX)


def getAll():
    for placeID in AREA_CD:
        send(placeID)


def main():
    schedule.every(5).minutes.do(getAll)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

