# 导入os模块，用于处理文件和目录
import os
# 导入csv模块，用于读取csv文件
import csv
# 导入colorama模块，用于设置终端输出的颜色
from colorama import Fore, Back, Style, init
# 导入pandas模块，用于数据处理
import pandas as pd
# 导入matplotlib.pyplot模块，用于绘制图形
import matplotlib.pyplot as plt
# 导入jieba模块，用于中文分词
import jieba
# 导入wordcloud模块，用于生成词云
import wordcloud
# 导入matplotlib.gridspec模块，用于创建网格布局
import matplotlib.gridspec as gridspec
# 导入FuncAnimation模块，用于创建动画
from matplotlib.animation import FuncAnimation
# 导入matplotlib.image模块，用于读取图像
import matplotlib.image as mpimg
# 导入PIL模块，用于处理图像
from PIL import Image
# 导入pyecharts.charts模块，用于创建地图
from pyecharts.charts import Geo
# 导入pyecharts.options模块，用于设置地图样式
from pyecharts import options as opts
# 导入numpy模块，用于数值计算
import numpy as np
# 导入pygame模块，用于创建游戏
import pygame
# 导入random模块，用于生成随机数
import random
# 导入pi模块，用于计算圆周率
from math import pi
# 初始化colorama模块
init(autoreset=True)
# 定义文件名
fileName = "航天项目信息表1.csv"
# 定义项目列表
projects = []
# 读取CSV文件
def ReadProjectInfo(fileName):
    # 清空projects列表
    projects.clear()
    try:
        # 打开文件，以只读模式读取，编码格式为gbk
        with open(fileName, "r", encoding="gbk") as fo:
            # 使用csv.DictReader读取文件内容，将每一行转换为字典
            reader = csv.DictReader(fo)
            # 遍历每一行
            for row in reader:
                # 清理每一行的数据，去除空格
                cleaned_row = {
                    "序号": row.get("序号", "").strip(),
                    "项目名称": row.get("项目名称", "").strip(),
                    "启动年度": row.get("启动年度", "").strip(),
                    "完成年度": row.get("完成年度", "").strip(),
                    "成果状态": row.get("成果状态", "").strip(),
                    "所属机构": row.get("所属机构", "").strip(),
                    "项目类型": row.get("项目类型", "").strip()
                }
                # 将清理后的数据添加到projects列表中
                projects.append(cleaned_row)
    except FileNotFoundError:
        # 如果文件不存在，打印提示信息
        print(Fore.RED + "文件不存在，将创建新文件")

# 保存到CSV文件
def WriteProjectInfo(fileName):
    # 打开文件，以写入模式，编码为gbk，换行符为空
    with open(fileName, "w", encoding="gbk", newline="") as fo:
        # 定义字段名
        fieldnames = ["序号", "项目名称", "启动年度", "完成年度", "成果状态", "所属机构", "项目类型"]
        # 创建DictWriter对象
        writer = csv.DictWriter(fo, fieldnames=fieldnames)
        # 写入表头
        writer.writeheader()
        # 遍历projects列表，写入每一行数据
        for project in projects:
            writer.writerow(project)
    # 打印提示信息
    print(Fore.GREEN + "数据已保存！")

# 输入验证
def InputCheck(item, allow_empty=False):
    # 定义一个函数，用于检查输入是否为空
    while True:
        # 循环，直到输入不为空
        myitem = input(f"请输入{item}：").strip()
        # 输入一个字符串，并去除首尾空格
        if not allow_empty and not myitem:
            # 如果不允许为空，且输入为空，则输出错误信息
            print(Fore.RED + f"{item}不能为空！")
        else:
            # 否则，返回输入的字符串
            return myitem

# 按序号查找项目索引
# 根据项目ID搜索项目
def SearchByID(project_id):
    # 遍历项目列表
    for idx, project in enumerate(projects):
        # 如果项目ID与传入的ID相同
        if project["序号"] == project_id:
            # 返回项目在列表中的索引
            return idx
    # 如果没有找到匹配的项目，返回-1
    return -1

