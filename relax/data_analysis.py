'''
1. 各期弹幕数量对比
2. 谁是弹幕发射机
3. 会员等级分布
4. 弹幕在讨论些什么
5. 8个实习生提及次数对比
6. 大家如何评论8个实习生
7. 情感分析

uservip_degree
timepoint     
content       
opername      
upcount       
season   

'''

from doctest import FAIL_FAST

import jieba
import pandas as pd
import pyecharts.options as opts
import stylecloud
from pyecharts.charts import Bar, Pie
from pyecharts.commons.utils import JsCode


def ana_1(df: pd.DataFrame):
    # 1. 各期弹幕数量对比
    df1 = df['season'].value_counts().sort_index()
    Bar().add_xaxis(df1.index.tolist()).add_yaxis(
        '', df1.values.tolist()).render('data/1.html')


def ana_2(df: pd.DataFrame):
    # 2. 谁是弹幕发射机
    df1 = df['opername'].value_counts()
    # 去掉 索引值为 无名氏 的那一行数据
    df1 = df1[df1.index != '无名氏']
    df1 = df1[0:10]
    Bar().add_xaxis(df1.index.tolist()).add_yaxis(
        '', df1.values.tolist()).set_global_opts(xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=-15, interval=0))).render(
                'data/2.html')


def ana_3(df: pd.DataFrame):
    # 3. 会员等级分布
    df1 = df['uservip_degree'].value_counts()
    # 可以在JsCode里 用console.log打印, 然后在谷歌浏览器按F12查看
    Pie().add('', list(df1.items())).set_series_opts(
        label_opts=opts.LabelOpts(formatter=JsCode('''
            function(param){
                let name = param.name?param.name:0;
                let res =`等级${name}: ${param.percent}%`;
                return res;
            }
            '''),
                                  font_size=14)).render('data/3.html')


def ana_4(df: pd.DataFrame, stopwords: list):
    # 4. 弹幕在讨论些什么
    '''
    1. 弹幕分词
    2. 停用词
    3. 制作词云
    '''
    # new_words = [
    #     '撒贝宁', '范丞丞', '何炅', '周深', '杨天真', '徐灵菱', '王钊', '史欣悦', '郭涛', '梁春娟', '丁辉',
    #     '朱一暄', '李晋晔', '瞿泽林', '刘煜成', '王骁', '王颖飞', '詹秋怡', '何旻哲', '赵南希'
    # ]
    '''
    实习生: '丁辉','一暄', '晋晔', '泽林', '煜成', '王骁', '颖飞', '秋怡'
    踢馆: '旻哲', '南希'
    '''
    new_words = [
        '撒老师', '范丞丞', '何炅', '周深', '天真', '徐灵菱', '王钊', '欣悦', '郭涛', '梁春娟', '丁辉',
        '一暄', '晋晔', '泽林', '煜成', '王骁', '颖飞', '秋怡', '旻哲', '南希'
    ]
    for i in new_words:
        jieba.add_word(i)
    words = jieba.lcut(df['content'].str.cat(sep='$'))

    # 因为打印的图片中,这些无用的次太多,所以停用掉
    stopwords.extend(
        ['觉得', '真的', '应该', '其实', '好像', '感觉', '说', '哈', '哈哈', '哈哈哈', '哈哈哈哈'])
    stylecloud.gen_stylecloud(' '.join(words),
                              font_path='asset/HanYiKaiTiJian.ttf',
                              icon_name='fas fa-square',
                              custom_stopwords=stopwords,
                              max_words=100,
                              size=653,
                              output_name='data/4.png')


def ana_5(df: pd.DataFrame):
    # 5. 8个实习生提及次数对比
    df1 = df['focus'].value_counts()
    df1 = df1.drop(index=['无'])
    Bar().add_xaxis(df1.index.tolist()).add_yaxis(
        '', df1.values.tolist()).render('data/5.html')


def ana_6(df: pd.DataFrame, key_words: list, stopwords: list):
    # 6. 大家如何评论8个实习生
    stopwords.extend(
        ['觉得', '真的', '应该', '其实', '好像', '感觉', '说', '哈', '哈哈', '哈哈哈', '哈哈哈哈'])
    for i in key_words:
        jieba.add_word(i)
    for i in ['朱一暄', '李晋晔', '瞿泽林', '刘煜成', '王颖飞', '詹秋怡']:
        jieba.add_word(i)
    for i in key_words:
        df1 = df.query('focus == @i')
        words = jieba.lcut(df1['content'].str.cat(sep='$'))
        stylecloud.gen_stylecloud(' '.join(words),
                                  font_path='asset/HanYiKaiTiJian.ttf',
                                  icon_name='fas fa-heart',
                                  custom_stopwords=stopwords,
                                  output_name=f'data/6_{i}.png',
                                  max_words=100,
                                  size=653,
                                  collocations=False)


def find_intern(content: str, key_words: list):
    for i in key_words:
        if i in content:
            return i
    return '无'


def get_stopwords():
    with open(r'asset/stopword.txt', mode='r', encoding='utf8') as f:
        return [i.strip() for i in f.readlines()]



def main():
    df = pd.read_csv('data/2.csv', dtype={'content': 'string'})
    df = df.dropna()
    stopwords = get_stopwords()
    # ana_1(df)
    # ana_2(df)
    # ana_3(df)
    # ana_4(df, stopwords)

    # 增加一列 人物提及
    key_words = ['丁辉', '一暄', '晋晔', '泽林', '煜成', '王骁', '颖飞', '秋怡']
    df['focus'] = df['content'].apply(find_intern, args=(key_words, ))
    kong = '无'
    df = df.query('focus != @kong')
    # ana_5(df)
    ana_6(df, key_words, stopwords)


if __name__ == '__main__':
    main()
