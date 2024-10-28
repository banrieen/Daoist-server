from smb.SMBConnection import SMBConnection

## 连接，传输不稳定
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
    except  ConnectionError as e:
        logger.info(e)
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
    
def send_update_content(conn, version:str,updateFile:str, dropFile:str, sharePath:str, shareFile:str)->bool:
    # 更新文件
    ## 尝试删除不需要的文件
    ## 推送更新的文件到远端,如果是文件夹内有多个,就遍历发送
    ## 远程更新目录是固定的，不适合自动适配
    ## 发送更新版本说明

    sharePath, child = os.path.split(sharePath)
    if os.path.isdir(updateFile):
        for filename in os.listdir(updateFile):
            basename, extension = os.path.splitext(filename)
            file_type = "rb" if "exe" in extension else "r"
            updates = os.path.join(updateFile, filename)
            shareFile = os.path.join(child, filename)
            try:
                conn.deleteFiles(sharePath, shareFile, delete_matching_folders=False, timeout=30)
                with open(updates, file_type) as f:
                    conn.storeFile(sharePath, shareFile, f, timeout = 60,)
            except:
                pass
    try:
        versionFile = f"__VERSION__{version}.txt"
        with open(versionFile, "wt+") as u:
            u.write(version)
        shareFile = os.path.join(child, versionFile)
        conn.storeFile(sharePath, shareFile, u, timeout = 60,)
    except ConnectionError as e:
        logger.info(e,f"{sharePath}, {child}")
    conn.close()
    return True


## net use 
def send_update_content(update_client:dict)->bool:
    # 更新文件
    ## 尝试删除不需要的文件
    ## 推送更新的文件到远端,如果是文件夹内有多个,就遍历发送
    ## 远程更新目录是固定的，不适合自动适配
    ## 发送更新版本说明
    send_flag = False
    _share_driver = "Z:"
    update_path = update_client["update_file"]
    station_ip = update_client["StationIP"]
    share_path = update_client["share_path"]
    username = update_client["username"]
    password = update_client["password"]
    conn = f"net use {_share_driver} \\{station_ip}\{share_path} /user:{username} {password}"
    commands =  []
    commands.append(conn)
    try:
        if os.path.isdir(update_path):
            for filename in os.listdir(update_path):
                share_file = os.path.join(update_path, filename)
                commands.append(f"copy /Y {share_file} {_share_driver}")
        version = update_client["AgentVersion"]
        version_file = f"__VERSION__{version}.txt"
        share_file = os.path.join(update_path, version_file)
        with open(share_file, "wt+") as u:
            u.write(version)
        commands.append(f"copy /Y {share_file} {_share_driver}")
        ## 关闭共享连接
        commands.append(f"net use Z: /delete" )
        pdb.set_trace()
        _rst = execute_wmic(commands)
        if _rst and "1 个文件" in _rst:
            send_flag = True
    except ConnectionError as e:
        logger.info(e,f"{share_file}")
    return send_flag