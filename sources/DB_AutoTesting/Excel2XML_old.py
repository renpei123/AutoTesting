import xlrd
import datetime
import time
import sys
import xml.dom.minidom
import os

print
sys.getdefaultencoding()
reload(sys)  # 就是这么坑爹,否则下面会报错
sys.setdefaultencoding('utf-8')  # py默认是ascii。。要设成utf8


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)  # xlrd 操作excel的外部库
        return data
    except Exception, e:
        print str(e)


bgntm = '2017-05-18_'


def get_time_t(stime):
    stime = bgntm + stime + ':00'
    # return time.strptime(stime, '%Y-%m-%d %H:%M:%S')      #将时间转成时间戳
    return stime

def convert_xlsx_to_dict_array(self,file_name):
    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    columns = table.row_values(0)
    result_list = []
    for i in range(1,nrows):
        value = table.row_values(i)
        row = dict()
        for i in range(len(columns)):
            row[columns[i]] = value[i]
            result_list.append(row)
    return result_list


def excel_table_byindex(file, colnnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    col_name = table.row_value(0)
    doc = xml.dom.minidom.Document()  # 打开xml对象
    xmain = doc.createElement('main')
    doc.appendChild(xmain)
    for nrow in range(0, nrows):  # 遍历每一行
        if nrow == 0:
            continue

        uid = table.cell(nrow, 0).value  # 取值..第一列

        item = doc.createElement('%d' % uid)  # 生成节点
        stime = table.cell(nrow, 1).value  # 第二列的值
        stime = stime.strip()  # 去除空格..excel数据里 经常会无意有蛋疼的多余空格
        listT = stime.split('-')  # 按 -分割字符串

        # sbgn = 'bgn = %d'%time.mktime(get_time_t(listT[0]))
        sbgn = 'bgn = ' + get_time_t(listT[0])
        print
        'uid=%d' % uid
        print
        'bgn:' + sbgn
        send = 'end = ' + get_time_t(listT[1])
        # send = 'end = %d'%time.mktime(get_time_t(listT[1]))
        print
        'end:' + send
        exxbgn = doc.createTextNode(sbgn)  # 纯文本节点
        exxend = doc.createTextNode(send)
        item.appendChild(exxbgn)  # 加入树中
        item.appendChild(exxend)

        # ebgn = doc.createElement('bgn')
        # eend = doc.createElement('bgn')
        # item.appendChild(ebgn)
        # item.appendChild(eend)

        # item.setAttribute('bgn', '%d'%time.mktime(get_time_t(listT[0]))) #设置节点属性
        # item.setAttribute('end', '%d'%time.mktime(get_time_t(listT[1])))
        # for lt in listT:
        # print time.mktime(get_time_t(lt))

        xmain.appendChild(item)

    f = open('G:/testPro/py/exceltoxml/day.xml', 'w')  # xml文件输出路径
    f.write(doc.toprettyxml())
    f.close()


excel_table_byindex('G:/testPro/py/exceltoxml/day.xlsx')