# UI界面
def ShowUI():
    # 清屏
    os.system("cls")
    # 定义颜色和样式
    TITLE = Fore.BLUE + Style.BRIGHT
    MENU = Fore.WHITE + Style.BRIGHT
    BORDER = Fore.CYAN
    ACCENT = Fore.YELLOW

    # 定义UI界面
    ui = f'''
    {BORDER}╭───────────────────────────────────────╮
    {BORDER}│ {TITLE}  ██████╗ ██████╗ ██╗  ██╗███████╗  {BORDER}│
    {BORDER}│ {TITLE}  ██╔══██╗██╔══██╗██║  ██║██╔════╝  {BORDER}│
    {BORDER}│ {TITLE}  ██████╔╝██████╔╝███████║█████╗    {BORDER}│
    {BORDER}│ {TITLE}  ██╔══██╗██╔═══╝ ██╔══██║██╔══╝    {BORDER}│
    {BORDER}│ {TITLE}  ██████╔╝██║     ██║  ██║███████╗  {BORDER}│
    {BORDER}│ {TITLE}  ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝  {BORDER}│
    {BORDER}├───────────────────────────────────────┤
    {BORDER}│ {ACCENT}🚀 航天项目智能管理系统 v终极版          {BORDER}│
    {BORDER}├───────────────────────────────────────┤
    {BORDER}│ {MENU} 1. {Fore.GREEN}📋 显示所有项目        {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 2. {Fore.GREEN}✨ 添加新项目          {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 3. {Fore.RED}🗑️ 删除项目            {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 4. {Fore.YELLOW}✏️ 修改项目信息        {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 5. {Fore.CYAN}💾 保存文件            {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 6. {Fore.CYAN}🔍 查询项目            {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 7. {Fore.BLUE}📊 数据分析           {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 8. {Fore.MAGENTA}📈 数据可视化         {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU} 9. {Fore.GREEN}🎮 启动航天游戏       {ACCENT}»»       {BORDER}│
    {BORDER}│ {MENU}10. {Fore.RED}🚪 退出系统           {ACCENT}»»       {BORDER}│
    {BORDER}╰───────────────────────────────────────╯
    {Style.RESET_ALL}
    '''
    # 打印UI界面
    print(ui)

# 显示所有项目（表格对齐）
def ShowAllProjects():
    os.system("cls")
    if not projects:
        print(Fore.YELLOW + "暂无项目信息！")
        input("\n按任意键返回")
        return
    # ---------- 排序选项 ----------
    print(Fore.CYAN + "排序方式：")
    print(Fore.WHITE + " 1. 按启动年度升序")
    print(Fore.WHITE + " 2. 按启动年度降序")
    print(Fore.WHITE + " 3. 不排序")
    sort_choice = input(Fore.YELLOW + "请选择排序方式（默认不排序）: ").strip()

    # 处理排序逻辑
    if sort_choice == "1":
        sorted_projects = sorted(
            projects,
            key=lambda x: int(x["启动年度"]) if x["启动年度"].isdigit() else 0
        )
    elif sort_choice == "2":
        sorted_projects = sorted(
            projects,
            key=lambda x: int(x["启动年度"]) if x["启动年度"].isdigit() else 0,
            reverse=True
        )
    else:
        sorted_projects = projects.copy()
     # 计算各列最大宽度
    col_width = {
        "序号": 4,
        "项目名称": 12,
        "启动年度": 8,
        "完成年度": 8,
        "成果状态": 8,
        "所属机构": 14,
        "项目类型": 12
    }
    # 动态计算列宽
    for proj in sorted_projects:
        for key in col_width:
            col_width[key] = max(col_width[key], len(str(proj.get(key, ""))) + 2)
    # 构建表格边框
    border_top = "┌" + "┬".join(["─" * col_width[key] for key in col_width]) + "┐"
    border_mid = "├" + "┼".join(["─" * col_width[key] for key in col_width]) + "┤"
    border_bot = "└" + "┴".join(["─" * col_width[key] for key in col_width]) + "┘"
    # 打印表头
    header = (
            Fore.CYAN +
            "│".join([
                "序号".ljust(col_width["序号"]),
                "项目名称".ljust(col_width["项目名称"]),
                "启动年度".ljust(col_width["启动年度"]),
                "完成年度".ljust(col_width["完成年度"]),
                "成果状态".ljust(col_width["成果状态"]),
                "所属机构".ljust(col_width["所属机构"]),
                "项目类型".ljust(col_width["项目类型"])
            ])
    )
    print(border_top)
    print(header)
    print(border_mid)
    # 打印数据行
    for proj in sorted_projects:
        row = "│".join([
            Fore.WHITE + proj["序号"].ljust(col_width["序号"]),
            Fore.GREEN + proj["项目名称"].ljust(col_width["项目名称"]),
            Fore.YELLOW + proj["启动年度"].ljust(col_width["启动年度"]),
            Fore.YELLOW + proj["完成年度"].ljust(col_width["完成年度"]),
            Fore.CYAN + proj["成果状态"].ljust(col_width["成果状态"]),
            Fore.MAGENTA + proj["所属机构"].ljust(col_width["所属机构"]),
            Fore.BLUE + proj["项目类型"].ljust(col_width["项目类型"])
        ])
        print(row)
    print(border_bot)
    input("\n按任意键返回")

