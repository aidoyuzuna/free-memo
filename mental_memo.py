import os
import csv
import datetime
import requests


# 気象情報取得
def get_meteorological(now_raw):
    now_meteorological = now_raw.strftime('%Y%m%d%H')
    url = "https://www.jma.go.jp/bosai/amedas/data/map/" + now_meteorological + "0000.json"
    header = {"content-type": "application/json"}
    response = requests.get(url, headers=header)
    data = response.json()

    temp = data["50331"]["temp"]  # 気温（静岡）
    pres = data["50331"]["pressure"]  # 気圧（静岡）
    hum = data["50331"]["humidity"]  # 湿度（静岡）

    return temp[0], pres[0], hum[0]


# メンタルデータを書き込む
def data_input():
    input_body = int(input("今のカラダの調子を数値化（1～5）してください："))
    if input_body < 0 or input_body > 5:
        print("エラーだよ！もう一度カラダの調子を入力してね")
        input_body = int(input("今のカラダの調子を数値化（1～5）してください："))

    input_mental = int(input("今のココロの調子を数値化（1～5）してください："))
    if input_mental < 0 or input_mental > 5:
        print("エラーだよ！もう一度カラダの調子を入力してね")
        input_body = int(input("今のココロの調子を数値化（1～5）してください："))

    input_comment = input("今の気分・コメントを書いてください：")
    return input_body, input_mental, input_comment


# CSV書き込み
def white_csv(out_body, out_mental, out_comment):
    with open(full_path, mode="a", encoding='utf8', newline='') as f:
        csvwriter = csv.writer(f)
        now = datetime.datetime.now()
        temperature, pressure, humidity = get_meteorological(now)
        now_format = now.strftime("%Y-%m-%d %H:%M")
        if os.stat(full_path).st_size == 0:
            empty_data = ["日付", "気温", "気圧", "湿度", "カラダ", "ココロ", "コメント"]
            csvwriter.writerow(empty_data)
        data = [[now_format, temperature, pressure, humidity, out_body, out_mental, out_comment]]
        csvwriter.writerows(data)


# ファイルパス
root_dir = "I:\\09_ジャンクボックス\\094_ナレッジ・体調ログ\\体調ログ"
month_date = datetime.datetime.today()
month_file = month_date.strftime("%Y-%m")
full_path = f"{os.path.join(root_dir, month_file)}.csv"

# 実行
body, mental, comment = data_input()
white_csv(body, mental, comment)
