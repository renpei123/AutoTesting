# -*- coding: utf-8 -*-
#!/usr/bin/python
import json



def readConf():
    with open("table_dep.json",'r',encoding='utf-8') as f: 
        d = json.load(f)
    return d


def getBaseTableList():
    arrayDict = readConf()
    #tableList=[]
    tableList = list(arrayDict.keys())
    #print(type(arrayDict.keys()))
    return tableList

def getViewList(ViewType):
    #ViewType = "V"
    arrayDict = readConf()
    tableList = list(arrayDict.keys())
    viewList = []
    #print(type(arrayDict))
    for table in tableList:
        for view in arrayDict[table]:
            if view["TYPE"] == ViewType:
                viewList.append(view["NAME"])
    return viewList           

            
def getViewListByTable(TableName,ViewType):
    arrayDict = readConf()
    viewList = []
    for view in arrayDict[TableName]:
        if view["TYPE"] == ViewType:
            viewList.append(view["NAME"])
    return viewList



if __name__ == "__main__":
    print(getViewList("V"))
    print(getViewList("UV"))
    print(getViewListByTable("BDWDB.CHRG_DTL18","V"))

