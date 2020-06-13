import xlrd
from xlutils.copy import copy

if __name__ == '__main__':
    # 读取
    wb = xlrd.open_workbook('instrument.xlsx')
    sheetNameArr = wb.sheet_names()

    sheet = wb.sheet_by_name(sheetNameArr[0])
    # copy,获取sheet
    workbooknew = copy(wb)
    ws = workbooknew.get_sheet(0)
    print(sheet.nrows, sheet.ncols)
    col0 = ''
    col1 = ''
    col2 = ''

    row_r = 0
    for row in range(sheet.nrows):
        print(row_r, sheet.cell(row, 0).value, sheet.cell(row, 1).value, sheet.cell(row, 2).value)

        if col0 == '':
            col0 = sheet.cell(row, 0).value
        if col1 == '':
            col1 = sheet.cell(row, 1).value
        if col2 == '':
            col2 = sheet.cell(row, 2).value

        if row_r != 0:
            if col0 == sheet.cell(row, 0).value:
                ws.write(row, 0, '')
            else:
                col0 = sheet.cell(row, 0).value
            if col1 == sheet.cell(row, 1).value:
                ws.write(row, 1, '')
            else:
                col1 = sheet.cell(row, 1).value
            if col2 == sheet.cell(row, 2).value:
                ws.write(row, 2, '')
            else:
                col2 = sheet.cell(row, 2).value

        row_r = row_r + 1
        # print(sheet.cell(row, 1).value)
        # print(sheet.cell(row, 2).value)
    workbooknew.save(u'instrument_copy.xlsx')
