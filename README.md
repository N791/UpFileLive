# UpFileLive

`UpFileLive` is a Python tool designed to interact with the [upfile.live](https://upfile.live) file-sharing service. It allows users to upload files and retrieve shareable and downloadable links using both synchronous and asynchronous methods. [中文描述](README_zhCN.md)


## Installation

Install the library via pip:

```bash
pip install UpFileLive
```

### Dependencies

This library requires:

- Python 3.7 or later
- [playwright](https://playwright.dev/python/)

Install Playwright and dependencies:

```bash
pip install playwright
python -m playwright install
```

## Usage

### Initialization

```python
From UpFileLive import UpFileLive

# Initialize the UpFileLive object
file_uploader = UpFileLive("/path/to/your/file")
```

### Synchronous File Upload

```python
# Upload a file and get the share link
file_uploader.sync_upfile()
print(f"Share Link: {file_uploader.get_share_link()}")
```

### Asynchronous File Upload

```python
import asyncio

async def async_upload():
    await file_uploader.async_upfile()
    print(f"Share Link: {file_uploader.get_share_link()}")

asyncio.run(async_upload())
```

### Synchronous Download Link Retrieval

```python
# Set the share link and retrieve the download link (If you have already run the upfile function, you do not need to set this option.)
# file_uploader.share_link = "<your_share_link>" 
file_uploader.sync_download()
print(f"Download Link: {file_uploader.get_download_link()}")
```

### Asynchronous Download Link Retrieval

```python
async def async_download():
    # file_uploader.share_link = "<your_share_link>"
    await file_uploader.async_download()
    print(f"Download Link: {file_uploader.get_download_link()}")

asyncio.run(async_download())
```

### One-Click Upload and Download

#### Synchronous

```python
file_uploader.sync_upfile_download()
print(f"Share Link: {file_uploader.get_share_link()}")
print(f"Download Link: {file_uploader.get_download_link()}")
```

#### Asynchronous

```python
async def async_upload_download():
    await file_uploader.async_upfile_download()
    print(f"Share Link: {file_uploader.get_share_link()}")
    print(f"Download Link: {file_uploader.get_download_link()}")

asyncio.run(async_upload_download())
```


## License

This project is licensed under the [Modified MIT License](LICENSE).

