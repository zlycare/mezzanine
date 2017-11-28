# -*- coding: utf-8 -*-

from bson_rpc.client import connect


conn = connect('10.80.236.161','10.30.49.170',8181)
# conn = connect('10.30.49.170',8181)
conn.use_service(['gen_keywords', 'gen_category', 'gen_search_index']);

arr_k_messages = []
arr_c_messages = []
arr_s_messages = []

def auto_gen_keywords_message(article_id, article_content):
    # 避免连续发送重复消息给Q（）
    if article_id in arr_k_messages:
        return
    else:
        arr_k_messages.append(article_id)
    print 'arr_k_messages count:',len(arr_k_messages)
    try:
        err, res = conn.gen_keywords(article_id, article_content)
        print str(res).decode('unicode_escape')
    except BaseException, e:
        print e


def auto_gen_category_message(article_id, article_content):
    # 避免连续发送重复消息给Q（）
    if article_id in arr_c_messages:
        return
    else:
        arr_c_messages.append(article_id)
    print 'arr_c_messages count:',len(arr_c_messages)
    try:
        err, res = conn.gen_category(article_id, article_content)
        print str(res).decode('unicode_escape')
    except BaseException, e:
        print e

def auto_gen_search_index_message(article_id, article_content):
    # 避免连续发送重复消息给Q（）
    if article_id in arr_s_messages:
        return
    else:
        arr_s_messages.append(article_id)
    print 'arr_s_messages count:',len(arr_s_messages)
    try:
        err, res = conn.gen_search_index(article_id, article_content)
        print str(res).decode('unicode_escape')
    except BaseException, e:
        print e