# 添加项目
def AddProject():
    # 清屏
    os.system("cls")
    # 输入项目编号
    new_id = InputCheck("项目编号")
    # 检查编号是否已存在
    if SearchByID(new_id) != -1:
        # 如果编号已存在，输出提示信息
        print(Fore.RED + "编号已存在！")
        # 等待用户输入任意键返回
        input("按任意键返回")
        return

    # 创建新项目字典
    new_project = {
        "序号": new_id,
        "项目名称": InputCheck("项目名称"),
        "启动年度": InputCheck("启动年度"),
        "完成年度": InputCheck("完成年度（可空）", allow_empty=True),
        "成果状态": InputCheck("成果状态"),
        "所属机构": InputCheck("所属机构"),
        "项目类型": InputCheck("项目类型")
    }
    # 将新项目添加到项目列表中
    projects.append(new_project)
    # 将项目列表写入文件
    WriteProjectInfo(fileName)
    # 输出添加成功信息
    print(Fore.GREEN + "添加成功！")
    # 等待用户输入任意键返回
    input("按任意键返回")

# 删除项目
def DeleteProject():
    # 清屏
    os.system("cls")
    # 输入要删除的项目编号
    target_id = InputCheck("要删除的项目编号")
    # 根据项目编号查找项目
    idx = SearchByID(target_id)
    # 如果项目不存在
    if idx == -1:
        # 输出项目不存在
        print(Fore.RED + "项目不存在！")
    else:
        # 删除项目
        del projects[idx]
        # 写入项目信息
        WriteProjectInfo(fileName)
        # 输出删除成功
        print(Fore.GREEN + "删除成功！")
    # 按任意键返回
    input("按任意键返回")

# 修改项目
def ModifyProject():
    # 清屏
    os.system("cls")
    # 输入要修改的项目编号
    target_id = InputCheck("要修改的项目编号")
    # 根据项目编号查找项目
    idx = SearchByID(target_id)
    # 如果项目不存在，则输出提示信息并返回
    if idx == -1:
        print(Fore.RED + "项目不存在！")
        input("按任意键返回")
        return

    # 输出提示信息，表示留空表示不修改
    print(Fore.YELLOW + "留空表示不修改")
    # 获取要修改的项目
    project = projects[idx]
    # 遍历项目字段，依次输入新值
    for field in ["项目名称", "启动年度", "完成年度", "成果状态", "所属机构", "项目类型"]:
        new_value = InputCheck(f"新{field}", allow_empty=True)
        # 如果新值不为空，则更新项目字段
        if new_value:
            project[field] = new_value

    # 将修改后的项目信息写入文件
    WriteProjectInfo(fileName)
    # 输出修改成功信息
    print(Fore.GREEN + "修改成功！")
    # 等待用户输入任意键返回
    input("按任意键返回")

# 查询子菜单
def QueryMenu():
    # 无限循环，直到用户选择返回主菜单
    while True:
        # 清空屏幕
        os.system("cls")
        # 打印查询条件选择菜单
        print(Fore.CYAN + "┌───────────────┐")
        print(Fore.CYAN + "│ 查询条件选择   │")
        print(Fore.CYAN + "├───────────────┤")
        print(Fore.WHITE + " 1. 按启动年度查询")
        print(Fore.WHITE + " 2. 按项目类型查询")
        print(Fore.WHITE + " 3. 按所属机构查询")
        print(Fore.WHITE + " 4. 返回主菜单")
        print(Fore.CYAN + "└───────────────┘")
        # 获取用户输入的查询方式
        choice = input("请选择查询方式：")

        results = []
        # 根据用户选择的查询方式，执行相应的查询操作
        if choice == "1":
            # 按启动年度查询
            year = InputCheck("启动年度")
            results = [p for p in projects if p["启动年度"] == year]
        elif choice == "2":
            # 按项目类型查询
            ptype = InputCheck("项目类型")
            results = [p for p in projects if p["项目类型"] == ptype]
        elif choice == "3":
            # 按所属机构查询
            org = InputCheck("所属机构")
            results = [p for p in projects if p["所属机构"] == org]
        elif choice == "4":
            # 返回主菜单
            return
        else:
            # 无效选项
            print(Fore.RED + "无效选项！")
            input("按任意键重试")
            continue

        # 显示结果
        os.system("cls")
        if not results:
            # 未找到匹配项目
            print(Fore.YELLOW + "未找到匹配项目！")
        else:
            # 找到匹配项目
            print(Fore.CYAN + f"找到 {len(results)} 条结果：")
            for p in results:
                print(Fore.WHITE + "-" * 50)
                print(f"{Fore.YELLOW}项目名称：{Fore.GREEN}{p['项目名称']}")
                print(f"{Fore.YELLOW}启动年度：{p['启动年度']} | 完成年度：{p['完成年度']}")
                print(f"{Fore.YELLOW}所属机构：{p['所属机构']} | 类型：{p['项目类型']}")
                print(f"{Fore.YELLOW}成果状态：{p['成果状态']}")
        input("\n按任意键返回")

