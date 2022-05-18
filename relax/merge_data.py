import os

import pandas as pd


def merge_csv(season_path, season_no):
    dfs = []
    for i in os.listdir(season_path):
        csv_path = os.path.join(season_path, i)
        df = pd.read_csv(csv_path)
        df['season'] = i.split('：', 1)[0]
        dfs.append(df)

    df = pd.concat(dfs)
    df.to_csv(f'data/raw_{season_no}.csv', encoding='utf-8-sig')
    print(df.sample(10))


def merge_all():
    merge_csv(os.path.join('asset', '令人心动的offer_第1季'), 1)
    merge_csv(os.path.join('asset', '令人心动的offer_第2季'), 2)
    merge_csv(os.path.join('asset', '令人心动的offer_第3季'), 3)


if __name__ == '__main__':
    merge_all()
