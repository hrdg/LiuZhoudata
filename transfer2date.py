
# encoding:utf-8
#@author yqq

import re


dict = {
    u'○':u'0',u'〇':u'0',u'0':u'0',u'零':u'0',u'元':'1',u'一':u'1',u'二':u'2',u'三':u'3',u'四':u'4',u'五':u'5',u'六':u'6',u'七':u'7',u'八':u'8',u'九':u'9',u'十':u'10',
    u'十一':u'11',u'十二':u'12',u'十三':u'13',u'十四':u'14',u'十五':u'15',u'十六':u'16',u'十七':u'17',u'十八':u'18',u'十九':u'19',u'二十':u'20',u'二十一':u'21',
    u'二十二':u'22',u'二十三':u'23',u'二十四':u'24',u'二十五':u'25',u'二十六':u'26',u'二十七':u'27',u'二十八':u'28',u'二十九':u'29',u'三十':u'30',u'三十一':u'31'
}
def getDigitDate(a,encoding='utf-8'):
    if isinstance(a, str):
        a = a.decode(encoding)
    s =re.split(u'年|月|日',a)#分成三个字符串处理
    for i in s[0]:
        swap1 = dict.get(i,None)
        if swap1:
            data1=s[0].replace(i,swap1)
            s[0]=data1
        else:
            data1=s[0]
    swap2 = dict.get(s[1],None)
    if swap2:
        data2 = s[1].replace(s[1],swap2)
    else:
        data2=s[1]
    swap3 = dict.get(s[2],None)
    if swap3:
        data3 = s[2].replace(s[2],swap3)
    else:
        data3=s[2]
    if len(data2)==1:
        data2_new=u'0'+data2
    else:
        data2_new = data2
    if len(data3)==1:
        data3_new=u'0'+data3
    else:
        data3_new=data3
    data = data1+data2_new+data3_new
    return data