# 数据分析
def Static():
    while True:
        os.system("cls")
        df = pd.read_csv(fileName, encoding='gbk')
        print(Fore.CYAN + "┌───────────────┐")
        print(Fore.CYAN + "│ 查询条件选择   │")
        print(Fore.CYAN + "├───────────────┤")
        print(Fore.WHITE + " 1. 所属机构统计")
        print(Fore.WHITE + " 2. 已完成和持续进行统计")
        print(Fore.WHITE + " 3. 项目持续时间分析")
        print(Fore.WHITE + " 4. 详细统计指标")
        print(Fore.WHITE + " 5. 返回主菜单")
        print(Fore.CYAN + "└───────────────┘")
        n = input("请输入对应的数字: ")

        # 根据用户输入的数字，执行相应的操作
        if n == "1":
            # 统计所属机构
            print(df["所属机构"].value_counts())
        elif n == "2":
            # 统计已完成和持续进行的项目
            print(df["成果状态"].value_counts())
        elif n == "3":
            # 转换数值类型并处理异常值
            df['启动年度'] = pd.to_numeric(df['启动年度'], errors='coerce')
            df['完成年度'] = pd.to_numeric(df['完成年度'], errors='coerce')

            # 过滤有效数据
            valid_df = df.dropna(subset=['启动年度', '完成年度'])
            valid_df = valid_df[(valid_df['完成年度'] > valid_df['启动年度'])]

            # 计算并输出项目平均持续时间
            if not valid_df.empty:
                valid_df['项目持续时间'] = valid_df['完成年度'] - valid_df['启动年度']
                avg_duration = valid_df['项目持续时间'].mean()
                print(f"\n项目平均持续时间: {avg_duration:.1f}年")
                print("参与计算的项目：")
                print(valid_df[['项目名称', '启动年度', '完成年度', '项目持续时间']])
            else:
                print(Fore.YELLOW + "没有有效数据可计算平均持续时间")

        elif n == "4":
            # 转换数值类型并处理异常值
            df['启动年度'] = pd.to_numeric(df['启动年度'], errors='coerce')
            df['完成年度'] = pd.to_numeric(df['完成年度'], errors='coerce')
            valid_df = df.dropna(subset=['启动年度', '完成年度'])
            valid_df = valid_df[(valid_df['完成年度'] > valid_df['启动年度'])]

            # 计算并输出项目持续时间的详细统计指标
            if not valid_df.empty:
                valid_df['项目持续时间'] = valid_df['完成年度'] - valid_df['启动年度']
                print("\n项目持续时间详细统计：")
                print(f"平均值：{valid_df['项目持续时间'].mean():.1f}年")
                print(f"最大值：{valid_df['项目持续时间'].max()}年")
                print(f"最小值：{valid_df['项目持续时间'].min()}年")
                print(f"中位数：{valid_df['项目持续时间'].median()}年")
                print(f"总和：{valid_df['项目持续时间'].sum()}年")
                print(f"方差：{valid_df['项目持续时间'].var():.1f}")
            else:
                print(Fore.YELLOW + "无有效数据")
        elif n=='5':
            # 返回主菜单
            return
        input("\n按任意键返回")

