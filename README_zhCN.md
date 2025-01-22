# UpFileLive

`UpFileLive` 是一个用于与 [upfile.live](https://upfile.live) 文件分享服务交互的 Python 工具类。它提供了同步和异步方式上传文件并生成分享链接和下载链接的功能。

## 安装

使用 pip 安装:

```bash
pip install UpFileLive
```

### 依赖库
- [playwright](https://playwright.dev/python/), loguru
- Python 版本 >= 3.7

通过以下命令安装依赖库：
```bash
pip install playwright loguru
python -m playwright install
```

## 使用方法

### 初始化类
```python
from UpFileLive import UpFileLive

# 初始化 UpFileLive 对象
file_uploader = UpFileLive("/path/to/your/file")
```

### 同步上传文件
```python
# 上传文件并获取分享链接
file_uploader.sync_upfile()
print(f"分享链接: {file_uploader.get_share_link()}")
```

### 异步上传文件
```python
import asyncio

async def async_upload():
    await file_uploader.async_upfile()
    print(f"分享链接: {file_uploader.get_share_link()}")

asyncio.run(async_upload())
```

### 同步获取下载链接
```python
# 获取下载链接(如果已经运行过 upfile 函数，则无需设置此选项)
# file_uploader.share_link = "<your_share_link>"
file_uploader.sync_download()
print(f"下载链接: {file_uploader.get_download_link()}")
```

### 异步获取下载链接
```python
async def async_download():
    # file_uploader.share_link = "<your_share_link>"
    await file_uploader.async_download()
    print(f"下载链接: {file_uploader.get_download_link()}")

asyncio.run(async_download())
```

### 一键上传并获取下载链接
#### 同步方式
```python
file_uploader.sync_upfile_download()
print(f"分享链接: {file_uploader.get_share_link()}")
print(f"下载链接: {file_uploader.get_download_link()}")
```

#### 异步方式
```python
async def async_upload_download():
    await file_uploader.async_upfile_download()
    print(f"分享链接: {file_uploader.get_share_link()}")
    print(f"下载链接: {file_uploader.get_download_link()}")

asyncio.run(async_upload_download())
```

## 许可协议
本项目采用 [MIT 许可协议](LICENSE)。

