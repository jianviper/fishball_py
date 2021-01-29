#!/usr/bin/env python
#coding:utf-8
import time

import requests, sys, xlwt
from datetime import datetime, timedelta

word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'
COOKIES = \
    'BDUSS' \
    '=ZpZEZLbXBCZTUzczFvTndGT0oyNVl2M2Nkd2FndlEtY0ljR1psRGRKaUtvamhnSVFBQUFBJCQAAAAAAAAAAAEAAAD10vMANDAyMjAwMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIoVEWCKFRFgfj'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': COOKIES,
    'DNT': '1',
    'Host': 'index.baidu.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://index.baidu.com/v2/main/index.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def decrypt(t, e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n) / 2)
    start = n[ln:]
    end = n[:ln]
    for j, k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)


def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={0}'
    resp = requests.get(url.format(uniqid), headers=headers)
    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')


def get_index_data(keyword, start='2011-01-01', end='2021-01-27', k=''):
    keyword = str(keyword).replace("'", '"')
    url = f'http://index.baidu.com/api/SearchApi/index?area=0&word={keyword}&area=0&startDate={start}&endDate={end}'
    # print(url)

    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print('获取指数失败')
        sys.exit(1)

    content = resp.json()
    data = content.get('data')
    user_indexes = data.get('userIndexes')[0]
    uniqid = data.get('uniqid')
    ptbk = get_ptbk(uniqid)

    while ptbk is None or ptbk == '':
        ptbk = get_ptbk(uniqid)

    all_data = user_indexes.get('all').get('data')
    result = decrypt(ptbk, all_data)
    result = result.split(',')

    weeks = len(result)
    date_list = date(start, end, weeks)

    return [date_list, result]


def date(start, end, weeks):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    # print(start_date, end_date, weeks)
    s, e = None, None

    # days = (end_date - start_date).days
    date_list = []
    for i in range(weeks):
        s = start_date + timedelta(days=i * 7)  #开始时间
        e = s + timedelta(days=7)  #一周结束时间
        if i == 0:
            e = s + timedelta(days=6)

        # print(i + 1, s.strftime('%Y-%m-%d'), '-', e.strftime('%Y-%m-%d'))
        date_list.append((s.strftime('%Y-%m-%d')))
    # print(date_list)
    return date_list


def write_to_excel(result: list, name: list, type=1, filename=''):
    '''
    :param result: 结果列表，格式：[date,data]
    :param name: 表头名称
    :param type: 0：横向，1：竖向
    :return:
    '''
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('My Worksheet')
    style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style.alignment = al
    # 写入excel
    # 参数对应 行, 列, 值
    if type == 0:
        for d in range(len(result)):  #横向排列
            worksheet.write_merge(d * 2 + 1, d * 2 + 1, 0, 0, name[d], style)
            if d == 0:
                for i in range(len(result[d][0])):  #日期
                    worksheet.write(d * 2, i + 1, label=result[d][0][i])
            for i in range(len(result[d][1])):  #数据
                worksheet.write(d * 2 + 1, i + 1, label=int(result[d][1][i]))
    elif type == 1:
        # 设置冻结为真
        worksheet.set_panes_frozen('1')
        # 水平冻结
        worksheet.set_horz_split_pos(1)
        for d in range(len(result)):  #竖向排列
            worksheet.write(0, d * 2 + 1, name[d], style)
            if d == 0:
                for i in range(len(result[d][0])):  #日期
                    worksheet.write(i + 1, d * 2, label=result[d][0][i])
            for i in range(len(result[d][1])):  #数据
                worksheet.write(i + 1, d * 2 + 1, label=int(result[d][1][i]), style=style)

    # 保存
    workbook.save(filename)


def export(date_range: list, keywords: list, file_name):
    result_list = []
    for k in keywords:
        words = [[{"name": k, "wordType": 1}]]
        result_list.append(get_index_data(words, date_range[0], date_range[1], k))
    write_to_excel(result_list, keywords, 1, file_name)


if __name__ == '__main__':
    key_word = ['在线会议', '腾讯会议', 'ZOOM', '小鱼易连', '瞩目', 'WELINK']
    key_word1 = ['任务管理', 'teambition', 'worktile', 'tower', 'trello', '明道云']
    file_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename = '[{0}]{1}.xls'.format('dota2', file_time)
    export(['2020-1-1', '2020-1-20'], ['dota2'], filename)
