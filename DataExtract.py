#!/user/bin/python
# encoding:utf-8
#@author yqq

import xlrd
import xlwt
import re
from transfer2num import getResultForDigit
from transfer2date import getDigitDate
file_path = "E:/ZBall.xlsx"
pattern1 = re.compile(r'[A-Z][\w\d]{1,8}.[\w\d]{1,2}.\d{1,5}.[A-Z]{1,5}|[A-Z][\w\d]{2,15}.\d{3}')#采购编号
pattern2 = re.compile(r'项目名称[^\n|\s]*[:：]{1}[\S]*')#项目采购名称 项目名称[^\n|\s]*[:：]{1}[\S]*
pattern3 = re.compile(r'[零壹贰叁肆伍陆柒捌玖拾佰仟万亿元圆角]{1,20}[分整]?')#采购金额 中标.*?[零壹贰叁肆伍陆柒捌玖拾佰仟万亿元圆角]{1,20}[分整]?
pattern32 =re.compile(r'\d{0,3}[,，]?\d{0,3}[,，]?\d{0,3}[,，]?\d{1,3}\W?\d{0,3}\W{0,3}元')  #采购金额不是大写中文
pattern4 = re.compile(r'联.{0,3}系.{0,3}人.{0,30}\W.{0,20}电.{0,3}话.{0,6}?\W*?\d{4}.\d{6,7}') #采购联系人

pattern5 = re.compile(r'.{0,4}年.{1,3}月.{1,4}日') #日期
pattern6 = re.compile(r'采购.{0,5}[构人称位]{1}[:：]{1}.*?[局校司所厂学心队站会处室院]') #采购人名称
pattern7 = re.compile(r'地\W{0,4}址\W.*?[号层室厂部栋厦楼)）]') #采购人地址
pattern8 = re.compile(r'中标.{0,5}[:：]{1}.{1,16}[厂司处所局院校站坊部]') #中标供应商名称
# 中标[^\n]\W{0,5}名称[:：]{1}(.*)[厂司处所局厅院校站]
pattern9 = re.compile(r'中标.{1,5}地址[:：]{1}.*?[号层室厂部栋厦]{1}|中标.{1,5}地址[:：]{1}.*?[\S]*') #中标供应商地址
pattern10 = re.compile(r'[（(]{1}[A-Z][\w\d]{1,8}.[\w\d]{1,2}.\d{1,5}.[A-Z]{1,5}[）)]{1}|[（(]{1}[A-Z][\w\d]{2,15}.\d{3}[）)]{1}')#去除名称里面的编号
pattern11 = re.compile(r'中标.{0,5}地址[:：]{1}.*') #去除中标供应商里面的地址
pattern62 =re.compile(r'招\W{0,3}标{0,3}人\W*[局校司所院厂学心队会处站室]{1}') #采购人特殊情况，写了招标人
pattern63 =re.compile(r'采购项目名称(.*?)\n')        #去除采购人名称里面的采购项目名称

pattern12 = re.compile(r'#及电话\W{1,3}[\S]|#\W{1,3}[\S]') #采购联系人
pattern13 =re.compile(r'\d{4}.\d{6,7}')#联系人电话或者传真
pattern_if1 = re.compile(r'中标.{0,4}公告如下.{1}|中标.{0,5}信息.{1}')

