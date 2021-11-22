# -*- coding:utf-8 -*-

from time import time
import pandas as pd
import datetime
import random
import requests
from concurrent.futures import  ThreadPoolExecutor
import re
import jieba
import collections
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts import options as opts
from pyecharts.globals import ThemeType, CurrentConfig

t0 = time()

# start = '20211119'
# end = '20211120'
#
# # 生成时间序列
# date_list = [x for x in pd.date_range(start, end).strftime('%Y-%m-%d')]
# print(date_list)

# 开始生成爬虫代码
user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
]
start_time = datetime.datetime.now()


def grab_barrage(date):
    # 伪造请求头
    headers = {
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/bangumi/play/ep429796?from_spmid=666.9.banner.0',
        'cookie': "b_ut=-1; i-wanna-go-back=-1; _uuid=2931F8D9-6D62-461D-4362-67BC69BD50FE02912infoc; buvid3=6E1EE096-0EFD-4726-9BE0-AC9808384539167616infoc; fingerprint=41bedeba0086e34dc4186a7fcc372d76; buvid_fp=6E1EE096-0EFD-4726-9BE0-AC9808384539167616infoc; buvid_fp_plain=888533D6-8527-4561-91AE-5114877DF339148806infoc; DedeUserID=323037864; DedeUserID__ckMd5=63dbd00feb8d51f4; SESSDATA=e823bb6e%2C1649241143%2C3f48b*a1; bili_jct=4fbdb6d5efd6820ef02c9a184d0b7ced; blackside_state=1; rpdid=|(umuum~)|mY0J'uYJJY)mYRl; CURRENT_QUALITY=0; video_page_version=v_new_home_9; LIVE_BUVID=AUTO5416367780721269; sid=9yyxq64a; bp_video_offset_323037864=595526077779213300; bp_t_offset_323037864=595526077779213300; innersign=1; CURRENT_FNVAL=80; PVID=3; CURRENT_BLACKGAP=1",
        'user-agent': random.choice(user_agent)
    }
    # 构造url访问 需要用到的参数
    params = {
        'type': 1,
        'oid': '443749621',
        'date': date
    }
    # 发送请求 获取响应
    response = requests.get(url, params=params, headers=headers)
    response.encoding = 'utf-8'
    print(response.text)
    # comment = re.findall("(?<=:).*?(?=@)", response.text)
    # comment = re.findall(".*?([\u4E00-\u9FA5]+).*?", response.text)
    # with open("danmu_test.txt", 'w', encoding='utf-8') as df:
    #     for words in comment:
    #         df.write(words + '\n')
    # print(comment)


t1 = time()
print("Time cost:", t1-t0)


def main():
    # 开始多线程爬取 提高爬取效率
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(grab_barrage, date_list)

    # 计算所用时间
    delta = (datetime.datetime.now() - start_time).total_seconds()
    print(f'用时：{delta}s')


def create_word_cloud(all_words):
    word_counts = collections.Counter(all_words)
    word_counts_top100 = word_counts.most_common(100)
    print(word_counts_top100)
    word1 = WordCloud(init_opts=opts.InitOpts(width='1350px', height='750px', theme=ThemeType.MACARONS))
    word1.add('词频', data_pair=word_counts_top100,
              word_size_range=[15, 108], textstyle_opts=opts.TextStyleOpts(font_family='cursive'),
              shape=SymbolType.ROUND_RECT)
    word1.set_global_opts(title_opts=opts.TitleOpts('弹幕词云图'),
                          toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical'),
                          tooltip_opts=opts.TooltipOpts(is_show=True, background_color='red', border_color='yellow'))
    word1.render("弹幕词云图.html")


def delete_stop_word(words_list):
    stop_word = ['!', '，', '！', '？', '�']
    flag = False
    for w in words_list:
        if w in stop_word:
            flag = True
            words_list.remove(w)
    if flag:
        # print("删除停用词")
        pass
    return words_list


def analysis(sentence):
    split_sentence = jieba.cut(sentence, cut_all=False)
    return delete_stop_word(list(split_sentence))


def read_file(file):
    words_list = list()
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            # print(line[1:].strip('\n'))
            split_list = analysis(line[1:].strip('\n'))
            words_list += split_list
    print(len(words_list))
    # print(words_list)
    create_word_cloud(words_list)


if __name__ == '__main__':
    url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?'
    start = '20211117'
    end = '20211121'

    # 生成时间序列
    date_list = [x for x in pd.date_range(start, end).strftime('%Y-%m-%d')]
    # print(date_list)
    count = 0

    # 调用主函数
    main()

    # 读取文件
    # read_file('danmu_test.txt')

