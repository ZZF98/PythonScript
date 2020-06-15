import xlrd
import xlwt
from xlutils.copy import copy

# zq_data = {}
# add_zq_data = {}
# with open('department_copy1.json', 'r', encoding='UTF-8')as f:
#     data = json.load(f)
#     for data in data["RECORDS"]:
#         print(data["id"], data["name"])
#         zq_data[data["name"]] = data["id"]

data = xlrd.open_workbook("test.xlsx")
newWb = copy(data)  # 复制
# 获取工作区
newWs = newWb.get_sheet(0)
table = data.sheet_by_index(0)

for rowNum in range(table.nrows):
    rowVale = table.row_values(rowNum)
    if rowVale[12] != "":
        print(rowVale[12])
        newWs.write(rowNum, 13, "value")

newWb.save("new_test.xlsx")
