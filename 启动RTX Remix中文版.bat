@echo off
title RTX Remix 中文启动器
rem ============================================
rem  RTX Remix Toolkit 中文版启动器
rem  中文翻译扩展：D:\deepseek\new caozuo\rtx.remix.zh
rem ============================================
set "KIT=C:\Program Files\NVIDIA Corporation\RTX Remix\kit\kit.exe"
set "EXT=D:\deepseek\new caozuo\rtx.remix.zh"
if not exist "%KIT%" (
    echo [错误] 找不到 kit.exe
    pause
    exit /b 1
)
if not exist "%EXT%\config\extension.toml" (
    echo [错误] 找不到中文扩展
    pause
    exit /b 1
)
echo 正在启动 RTX Remix Toolkit（中文版）...
cd /d "C:\Program Files\NVIDIA Corporation\RTX Remix"
"%KIT%" apps/lightspeed.app.trex.kit --ext-path "%EXT%" --enable rtx.remix.zh
