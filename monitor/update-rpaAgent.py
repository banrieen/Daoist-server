#!/usr/bin/env python3
"""远程更新
# 用途：更新机台自动化任务
1. 读取设备列表，获取机台编号
2. 读取机台日志解析 lotID
3. 通过 lotID 获取产品名称
4. 结合产品编号，机台编号更新自动化任务
# 版本： 0.1
# 维护者： haiyuan
# 更新时间：2024/06/24
# 执行环境: python 3.11以上
## 依赖本地环境
### 通过机台编号，所在厂区获取机台IP： http://192.168.115.172:8000/api/equipment/common/JSW1/POS-137
### 本地客户端通信：

"""

from smb.SMBConnection import SMBConnection
from smb.base import ConnectionError, NotReadyError, ProtocolErrorimport polars as pl
import ray
import subprocess
import requests as rq
import logging
import datetime
import os
import mariadb
import pdb

# ray.init()
logger = logging.getLogger(__name__)
logging.basicConfig(filename='autolog.log', level=logging.INFO)

def execute_wmic(commands:str)->bool:
    # 在 windows 系统使用 WMIC 远程执行命令
    # windows XP SP1/3 需要启动 WMIC 服务
    try:
        if not commands:
            return False
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, shell=True)
            if result.returncode == 0:
                continue
            else:
                return False
    except Exception as e:
        return False
    return result.stdout
    
def init_smb_conn(host:str,username:str,password:str,remote_name:str,domain:str="",client_name:str="AutoLocation"):
    # 尝试连接远端 samba v1.x 共享服务
    try:
        # 新建 SMBConnection 对象, 默认走 445 端口
        conn = SMBConnection(username=username,
                            password=password,
                            my_name=client_name,
                            remote_name=remote_name,
                            domain=domain,
                            use_ntlm_v2=False,
                            is_direct_tcp=True
                            )
        conn.connect(host, port=445, sock_family=None, timeout=5)
        return conn
    except ConnectionError:
        # logger.info(e)
        # 切换为 139端口，is_direct_tcp=False
        conn = SMBConnection(username=username,
                            password=password,
                            my_name=client_name,
                            remote_name=remote_name,
                            domain=domain,
                            use_ntlm_v2=False,
                            is_direct_tcp=False
                            )
        conn.connect(host, port=139, sock_family=None, timeout=5)
        return conn
    finally:
        pass
    
def send_update_content(conn, update_client)->bool:
    # 更新文件
    ## 尝试删除不需要的文件
    ## 推送更新的文件到远端,如果是文件夹内有多个,就遍历发送
    ## 远程更新目录是固定的，不适合自动适配
    ## 发送更新版本说明
    update_path = update_client["update_path"]
    station_ip = update_client["StationIP"]
    share_path = update_client["share_path"]
    username = update_client["username"]
    password = update_client["password"]
    version = update_client["AgentVersion"]
    sharePath, child = os.path.split(share_path)
    try:
        for filename in os.listdir(update_path):
            basename, extension = os.path.splitext(filename)
            file_type = "rb" if "exe" in extension else "r"
            updates = os.path.join(update_path, filename)
            shareFile = os.path.join(child, filename)
            try:
                conn.deleteFiles(sharePath, shareFile, delete_matching_folders=False, timeout=30)
            except:
                pass
            
            with open(updates, file_type) as f:
                # pdb.set_trace()
                conn.storeFile(sharePath, shareFile, f, timeout = 120,)
        versionFile = f"__VERSION__{version}.txt"
        with open(versionFile, "wt+") as u:
            u.write(version)
        shareFile = os.path.join(child, versionFile)
        conn.storeFile(sharePath, shareFile, u, timeout = 60,)
        return True
    except:
        logger.info(f"{sharePath}, {child}")
        pass
    conn.close()
    return False

def insert_record(row, update_client, db_table="flow_update_record",user="thomas",password="thomas",host="192.168.56.113",port=3306,database="rpa_vt"):
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
    # Get Cursor
    cursor = conn.cursor()
    df = {
            "fab" : "",
            "StationID" : "",
            "AgentVersion" : "",
            "AgentName" : "",
            "StationIP" : "",
            "FlowName" : "",
            "FlowVersion" : "",
            "OtherStationID" : "",
            "OtherStationIP" : "",
            "UpdateTime" : "",
            "UpdateStatus" : "",
            "Info" : "",
            "account" : "",
                }
    
    columns =  tuple(df.keys())
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (db_table, ",".join(columns), ', '.join(['%s'] * len(columns)))
    df["UpdateTime"]  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["StationID"] =  row[1]
    df["fab"] =  str(row[0])
    df["AgentName"] =  update_client["AgentName"]
    df["StationIP"] = update_client["StationIP"]
    df["AgentVersion"] = update_client["AgentVersion"]
    cursor.execute(insert_sql, tuple(df.values()))
    conn.commit() 
    conn.close()

