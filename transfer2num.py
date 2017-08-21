#!/user/bin/python
#encoding:utf-8
# @author: yqq
dict ={u'零':0, u'壹':1, u'贰':2, u'叁':3, u'肆':4, u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9, u'拾':10, u'佰':100, u'仟':1000, u'万':10000,
       u'亿':100000000,u'角':0.1,u'分':0.01}
def getResultForDigit(a,encoding='utf-8'):
    if isinstance(a, str):
        a = a.decode(encoding)
    count = 0
    result = 0
    tmp = 0
    Billion = 0
    while count < len(a):
        tmpChr = a[count]
        tmpNum = dict.get(tmpChr, None)
        #如果等于1亿
        if tmpNum == 100000000:
            result = result + tmp
            result = result * tmpNum
            #获得亿以上的数量，将其保存在中间变量Billion中并清空result
            Billion = Billion * 100000000 + result
            result = 0
            tmp = 0
        #如果等于1万
        elif tmpNum == 10000:
            result = result + tmp
            result = result * tmpNum
            tmp = 0
        #如果等于十或者百，千
        elif tmpNum >= 10:
            if tmp == 0:
                tmp = 1
            result =result+tmpNum * tmp
            tmp = 0
            #如果是个位数
        elif tmpNum >=1:
            tmp = tmp * 10 + tmpNum

        #分 角
        elif tmpNum >=0.1:
            if tmp == 0:
                tmp = 1
            result = result + tmpNum * tmp
            tmp = 0

        elif tmpNum >=0.01:
            if tmp == 0:
                tmp = 1
            result = result + tmpNum * tmp
            tmp = 0

        count += 1
    result = result + tmp
    result = result + Billion
    return result