from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import *


# 返回结果列表
def search_results(search_content):
    ix = open_dir("index")
    searcher = ix.searcher()
    parser = QueryParser("positionname", ix.schema)
    myquery = parser.parse(search_content)
    results = searcher.search(myquery, limit=None)
    result_list = []
    for result in results:
        item = {}
        item['positionname'] = result['positionname']
        item['link'] = result['link']
        result_list.append(item)
    return result_list

if __name__ == '__main__':
    result = search_results("java工程师")
    print(result)
    # for each in result:
    #     print(each)