# @ray.remote
def deploy_clent(station, update_client, start_agent=False):
    ## 获取机台的IP,账号，密码
    ## 停止客户端，停止文件占用
    ## 更新版本说明
    ## 推送内容
    ## 启动客户端
    ## 验证客户端，检查最新的日志
    ## 记录更新

    fabID = "JSW1" if 1.0 == station[0] else "JSW5"
    stationInfo = rq.get(f"http://192.168.115.172:8000/api/equipment/common/{fabID}/{station[1]}")
    stationInfo = stationInfo.json()
    if stationInfo["data"]:
        update_client["StationIP"] = stationInfo["data"]["ip"]
        stationTpye = stationInfo["data"]["eqp_type_name"]
        stationKvmIP = stationInfo["data"]["kvm_ip"]
    else:
        pass 
    # update_client
    host = update_client["StationIP"]
    username = update_client["username"]
    password = update_client["password"]
    version = update_client["AgentVersion"]
    ## 停止客户端
    stop_agent = f'wmic /node:{host} /user:{username} /password:{password} process call create "cmd /c D:\\proberfiles\\PMI_Image\\rpaAgent\\rpaAgent.exe stop"'
    execute_wmic(stop_agent)
    conn = init_smb_conn(host,username,password,remote_name=host,domain="",client_name="AutoLocation")
    ## 推送更新文件 
    rst = send_update_content(conn,update_client)  
    if rst:
        ## 启动客户端
        start_agent =f'wmic /node:{host} /user:{username} /password:{password} process call create "D:\\proberfiles\\PMI_Image\\rpaAgent\\update-agent-XP.bat {version} start"' 
        execute_wmic(start_agent)
        ## 获取状态
        get_status = f'wmic /failfast:on  /node:{host} /user:{username} /password:{password} process where name=rpaAgent.exe get ProcessId '
        _ = execute_wmic(get_status)
        ## 插入数据库记录
        update_client["UpdateStatus"] = "1"
        insert_record(station, update_client, db_table="flow_update_record",user="thomas",password="thomas",host="192.168.56.113",port=3306,database="rpa_vt")
    else:
        update_client["UpdateStatus"] = "0"
        insert_record(station, update_client, db_table="flow_update_record",user="thomas",password="thomas",host="192.168.56.113",port=3306,database="rpa_vt")

def auto_deploy(remote_station:dict,update_client:dict):
    # 获取更新列表
    ## 并发执行
    ## 获取执行结果
    ## 更新excel
    df = pl.read_excel(
    source = remote_station["station_file"],
    sheet_name = remote_station["sheet_name"],
    engine_options = {"skip_empty_lines": True},
    read_options={"has_header": True,"skip_rows":6}
    )
    stationList =  df.select(remote_station["selector_col"])
    
    # 远程执行, 初始化集群 ray start --head --num-cpus=4 --dashboard-host=0.0.0.0
    # for row in stationList.rows():
    row = (1.0, 'POS-166', '1.1.0')
    print(f'==============>{row}')
    deploy_clent(row,update_client,start_agent=update_client["start_agent"])

    # jobs = [deploy_clent.remote(row,update_client,start_agent=remote_station["start_agent"]) for row in stationList.rows()]
    # # pdb.set_trace()
    # print(ray.get(jobs)) # [0, 1, 4, 9]


if __name__ == "__main__":
    remote_station = {
    "station_file" : r"C:\workspace\ProductSpace\08-伟测-RPA\RCC-RPA整体状态汇总.xlsx",
    "sheet_name" : "代操上线情况",
    "selector_col" : ("厂区","机台号","客户端版本号") ,
    }
    update_client = {
            "fab":"1.0",
            "StationID" :"01",
            "AgentVersion" :"v1.1.3",
            "AgentName" : "rpaAgent.exe",
            "StationIP" : "192.168.121.62" , 
            "host_type" : "OPUS3" ,                ## \\192.168.56.110\develop
            "username" : "OPUS3",                  ## "thomas"
            "password" : "semics",                 ## "thomas"
            "start_agent":False  ,                        ## 默认不启用客户端
            "share_path" : r"PMI_Image\rpaAgent" , ## "develop"
            "FlowName" :"",
            "FlowVersion" :"",
            "OtherStationID" :"",
            "OtherStationIP" :"",
            "UpdateTime" :"",
            "UpdateStatus" :"",
            "Info" :"",
            "account":"tom",
            "domain" : "",
            "client_name" : "AutoLocation",
            "update_path" : r"C:\workspace\ProductSpace\08-伟测-RPA\3.开发实施\updateFiles",
            "update_version" : "v1.1.1",
            "shareFile" : "update-agent-XP.bat",
            "dropFile" : ""
        }

    # execute_wmic(host,username,password,versionTag="")
    auto_deploy(remote_station,update_client)