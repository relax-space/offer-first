'''
数据清洗: 
1. 类型设置: 用户名 内容 设置为string
2. 内容处理: 用户名和内容只保留中文
3. 缺失值处理: 用户名如果缺失,则赋值为无名氏
4. 时间点处理: 用小时:分钟:秒格式来表示
'''
import pandas as pd


def time_change(timepoint):
    m, s = divmod(timepoint, 60)
    h, m = divmod(m, 60)
    return f'{h:0>2}:{m:0>2}:{s:0>2}'


def clean_all():
    for i in range(1, 4):
        df = pd.read_csv(f'data/raw_{i}.csv')
        df['opername'] = df['opername'].fillna('无名氏')
        df['content'] = df['content'].str.extract(r'([\u4e00-\u9fa5]+)')
        # 删除所有空弹幕(可能是纯表情)
        df = df.dropna()

        df['timepoint'] = df['timepoint'].apply(time_change)
        
        df.to_csv(f'data/{i}.csv')


if __name__ == '__main__':
    clean_all()