# 数据可视化
def Picture():
    # 无限循环
    while True:
        # 清屏
        os.system("cls")
        # 打印菜单
        print(Fore.CYAN + '''
        ┌───────────────┐
        │ 可视化菜单     │
        ├───────────────┤
         1. 机构分布饼图
         2. 发射数量趋势
         3. 持续时间散点
         4. 生成词云
         5. 基地分布图
         6. 图片轮播
         7. 机构柱状图
         8. 项目雷达图
         9. 返回主菜单
        └───────────────┘''')
        # 输入选择
        n = input("请选择（回车返回）: ").strip()
        # 如果输入为空，则返回
        if not n: return
        try:
            # 设置字体为黑体
            plt.rcParams['font.sans-serif'] = ['SimHei']
            # 解决负号'-'显示为方块的问题
            plt.rcParams['axes.unicode_minus'] = False
            # 如果n等于1
            if n == "1":
                # 读取csv文件，编码格式为gbk
                df = pd.read_csv(fileName, encoding='gbk')
                # 统计所属机构的数量
                counts = df["所属机构"].value_counts()
                # 创建一个10x10的画布
                plt.figure(figsize=(10, 10))
                # 绘制饼图，标签为所属机构，百分比格式为1.1f
                plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
                # 设置标题为所属机构分布
                plt.title("所属机构分布")
                # 显示图例
                plt.legend()
                # 显示图形
                plt.show()
            elif n == "2":
                # 使用ggplot样式
                plt.style.use('ggplot')
                # 创建一个16x6的图形
                plt.figure(figsize=(16, 6))
                # 创建一个字典，包含每年的航天器数量
                a = {
                    "1970 年": 1,
                    "1971 年": 1,
                    "1975 年": 1,
                    "1981 年": 3,
                    "1984 年": 1,
                    "1986 年": 1,
                    "1988 年": 1,
                    "1990 年": 2,
                    "2003 年": 2,
                    "2020 年": 89,
                    "2023 年": 221,
                    "2024 年": 257
                }
                # 将字典转换为DataFrame
                df = pd.DataFrame.from_dict(a, orient='index')
                # 绘制折线图，设置颜色、标记、标记大小和标签
                plt.plot(df, color='chocolate', marker='o', markersize=10, label='航天器数量')
                # 旋转x轴刻度标签
                plt.xticks(rotation=90)
                # 添加标题和坐标轴标签
                plt.title('中国每年发射航天器数量', fontdict={'fontweight': 500, 'size': 20})
                plt.xlabel('年份', fontdict={'fontweight': 500, 'size': 20})
                plt.ylabel('数量', fontdict={'fontweight': 500, 'size': 20})
                # 设置y轴范围
                plt.ylim([-50, 350])
                # 在每个折线点上标注具体数值
                for x, y in zip(df.index, df[0]):
                    plt.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 10), ha='center', size=16)
                # 放大x轴刻度字体
                plt.tick_params(axis='x', labelsize=16)
                # 放大y轴刻度字体
                plt.tick_params(axis='y', labelsize=16)
                # 添加图例
                plt.legend()
                # 显示图形
                plt.show()

            elif n == "3":
                # 读取csv文件，编码格式为gbk
                df = pd.read_csv(fileName, encoding='gbk')
                # 将完成年度和启动年度转换为数值型，如果有错误则忽略
                df['持续时间'] = pd.to_numeric(df['完成年度'], errors='coerce') - pd.to_numeric(df['启动年度'], errors='coerce')
                # 删除持续时间小于等于0的行
                valid_df = df.dropna().query('持续时间 > 0')
                # 绘制散点图，x轴为启动年度，y轴为持续时间
                plt.scatter(valid_df['启动年度'], valid_df['持续时间'])
                # 设置图表标题
                plt.title("项目持续时间分布")
                # 设置x轴标签
                plt.xlabel("启动年度")
                # 设置y轴标签
                plt.ylabel("年")
                # 显示图表
                plt.show()
            elif n == "4":
                # 生成词云
                GenerateWordcloud()
            elif n == "5":
                # 生成地理图表
                GenerateGeoChart()
            elif n == "6":
                # 创建一个14x14大小的图形
                # 创建一个14x14大小的图形窗口
                fig = plt.figure(figsize=(14, 14))
                # 定义一个包含图片路径和图片名称的列表
                images = [
                    ('picture/空间站.png', "中国空间站"),
                    ('picture/神州十九号航天员.png', "神州十九号航天员"),
                    ('picture/火箭.png', "中国火箭发射"),
                    ('picture/航天梦.png', "航天梦"),
                    ('picture/长征二号F“T1”.jpg', "长征二号F“T1”"),
                    ('picture/嫦娥三号.jpg', "嫦娥三号"),
                    ('picture/问天实验舱.jpg', "问天实验舱"),
                    ('picture/嫦娥二号.webp', "嫦娥二号"),
                    ('picture/羲和号效果图.jpg',"羲和号效果图"),
                    ('picture/神舟五号.jpg', "神舟五号"),
                    ('picture/神舟七号.jpg', "神舟七号"),
                    ('picture/天舟一号.jpg', "天舟一号"),
                    ('picture/风云四号A星.jpg', "风云四号A星"),
                    ('picture/风云三号.jpg', "风云三号"),
                    ('picture/实践十号.jpg', "实践十号"),
                    ('picture/实践二十号.jpg', "实践二十号"),
                    ('picture/快舟一号甲.jpg', "快舟一号甲"),
                    ('picture/快舟十一号.jpg', "快舟十一号"),
                    ('picture/墨子号.jpg', "墨子号"),
                    ('picture/梦天实验舱.jpg', "梦天实验舱"),
                    ('picture/捷龙三号.jpg', "捷龙三号"),
                    ('picture/鸿雁星座.jpg', "鸿雁星座")
                ]

                # 定义一个更新函数，用于更新图形窗口中的图片
                def update(frame):
                    # 清空图形窗口
                    fig.clf()
                    try:
                        # 读取图片
                        img = mpimg.imread(images[frame][0])
                        # 显示图片
                        plt.imshow(img)
                        # 设置标题
                        plt.title(images[frame][1], fontsize=20)
                        # 关闭坐标轴
                        plt.axis('off')
                    except Exception as e:
                        # 打印错误信息
                        print(Fore.RED + f"加载图片失败: {str(e)}")

                # 创建一个动画，每隔2秒更新一次图片
                ani = FuncAnimation(fig, update, frames=len(images), interval=2000)
                # 显示图形窗口
                plt.show()

            elif n == "7":  # 新增柱状图
                # 使用ggplot样式
                plt.style.use('ggplot')
                df = pd.read_csv(fileName, encoding='gbk')  # 读取csv文件，编码格式为gbk
                counts = df["所属机构"].value_counts()  # 统计所属机构的数量
                plt.figure(figsize=(12,6))  # 设置图形大小
                counts.plot(kind='bar', color='steelblue',label="数量")  # 绘制柱状图，颜色为steelblue

                plt.title("机构项目数量分布")  # 设置图形标题
                plt.xticks(rotation=45)  # 设置x轴标签旋转角度
                plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
                plt.legend()
                plt.show()  # 显示图形

            elif n == "8":  # 新增雷达图
                df = pd.read_csv(fileName, encoding='gbk')  # 读取csv文件
                types_count = df["项目类型"].value_counts()  # 统计项目类型数量
                
                categories = list(types_count.index)  # 获取项目类型列表
                values = types_count.values.tolist()  # 获取项目类型数量列表
                N = len(categories)  # 获取项目类型数量
                
                angles = [n / float(N) * 2 * pi for n in range(N)]  # 计算角度
                angles += angles[:1]  # 添加第一个角度
                
                plt.figure(figsize=(8,8))  # 设置图形大小
                ax = plt.subplot(111, polar=True)  # 创建极坐标图
                ax.set_theta_offset(pi/2)  # 设置角度偏移
                ax.set_theta_direction(-1)  # 设置角度方向
                
                plt.xticks(angles[:-1], categories, color='grey', size=10)  # 设置刻度标签
                ax.set_rlabel_position(0)  # 设置刻度标签位置
                
                values += values[:1]  # 添加第一个值
                ax.plot(angles, values, linewidth=1, linestyle='solid')  # 绘制雷达图
                ax.fill(angles, values, 'b', alpha=0.1)  # 填充雷达图
                plt.title("项目类型雷达图", y=1.1)  # 设置标题
                plt.show()  # 显示图形

            # 如果n等于9，则返回
            elif n == "9":
                return

        except Exception as e:
            # 打印红色字体，输出可视化失败的信息
            print(Fore.RED + f"可视化失败：{str(e)}")
            # 等待用户输入
            input()

