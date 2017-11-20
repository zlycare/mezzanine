# -*- coding: utf-8 -*-

from bson_rpc.client import connect


conn = connect('10.80.236.161','10.30.49.170',8181)
# conn = connect('127.0.0.1',8181)
conn.use_service(['gen_keywords', 'gen_category', 'gen_search_index']);


def auto_gen_keywords_message(article_id, article_content):
    err, res = conn.gen_keywords(article_id, article_content)
    print str(res).decode('unicode_escape')


def auto_gen_category_message(article_id, article_content):
    err, res = conn.gen_category(article_id, article_content)
    print str(res).decode('unicode_escape')


def auto_gen_search_index_message(article_id, article_content):
    err, res = conn.gen_search_index(article_id, article_content)
    print str(res).decode('unicode_escape')
