from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from snownlp import SnowNLP


def main():

    # df = pd.read_csv('data/1.csv',dtype={'content':'string'},
    #                  parse_dates=['timepoint'],
    #                  date_parser=lambda x: datetime.strptime(x, '%H:%M:%S'))
    df = pd.read_csv('data/1.csv', dtype={'content': 'string'})
    df = df.dropna()
    df = df.loc[0:100]
    df['sentiment'] = df['content'].apply(lambda x: SnowNLP(x).sentiments)
    # df.to_csv('data/2_1.csv',encoding='utf-8-sig')
    print(df.sample(100, replace=True))
    # 合并时间
    df['timepoint'] = pd.to_datetime(df['timepoint'])
    df.index = df['timepoint']

    df2 = df.resample('15min').mean().reset_index()
    print(df2)

    # df.index = df.index.apply(lambda x: datetime.strftime(x,'%H:%M:%S'))
    df.index = df.index.strftime('%H:%M:%S, %r')

    # 给数据表添加调色板
    color_map = sns.light_palette('orange', as_cmap=True)  #light_palette调色板
    df2.style.background_gradient(color_map)
    # sns.palplot(color_map,5)
    ax = sns.heatmap(df2, cmap=color_map)
    plt.show()
    pass


if __name__ == '__main__':
    main()
