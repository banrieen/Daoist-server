@echo off
:: Stop app, and delete shortcut
:: Replase update file, and restart app
:: 版本：v0.1.0
:: 在win7/11等系统 CMD 下可以用 WMIC 远程执行脚本,示例命令如下：
:: wmic /failfast:on /node:192.168.121.155 /user:OPUS3 /password:semics process call create "cmd.exe /c  D:\proberfiles\PMI_Image\rpaAgent\update-agent-XP.bat v1.1.0"
:: 查看远程系统的基本信息，示例：
:: wmic /node:192.168.121.170 /user:OPUS3 /password:semics process call create "cmd /c ipconfig /all >> D:\proberfiles\PMI_Image\debug.log"
:: 查看运行中的程序进程
:: wmic /failfast:on  /node:193.180.21.232 /user:OPUS3 /password:semics process where "name='rpaAgent.exe'" get ProcessId
:: 停止客户端
:: wmic /node:192.168.121.155 /user:OPUS3 /password:semics process call create "cmd /c D:\proberfiles\PMI_Image\rpaAgent\rpaAgent.exe stop"

SET APP=rpaAgent.exe
::SET VERSION=%1
SET APPLINK=shortcut-to-rpaAgent.exe.lnk
SET BOOTDIR="C:\Documents and Settings\OPUS3\Start Menu\Programs\Startup\"
SET APPLOCATION=D:\proberfiles\PMI_Image\rpaAgent\
SET LOCKFILE="C:\Documents and Settings\OPUS3\IKAS-Rpa-Agent.lock"

:: Create shortcut for APP
SETLOCAL ENABLEDELAYEDEXPANSION
SET LinkName=shortcut-to-rpaAgent.exe
SET Esc_LinkDest=%%APPLOCATION%%!LinkName!.lnk
SET Esc_LinkTarget=%%APPLOCATION%%%%APP%%
SET Esc_LinkDirectory=%%APPLOCATION%%
SET cSctVBS=CreateShortcut.vbs
SET LOG=".\%~N0_runtime.log"
((
  echo Set oWS = WScript.CreateObject^("WScript.Shell"^) 
  echo sLinkFile = oWS.ExpandEnvironmentStrings^("!Esc_LinkDest!"^)
  echo Set oLink = oWS.CreateShortcut^(sLinkFile^) 
  echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("!Esc_LinkTarget!"^)
  echo oLink.WorkingDirectory = oWS.ExpandEnvironmentStrings^("!Esc_LinkDirectory!"^)

  echo oLink.Save
)1>!cSctVBS!
cscript //nologo .\!cSctVBS!
DEL !cSctVBS! /f /q
)1>>!LOG! 2>>&1

:: Update shortcut to start folder
:: TASKKILL /f /t /im %APP%  
IF exist %BOOTDIR%%APPLINK% (
  DEL   /q %BOOTDIR%%APPLINK%
)
MOVE  %APPLOCATION%%APPLINK% %BOOTDIR%
D:
CD    %APPLOCATION%

echo Update Step: %2 >> update.log

:: Sleep 2 s
:: ping -n 2 127.0.0.1>nul
start /B %APP% stop
:: Sleep 2 s
ping -n 2 127.0.0.1>nul
start /B %APP% 
:: Update log
echo Update Datetime: %date% %time% >> update.log
echo Update Location: %cd%  >> update.log
echo Update Version:  %1 >> update.log
echo Update Error:  %ERRORLEVEL% >> update.log

EXIT