# 词云
def GenerateWordcloud():

    # 打开文件并读取内容
    try:
        with open("汇总内容.txt", "r", encoding="utf-8") as f:
            t = f.read()
        print("文本读取成功")
    except FileNotFoundError:
        print("文件未找到，请检查文件名和路径是否正确")
        exit()

    # 分词处理
    ls = jieba.lcut(t)
    # 定义停用词列表
    stopwords = ["有限公司", "和", "号"]
    # 过滤掉停用词
    filtered_ls = [word for word in ls if word not in stopwords]  # 添加这行过滤代码
    # 将过滤后的词用空格连接起来
    txt = " ".join(filtered_ls)
    # 读取中国形状蒙版图片
    mask = np.array(Image.open("中国2.png"))
    # 配置词云参数
    w = wordcloud.WordCloud(
        width=1000,
        height=700,
        background_color="white",
        font_path="C:/Windows/Fonts/SimHei.ttf",  # 确保字体路径正确
        mask=mask  # 添加蒙版参数
    )
    # 生成词云
    try:
        w.generate(txt)
        # 显示词云
        plt.imshow(w)
        plt.axis("off")
        plt.show()
        # 保存词云图片
        w.to_file("词云.png")
        print("词云生成并保存成功")
    except Exception as e:
        print(f"生成词云失败，错误原因: {e}")

