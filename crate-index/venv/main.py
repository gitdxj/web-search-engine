
import json
import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, STORED, TEXT, ID
from jieba.analyse import ChineseAnalyzer

filename = open("tencent.json", "r")
content = filename.read()
data = json.loads(content)

if not os.path.exists("index"):
    os.mkdir("index")

schema = Schema(positionname=TEXT(stored=True, analyzer=ChineseAnalyzer()), 
link=TEXT(stored=True), positiontype=ID(stored=True),workLocation=ID(stored=True))
ix = create_in("index", schema)

writer = ix.writer()
cout = 1
for each_info in data:
    writer.add_document(positionname=each_info['positionname'], link=each_info['positionlink'],
     positiontype=each_info['positionType'], workLocation=each_info['workLocation'])
    print(str(cout) + ":" + each_info['positionname']+'\n')
    cout = cout+1
writer.commit()


