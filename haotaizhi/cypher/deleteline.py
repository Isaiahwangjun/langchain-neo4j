import csv
import re

import pandas as pd


def delete_null_column(file_path):

    df = pd.read_csv(file_path)

    # 找到需要删除的列
    cols_to_drop = []
    for col in df.columns:
        if df[col].iloc[1:].isna().all():
            cols_to_drop.append(col)

    # 删除这些列
    df.drop(columns=cols_to_drop, inplace=True)

    # 将修改后的 DataFrame 写回到 Excel
    df.to_csv('temp.csv', index=False, encoding='UTF-8-Sig')


def read_csv_column(csv_file, column_name):
    # 打开 CSV 文件
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # 读取指定列的数据
        # column_data = [row[column_name] for row in reader]
        column_data = [
            row[column_name].split('\n')[0]
            if '\n' in row[column_name] else row[column_name] for row in reader
        ]

        return column_data


def read_csv_column_delete_english(csv_file, column_name):
    # 打开 CSV 文件
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # 读取指定列的数据，并删除所有英文字符
        column_data = [
            re.sub(r'[^\u4e00-\u9fff]', '', row[column_name]) for row in reader
        ]
        return column_data


def write_csv_column(csv_file, column_name, column_data):
    # 打开原始 CSV 文件和一个临时文件
    with open(csv_file, 'r', newline='',
              encoding='utf-8') as file, open('temp.csv',
                                              'w',
                                              newline='',
                                              encoding='utf-8') as temp_file:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(temp_file, fieldnames=reader.fieldnames)

        # 写入头部
        writer.writeheader()

        # 将处理后的数据写入临时文件
        for row, data in zip(reader, column_data):
            row[column_name] = data
            writer.writerow(row)

    import os
    os.replace('temp.csv', csv_file)


# 示例用法
csv_file = 'data/Organization.csv'
column_name = 'name'
file_path = r'C:\Users\wang\Downloads\tww_Publication_2024_5_15.csv'
# column_data = read_csv_column_delete_english(csv_file, column_name)
# print(column_data)
# write_csv_column(csv_file, column_name, column_data)
delete_null_column(file_path)