# 地理图表
def GenerateGeoChart():
    try:
        a = []
        count = {}
        try:
            file = open("城市信息表.csv", "r", encoding="gbk")
        except FileNotFoundError:
            print(Fore.RED + "错误：城市信息表.csv 文件未找到")
            return
        except Exception as e:
            print(Fore.RED + f"打开文件失败：{str(e)}")
            return

        for line in file:
            i = line.split(",")
            if len(i) < 4:  # 防止数据格式错误
                continue
            city = i[1].strip()
            try:
                lon = float(i[3].strip())
                lat = float(i[2].strip())
            except ValueError:
                continue
            a.append((city, lon, lat))
            count[city] = count.get(city, 0) + 1
        file.close()

        geo = (
            Geo(init_opts=opts.InitOpts(width="1000px", height="800px"))
            .add_schema(maptype="china")
        )

        # 添加城市坐标
        for city, lon, lat in a:
            geo.add_coordinate(city, lon, lat)

        # 添加数据系列
        geo.add(
            series_name="发射基地",
            data_pair=[(city, count[city]) for city, _, _ in a],
            type_="effectScatter",
            symbol_size=10,
            effect_opts=opts.EffectOpts(scale=3, period=4, color="#FF0000"),
            label_opts=opts.LabelOpts(
                is_show=True,
                position="right",
                formatter="{b}：{@[2]}次"
            )
        )
        # 设置全局选项
        geo.set_global_opts(
            title_opts=opts.TitleOpts(title="中国火箭发射基地分布"),
            visualmap_opts=opts.VisualMapOpts(is_show=False)
        )
        # 渲染并自动打开
        output_file = "发射基地分布图.html"
        geo.render(output_file)
        print(Fore.GREEN + f"地理图表已生成，保存为 {output_file}")
        import webbrowser
        webbrowser.open(output_file)

    except Exception as e:
        print(Fore.RED + f"生成地理图表时出错：{str(e)}")
