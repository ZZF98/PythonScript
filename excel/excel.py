import xlwt

# 关于样式
style_head = xlwt.XFStyle()  # 初始化样式
red_style_head = xlwt.XFStyle()  # 初始化样式
green_style_head = xlwt.XFStyle()  # 初始化样式

font = xlwt.Font()  # 初始化字体相关
font.name = "微软雅黑"
font.bold = True
font.colour_index = 0  # TODO 必须是数字索引

font_s = xlwt.Font()  # 初始化字体相关
font_s.name = "微软雅黑"
font_s.bold = True
font_s.colour_index = 1  # TODO 必须是数字索引

red_bg = xlwt.Pattern()  # 初始背景图案
red_bg.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x1
red_bg.pattern_fore_colour = 2  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray

green_bg = xlwt.Pattern()  # 初始背景图案
green_bg.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x1
green_bg.pattern_fore_colour = 3

# 设置字体
style_head.font = font

red_style_head.font = font_s
green_style_head.font = font_s
# 设置背景
red_style_head.pattern = red_bg
green_style_head.pattern = green_bg

# 创建一个excel
excel = xlwt.Workbook()
# 添加工作区
sheet = excel.add_sheet("数据报表")

# 标题信息
head = ["序列号", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "1", "13", "14", "15", "16",
        "17",
        "18", "19", "20", "21", "22", "23"]
for index, value in enumerate(head):
    sheet.write(0, index, value, style_head)

# 内容信息
content = [("Caaaaaa","0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0",
            "1", "0", "1", "0", "0")]
for index, value_list in enumerate(content, 1):
    for i, value in enumerate(value_list):
        if str(value) == '0':
            sheet.write(index, i, value, red_style_head)
        else:
            sheet.write(index, i, value, green_style_head)

# 保存excel
excel.save("write.xlsx")
