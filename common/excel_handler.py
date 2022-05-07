
# TODO:excel 的封装

import openpyxl

# 定义一个 ExcelHandler 类
class ExcelHandler:
    def __init__(self,file_path):
        """ 初始化 传入文件路径 """
        self.file = file_path
        self.worlk_book = None
    def open_file(self):
        """ 打开excel方法 """
        worlk_book = openpyxl.load_workbook(self.file)
        self.worlk_book = worlk_book
        return worlk_book

    def get_sheet(self,name):
        """ 获取表格/sheet 的方法 """
        sheet = self.open_file()
        return sheet[name]

    def read_data(self,name):
        """ 读取数据，读取表格/sheet 数据方法"""
        sheet = self.get_sheet(name)

        rows = list(sheet.rows)
        data = []
        headers = []
        for title in rows[0]:
            headers.append(title.value)
        for row in rows[1:]:
            row_data = {}
            for i, cell in enumerate(row):
                row_data[headers[i]] = cell.value
            data.append(row_data)
        return data

    def write(self,sheet_name,row,column,data):
        """ 写入单元格数据 """
        sheet = self.get_sheet(sheet_name)
        sheet.cell(row,column).value = data
        self.save()
        self.close()

    def save(self):
        """ 保存 """
        self.worlk_book.save(self.file)
    def close(self):
        """ 关闭文件 """
        self.worlk_book.close()

if __name__ == '__main__':
    pass



