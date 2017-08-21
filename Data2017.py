#!/user/bin/python
# encoding:utf-8
#@author yqq

import xlrd
import xlwt
import re
'''import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )'''

file_path = "E:/olddata.xls"  #  记得修改这里的路径和文件名

pattern = re.compile(r'20170[123]\d{1,2}')  #匹配2017 1 2 3月的记录

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
    for x in range(len(row0)):
        sheet1.write(0, x, row0[x], set_style('Times New Roman', 200, True))

    for i in range(sheetzb.nrows):
        for j in range(sheetzb.ncols):
            match=re.search(pattern,str(sheetzb.cell(i,5).value))
            if match:
                    sheet1.write(i,0,sheetzb.cell(i,0).value)
                    sheet1.write(i,1,sheetzb.cell(i,1).value)
                    sheet1.write(i,2,sheetzb.cell(i,2).value)
                    sheet1.write(i,3,sheetzb.cell(i,3).value)
                    sheet1.write(i,4,sheetzb.cell(i,4).value)
                    sheet1.write(i,5,sheetzb.cell(i,5).value)
                    sheet1.write(i,6,sheetzb.cell(i,6).value)
                    sheet1.write(i,7,sheetzb.cell(i,7).value)
                    sheet1.write(i,8,sheetzb.cell(i,8).value)
                    sheet1.write(i,9,sheetzb.cell(i,9).value)
    f.save('Data2017.xls')
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




