# -*- codeing = utf-8 -*-
# @Time : 2022/4/19 10:15
# @Author : Bochen Ren
# @File : 豆瓣.py
# @Software : python code

import sys
from bs4 import BeautifulSoup #网页解析，获取诗句
import re #正则表达式，进行文字匹配
import urllib.request,urllib.error #指定URL，获取网页数据
import xlwt #进行Excel操作
import sqlite3 #进行SQLite数据库操作

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):  #调用获取页面的信息函数10次
        url = baseurl + str(i*25)
        html = askURL(url) #保存返回值

        # 数据解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):  # soup.findall()在soup中查找符合要求的字符串
            data = []
            item = str(item)
            # print(item)
            # 添加电影链接
            link = re.findall(findMovieLink, item)[0]  # 通过正则表达式来查找链接
            data.append(link)
            # 添加图片链接
            src = re.findall(findImgSrc, item)[0]
            data.append(src)
            # 添加电影中外文名
            title = re.findall(findTitle, item)
            if (len(title) == 2):
                chineseTitle = title[0]
                data.append(chineseTitle)  # 添加中文名
                otherTitle = title[1].replace("/", "").strip()  # 去掉无关符号
                data.append(otherTitle)  # 添加外文名
            else:
                data.append(title[0])
                data.append(" ")  # 在excel表中留空/占位
            # 添加电影分数
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            # 添加电影评价人数
            judge = re.findall(findJudge, item)[0]
            data.append(judge)
            # 添加电影概述
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                data.append(inq[0].replace("。", ""))
            else:
                data.append(" ")
            # 添加电影相关信息
            bd = re.findall(findBd, item)[0].strip()  # 去掉前后空格
            bd = re.sub("<br(\s+)?/>(\s+)?", " ", bd)  # 去掉<br/>
            bd = re.sub("/", " ", bd)
            data.append(bd)
            datalist.append(data)
    return datalist

#得到指定一个URL的网页内容
def askURL(url):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 100.0.4896.127Safari / 537.36"
    }#我不是爬虫

    request = urllib.request.Request(url,headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html

#保存数据

#存储在Excel表中
def saveData(datalist,savepath):

    book = xlwt.Workbook(encoding="utf-8") #创建workbook
    sheet = book.add_sheet('豆瓣电影Top25',cell_overwrite_ok=True) #创建工作表
    col = ('电影链接','图片链接','电影中文名','电影外文名','评分','评价人数','电影概况','相关信息')
    for i in range(0,8):
        sheet.write(0,i,col[i])#列名
    for i in range(0,250):
        print(i)
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save('豆瓣电影top250.xls')

#存储在Sqlite数据库中
def saveData2DB(datalist,dbpath):
    creaetDB(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for i in range(len(data)):
            if i == 4 or i == 5:
                continue
            else:
                data[i] = '"'+data[i]+'"'

        sql = '''
            insert into movie250 (
            info_link,pic_link,cname,ename,score,rating,introduction,info)
            values(%s)'''%",".join(data) #"."jion(data)是将list data里的所有元素用,链接，%是将后面内容填到前面的占位符中去
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
#初始化建表
def creaetDB(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    sql = '''
        create table movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varcher,
        score numeric,
        rating numeric,
        introduction text,
        info text
        )
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()

def main():
    baseurl = "http://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    saveData(datalist,savepath)
    dbpath = "movie.db"
    saveData2DB(datalist,dbpath)

findMovieLink = re.compile(r'<a href="(.*?)">')  # 生成规则,.表示任意字符,*表示出现一次或多次,?表示前面的东西出现0次或一次
findImgSrc = re.compile(r'<img .*src="(.*?)"',re.S) #re.S让换行符包含在字符中
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)




if __name__ == "__main__":
    main()