def handle_excel():   #读取excel，进行筛选
    dataall = xlrd.open_workbook(file_path)
    dataall.sheet_names()
    sheetzb_name = dataall.sheet_names()[0]
    sheetzb = dataall.sheet_by_name(sheetzb_name)
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    style = xlwt.XFStyle()  # 初始化样式
    style.alignment.wrap = 1
    row0 = [u'采购编号', u'项目名称', u'中标金额', u'联系人', u'电话',u'日期', u'供应商名称',u'供应商地址', u'采购人',u'采购人地标']
    # 生成第一行
    for i in range(len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 200, True))
    m=swap=0

    for i in range(sheetzb.nrows):
        for record in sheetzb.row_values(i):
            record_new = record.replace('\t', '').replace(' ','')
            match_if1 = re.search(pattern_if1,record_new)
            if match_if1: #中标判断
                match1 = re.findall(pattern1, record_new)  # 采购编号
                if match1:
                    m += 1
                    a = match1[0]
                    sheet1.write(m,0,a)
                    swap += 1
                    match2 = re.findall(pattern2, record_new) #项目名称
                    if match2:
                        for temp in match2:
                            temp_new = re.split(u'：|说',temp)
                            temp_new2=temp_new[1].replace(u'二、采购项目简要','').replace(u'。','').replace(u'（编号','').replace(u'采购编号','').replace(u'（采购编号','').replace(u'[采购编号','')
                            temp_new3=re.sub(pattern10,u'',temp_new2)
                            sheet1.write(swap,1,temp_new3)
                    match3 = re.findall(pattern3, record_new)  # 中标金额
                    if match3:
                        list3 = []
                        for temp1 in match3:
                            temp1_new = temp1.replace(u'人民币', '').replace(u'整', '')
                            moneydigit = getResultForDigit(temp1_new)
                            if moneydigit <=100:
                                moneydigit=u''
                            list3.append(str(moneydigit))
                        list32str ='\n'.join(list3)
                        sheet1.write(swap, 2, list32str,style)
                    else:
                        match32 = re.findall(pattern32,record_new)   #金额不是中文大写情况，用这个正则匹配
                        if match32:
                            for temp32 in match32:
                                sheet1.write(swap,2,temp32)
                    match4 = re.findall(pattern4,record_new)   #联系人，电话第一次筛选
                    if match4:
                        list4=[]
                        for temp2 in match4:
                            temp2_new=temp2.replace(u':','').replace(u'：','').replace(u'联系人','#').replace(u'\n','')
                            list4.append(temp2_new)
                        list42str = ''.join(list4[0]) #只取第一个联系人，为采购联系人
                        match10 = re.findall(pattern12,list42str)  #联系人
                        if match10:
                            for temp21 in match10:
                                temp21_new=temp21.replace(u'#及电话','').replace(u'#','').replace(u'；','').replace(u';','').replace(u'，','').replace(u',','').replace(u'电','').replace(u'联系','').replace(u'。','').replace(u'、','').replace(u'联','')
                                sheet1.write(swap,3,temp21_new)
                        match11 = re.findall(pattern13,list42str)  #联系人电话或者传真
                        if match11:
                            for temp22 in match11:
                                sheet1.write(swap,4,temp22)

                    match5 = re.findall(pattern5,record_new)  #日期
                    if match5:
                        digitdate = getDigitDate(match5[-1])
                        sheet1.write(swap,5,digitdate)
                    match8 = re.findall(pattern8,record_new) #供应商名称
                    if match8:
                        list8=[]
                        for temp8 in match8:
                            temp8_new=temp8.replace(u'中标单位名称：','').replace(u'中标供应商名称：','').replace(u'中标人名称：','').replace(u'中标供应商名称:','').replace(u'中标人','')
                            temp8_new2=re.sub(pattern11,'',temp8_new)
                            list8.append(temp8_new2)
                        list82str = '\n'.join(list8)
                        sheet1.write(swap,6,list82str,style)
                    match9 = re.findall(pattern9,record_new) #供应商地址
                    if match9:
                        list9=[]
                        for temp9 in match9:
                            listtemp9=list(temp9)   #把temp9这组tuple转成list（tuple里面是list）
                            temp92str=''.join(listtemp9)    #list转成str
                            list9.append(temp92str)     #str存到list里面
                        list92str = '\n'.join(list9) #把上个list转成str
                        sheet1.write(swap,7,list92str,style)
                    match6 = re.findall(pattern6, record_new)  # 采购人名称
                    if match6:
                        list6=[]
                        for temp3 in match6:
                            list6.append(temp3)
                        list62str = '\n'.join(list6)
                        list62str_new = re.sub(pattern63,'',list62str) #去除采购人名称里的采购项目名称
                        sheet1.write(swap,8,list62str_new,style)
                    else:
                        match62 =re.findall(pattern62,record_new) #采购人写了招标人
                        if match62:
                            list62=[]
                            for temp62 in match62:
                                list62.append(temp62)
                                list622str = '\n'.join(list62)
                            sheet1.write(swap,8,list622str,style)
                    match7 = re.findall(pattern7,record_new)   #采购人地址
                    if match7:
                        list7=[]
                        for temp7 in match7:
                            list7.append(temp7)
                            num = len(list7)-len(list6)
                            if num>=1:
                                for order in range(num,len(list7)):
                                    list72str = '\n'.join(list7[order])
                                sheet1.write(swap, 9, list72str, style)
                            else:
                                list73str = '\n'.join(list7)
                            sheet1.write(swap, 9, list73str,style)

    f.save('YYYYYY.xls')
def set_style(name, height,bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    return style



if __name__ == '__main__':
    handle_excel()




