#!/usr/bin/env python3
"""脚本说明
用途：读取和计算指定的csv文件中的2列时间的延时
版本： 0.1
维护者： haiyuan
更新时间：2024/06/17
执行环境: python 3.11以上
执行示例：python daoist\Agent-wxGUI\calculate-time-interval.py --csvFile "C:\workspace\ProductSpace\08-伟测-RPA\3.开发实施\mark_feature\mark_feature_runtime-20240701.csv"
"""
from cmath import e
from datetime import *
import polars as pl
import os
import pdb
import mariadb
# import sys

# Connect to MariaDB Platform
# class storage_data():
#     def __init__(self,user="thomas",password="thomas",host="192.168.56.113",port=3306,database="rpa_vt"):
#         try:
#             conn = mariadb.connect(
#                 user,
#                 password,
#                 host,
#                 port,
#                 database
#             )
#         except mariadb.Error as e:
#             print(f"Error connecting to MariaDB Platform: {e}")
#             sys.exit(1)
#         # Get Cursor
#         self.cur = conn.cursor()

    # def insert

def time_count(endTime="2024-06-15 00:47:48:137412", startTime="2024-06-15 00:47:29:875000"):
    # 计算2个时间的差，单位为秒
    # 如果其中一个值为空，默认设置为 0
    if None!=endTime and None!=startTime:
        startTime = datetime.strptime(startTime,"%Y-%m-%d %H:%M:%S:%f")
        endTime = datetime.strptime(endTime,"%Y-%m-%d %H:%M:%S:%f")
        elapsedTime = endTime - startTime
        return elapsedTime.seconds
    else:
        return 0

def insert_db(df, db_table="flow_target_record",user="thomas",password="thomas",host="192.168.56.113",port=3306,database="rpa_vt"):
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
            )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    # Get Cursor
    cursor = conn.cursor()
    
    # cursor.execute(
    # f"INSERT INTO {db_table} (df.columns) VALUES (?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?,)", 
    # (df.rows()))
    columns = tuple(df.columns)
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (db_table, columns, ', '.join(['%s'] * len(df.columns)))
    # cursor.execute(
    # f"INSERT INTO {db_table} (df.columns) VALUES (?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?,)", 
    # (df.rows()))
    # cursor.executemany(insert_sql, df.rows())
    for row in df.rows():
        pdb.set_trace()
        cursor.execute(insert_sql, tuple(row))
    conn.commit() 
    conn.close()

def update_csv(task, csvFile, output):
    # 读取并计算指定列的时间差，单位：秒，并导出到csv中
    df = pl.read_csv(csvFile)
    # pdb.set_trace()
    # df_real = df.filter((pl.col(endTime) != "") & (pl.col(startTime) != ""))  # 可以过滤掉空行
    for i in task:
        endTime = i["endTime"]
        startTime = i["startTime"]
        resultColAlias = i["resultColAlias"]
        count = [time_count(row[0],row[1]) for row in df.select(pl.col(endTime,startTime)).iter_rows()]
        
        # insert_db(df)
        df = df.with_columns(pl.DataFrame({resultColAlias:count}))
    df.write_csv(output, separator=",")

if __name__ == "__main__":
    # 本地执行
    import argparse
    # import pdb
    ## 支持解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvFile', help='需要处理的 csv 文件')
    parser.add_argument('--output', help='保存结果的 csv 文件')
    parser.add_argument('--task', help='需要计算的列')
    args = parser.parse_args()
    csvFile_default = r"C:\workspace\ProductSpace\08-伟测-RPA\3.开发实施\mark_feature_runtime-20240618.csv"
    task_default = [{"endTime":"start_time","startTime":"mark_align_ok_time","resultColAlias":"H-F"},
            {"endTime":"start_time","startTime":"stop_before_probe_time","resultColAlias":"H-G"},
            {"endTime":"end_time","startTime":"start_time","resultColAlias":"I-H"},
            {"endTime":"wafer_start_time","startTime":"mark_align_ok_time","resultColAlias":"E-F"},]
    csvFile = args.csvFile if args.csvFile  else csvFile_default
    output =  args.output if args.output  else csvFile
    task =  args.task if args.task else task_default
    # 遍历文件目录
    csvDir = r"C:\workspace\ProductSpace\08-伟测-RPA\3.开发实施\mark_feature"
    for csvFile in os.listdir(csvDir):
        csvFile = os.path.join(csvDir, csvFile)
        output = csvFile
        try:
            update_csv(task, csvFile, output)
            print(f"Task Finished, Result saved in {output} !")
        except IOError as e:
            raise IOError(f"Tark ERROR On {csvFile}! ") from e