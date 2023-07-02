from datetime import datetime
from elasticsearch import Elasticsearch


es_url = "http://192.168.2.10:9200"
es = Elasticsearch(es_url)

# Call an API, in this example `info()`
# resp = es.info()
# print(resp)

# 删除索引Index
# result = es.indices.delete(index='test-index', ignore=[400, 404])
# print(result)

# 创建索引Index
# result = es.indices.create(index='test-index', ignore=400)
# print(result)

# 插入几条数据
datas = [
    {
        'title': '美国留给伊拉克的是个烂摊子吗',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16'
    },
    {
        'title': '公安部：各地校车将享最高路权',
        'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
        'date': '2011-12-16'
    },
    {
        'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
        'url': 'https://news.qq.com/a/20111216/001044.htm',
        'date': '2011-12-17'
    },
    {
        'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
        'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
        'date': '2011-12-18'
    }
]

# for i,data in enumerate(datas):
#     resp = es.index(index='test-index', document=data, id=i)
#     print(resp)

# 查看索引数据
result = es.search(index='test-index', query={"match_all": {}})
print(result)