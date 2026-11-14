@echo off
chcp 65001 >nul
rem ============================================
rem  RTX Remix Toolkit 中文启动器 (rtx.remix.zh)
rem  用法：把下面 EXT 改成本仓库实际路径后双击运行
rem ============================================
set "KIT=C:\Program Files\NVIDIA Corporation\RTX Remix\kit\kit.exe"
set "EXT=%~dp0"
if not exist "%KIT%" (
    echo [错误] 找不到 kit.exe：%KIT%
    pause
    exit /b 1
)
if not exist "%EXT%config\extension.toml" (
    echo [错误] 找不到扩展文件：%EXT%config\extension.toml
    pause
    exit /b 1
)
echo 正在启动 RTX Remix Toolkit（中文版）...
"%KIT%" apps/lightspeed.app.trex.kit --ext-path "%EXT%" --enable rtx.remix.zh
