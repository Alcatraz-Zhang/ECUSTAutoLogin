# 校园网自动重连脚本

## 项目描述

这个Python脚本旨在自动检测华理校园网连接状态，并在断开时自动重新登录。

## 功能特点

- 自动检测网络连接状态
- 在网络断开时自动重新登录
- 支持自定义登录URL、用户名和密码
- 可配置的重试次数和间隔时间
- 支持选择不同的网络速度选项（25M或其他）
- 使用无头浏览器模式，减少资源占用
- 提供时间戳日志输出

## 安装要求

1. Python 3.8+
2. Firefox 浏览器
3. geckodriver（Firefox WebDriver）

## 安装步骤

1. 克隆或下载此项目到本地。

2. 安装所需的Python包：
   ```
   pip install -r requirements.txt
   ```

3. 下载适合您系统的 [geckodriver](https://github.com/mozilla/geckodriver/releases)，并将其放置在系统PATH中或指定路径下。

## 配置

编辑 `config.json` 文件，填入您的个人信息和首选项：

```json
{
    "username": "你的账号",
    "password": "你的密码",
    "login_url": "http://login.ecust.edu.cn",
    "geckodriver_path": "path\\to\\geckodriver.exe",
    "max_retry": -10,
    "retry_time": 60,
    "speed": "25M"
}
```

- `username`: 您的校园网账号
- `password`: 您的校园网密码
- `login_url`: 校园网登录页面的URL
- `geckodriver_path`: geckodriver可执行文件的路径
- `max_retry`: 最大重试次数（设置为负数或0表示无限重试）
- `retry_time`: 每次检查网络状态的间隔时间（秒）
- `speed`: 选择的网络速度（"25M"或其他）

## 使用方法

运行脚本：

```
python login.py
```

脚本将开始监控网络状态，并在需要时自动重新连接。

## 注意事项

- 请确保您的账号信息安全，不要将包含密码的配置文件分享给他人。
- 这个脚本使用无头浏览器模式，运行时不会显示浏览器窗口。
- 如果遇到问题，请检查geckodriver的版本是否与您的Firefox浏览器版本兼容。

## 贡献

欢迎提交问题报告和改进建议。如果您想贡献代码，请先开issue讨论您想要改变的内容。