def run_game():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('菲菲')  # 将游戏的左上角改为菲菲
    FPS = 60
    # 调整窗口大小为 1000x1200
    screen = pygame.display.set_mode((1000, 1200))
    clock = pygame.time.Clock()  # 引入pygame模块的时间库
    running = True

    # 得分初始化
    score = 0
    # 创建字体对象，36 是字体大小
    font = pygame.font.Font(None, 36)
    # 载入图片要先做初始化
    background_img = pygame.image.load(os.path.join('img', 'background.png')).convert()
    # 调整背景图片大小以适应新窗口
    background_img = pygame.transform.scale(background_img, (1000, 1200))
    player_img = pygame.image.load(os.path.join('img', 'player.png')).convert()
    rock0_img = pygame.image.load(os.path.join('img', 'rock.png')).convert()
    bullet_img = pygame.image.load(os.path.join('img', 'bullet.png')).convert()
    enemy_img = pygame.image.load(os.path.join('img', 'enemy.png')).convert()
    rock1_img = pygame.image.load(os.path.join('img', 'rock1.png')).convert()
    rock5_img = pygame.image.load(os.path.join('img', 'rock5.png')).convert()
    # 创建一个列表 爆炸动画实际是一张张图片的播放
    expl_anim = {}
    expl_anim['lg'] = []
    expl_anim['sm'] = []
    # 循环载入9张爆炸图片
    for i in range(9):
        # 载入图片
        expl_img = pygame.image.load(os.path.join('img', f'expl{i}.png')).convert()
        # 设置透明度为黑色
        expl_img.set_colorkey((0, 0, 0))
        # 将图片放大到50*50
        expl_anim['lg'].append(pygame.transform.scale(expl_img, (50, 50)))
        # 将图片放大到30*30
        expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    # 载入音乐
    shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))
    expl0_sound = pygame.mixer.Sound(os.path.join('sound', 'expl0.wav'))
    expl1_sound = pygame.mixer.Sound(os.path.join('sound', 'expl1.wav'))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img, (50, 35))
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            # 调整玩家初始位置
            self.rect.centerx = 500
            self.rect.bottom = 950 - 10

        def update(self):
            key_pressed = pygame.key.get_pressed()  # 是否有按键，如有则返回对应的值
            if key_pressed[pygame.K_RIGHT]:  # 按右键 往右运动
                self.rect.x += 8
            if key_pressed[pygame.K_LEFT]:  # 按左键 往左运动
                self.rect.x -= 8
            # 调整边界判断
            if self.rect.right > 1000:
                self.rect.right = 1000
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.left > 1000:
                self.rect.right = 0

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
    class Rock(pygame.sprite.Sprite):  # 创建一个石头类别
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            rock = [rock0_img, rock1_img, rock5_img]
            self.image = random.choice(rock)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            # 调整石头初始位置随机范围
            self.rect.x = random.randrange(0, 1000 - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            # 调整边界判断
            if self.rect.top > 1200 or self.rect.left > 1000 or self.rect.right < 0:
                self.rect.x = random.randrange(0, 1000 - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(2, 10)
                self.speedx = random.randrange(-3, 3)

    class Enemy(pygame.sprite.Sprite):  # 创建一个飞机类别
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(enemy_img, (50, 35))
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect()
            # 调整敌人初始位置随机范围
            self.rect.x = random.randrange(0, 1000 - self.rect.width)
            self.rect.y = random.randrange(-100, 100)  # 调整初始位置范围，确保飞机能更快进入可视区域
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-1, 1)

        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            # 调整边界判断
            if self.rect.top > 1200 or self.rect.left > 1000 or self.rect.right < 0:
                self.rect.x = random.randrange(0, 1000 - self.rect.width)
                self.rect.y = random.randrange(-100, 100)  # 调整初始位置范围，确保飞机能更快进入可视区域
                self.speedy = random.randrange(2, 10)
                self.speedx = random.randrange(-1, 1)

    class Bullet(pygame.sprite.Sprite):  # 创建一个子弹类别
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = bullet_img
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()
    # 定义爆炸动画
    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, size):
            pygame.sprite.Sprite.__init__(self)
            self.size = size
            self.image = expl_anim[self.size][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(expl_anim[self.size]):
                    self.kill()
                else:
                    self.image = expl_anim[self.size][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center

    all_sprites = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemys = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(3):
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    for j in range(5):
        e = Enemy()
        all_sprites.add(e)
        enemys.add(e)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        # 更新游戏
        all_sprites.update()
        hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
        hits1 = pygame.sprite.groupcollide(enemys, bullets, True, True)
        for hit in hits:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            expl0_sound.play()
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)
            score += 10
        for hit in hits1:
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            expl1_sound.play()
            e = Enemy()
            all_sprites.add(e)
            enemys.add(e)
            score += 20
        hits = pygame.sprite.spritecollide(player, rocks, False)
        if hits:
            running = False
        hits1 = pygame.sprite.spritecollide(player, enemys, False)
        if hits1:
            running = False
        # 画面显示
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 0, 0))
        screen.blit(score_text, (80, 80))
        all_sprites.draw(screen)
        pygame.display.update()

    pygame.quit()

# 主程序
def CleanInput(prompt):
    """统一处理输入并清空缓冲区"""
    try:
        # 清空输入缓冲区
        while True:
            res = input(prompt)
            res = res.strip()
            if res:  # 只要输入不为空就返回
                return res
    except KeyboardInterrupt:
        exit(0)

def main():
    # 读取项目信息
    ReadProjectInfo(fileName)
    while True:
        # 显示用户界面
        ShowUI()
        try:
            # 获取用户输入
            choice = CleanInput(Fore.YELLOW + "请选择操作(数字1~10,按Enter返回):")
            if choice == "1":
                # 显示所有项目
                ShowAllProjects()
            elif choice == "2":
                # 添加项目
                AddProject()
            elif choice == "3":
                # 删除项目
                DeleteProject()
            elif choice == "4":
                # 修改项目
                ModifyProject()
            elif choice == "5":
                # 写入项目信息
                WriteProjectInfo(fileName)
                input("\n保存成功，按Enter返回...")
            elif choice == "6":
                # 查询菜单
                QueryMenu()
            elif choice == "7":
                # 静态
                Static()
            elif choice == "8":
                # 图片
                Picture()
            elif choice == "9":
                # 运行游戏
                run_game()
            elif choice == "10":
                # 打印感谢信息并退出循环
                print(Fore.CYAN + "感谢使用！")
                break
            else:
                # 无效输入
                print(Fore.RED + "无效输入！请选择1-10")
                input("按Enter继续...")
        except Exception as e:
            # 打印异常信息
            print(Fore.RED + f"操作异常: {str(e)}")
            input("按Enter继续...")

# 如果当前模块是主模块，则执行main()函数
if __name__ == "__main__":
    main()