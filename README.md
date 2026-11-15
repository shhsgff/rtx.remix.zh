# RTX Remix 中文翻译扩展 (rtx.remix.zh)

为 **NVIDIA RTX Remix Toolkit 1.6** 提供运行时中文（zh-CN）界面翻译。
不改动任何官方文件：扩展启动后周期性地遍历 omni.ui 控件树，把匹配词典的英文文本就地替换为中文。

> 原理：Omniverse Kit 扩展 + JSON 词典 + 控件树遍历。安全、可随时卸载。

## 安装（三选一）

### 方式一：克隆 + 启动器（推荐）

1. 克隆仓库（文件夹名必须与扩展 id 一致）：
   ```bat
   git clone https://github.com/shhsgff/rtx.remix.zh.git D:\AI绘画\rtx.remix.zh
   ```
2. 用启动器启动 Toolkit（把扩展路径和启用参数带进去）：
   ```bat
   cd /d "C:\Program Files\NVIDIA Corporation\RTX Remix\kit"
   kit.exe apps/lightspeed.app.trex.kit --ext-path "D:\AI绘画\rtx.remix.zh" --enable rtx.remix.zh
   ```
   或下载仓库里的 `启动RTX Remix中文版.bat` 改路径后使用。

### 方式二：复制到扩展搜索目录

把本仓库整个文件夹复制到 Toolkit 的扩展目录（如 `C:\Program Files\NVIDIA Corporation\RTX Remix\kit\exts\rtx.remix.zh`），然后在启动参数加 `--enable rtx.remix.zh`。

### 方式三：--enable 命令行（临时试用）

```bat
kit.exe apps/lightspeed.app.trex.kit --ext-path "<本仓库路径>" --enable rtx.remix.zh
```

## 覆盖范围

- Home 页（项目列表、按钮、快速入门）
- 主菜单（File / Edit / Create / Window / Help 等）
- AI Tools（ComfyUI 连接）面板
- 渲染设置面板（DLSS 3D-Guided Neural Rendering、高光恢复等）
- Stage Manager / Property 面板等常用界面

词典文件：`data/zh-CN.json`，按 `"英文原文": "中文翻译"` 格式。可直接编辑添加词条。

## 限制

- 只翻译 **静态文本控件（Label）**；图标、图片、动态拼接文本（如 `Host Memory: 14.1 GiB`）需要额外词条或前缀匹配。
- 未收录的英文文本会输出到 `%LOCALAPPDATA%\rtx-remix-zh.log`，可据此继续补充词典。
- 部分深度嵌套面板可能扫描不到；发现漏翻请提 issue 并附截图。

## 卸载

删除本文件夹、去掉启动参数即可，不影响官方文件。

## 目录结构

```
rtx.remix.zh/
├── config/
│   └── extension.toml        # 扩展清单
├── data/
│   └── zh-CN.json            # 翻译词典
├── docs/
│   ├── CHANGELOG.md
│   └── README.md             # 扩展窗口内文档
└── rtx/remix/zh/
    ├── __init__.py           # 扩展入口
    └── translator.py         # 控件树遍历翻译引擎
```

## License

MIT
