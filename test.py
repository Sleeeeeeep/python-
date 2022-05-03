# -*- codeing = utf-8 -*-
# @Time : 2022/5/3 11:47
# @Author : Bochen Ren
# @File : test.py
# @Software : douban

import jieba                            #分词的
from matplotlib import pyplot as plt    #绘图,数据可视化
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np
import sqlite3


#准备慈云所需要的词
con = sqlite3.connect("movie.db")
cur = con.cursor()
sql ='select introduction from movie250'
data = cur.execute(sql)
text =""
for item in data:
    text = text + item[0]
cur.close()
con.close()

#分词
cut = jieba.cut(text)
string = ' '.join(cut)
#print(len(string))

#图片获取及处理
img = Image.open(r'.\static\assets\img\小鹿剪影.jpg')#找到图片
img_array = np.array(img) #将图片转化为二维数组

#封装的wordcloud
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='simsun.ttc' #字体所在位置: C:\Windows\Fonts
    )
#传入词云
wc.generate_from_text(string)

#绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')#是否显示坐标轴

#plt.show()

plt.savefig(r'.\static\assets\img\word_white_background.jpg',dpi=500)






