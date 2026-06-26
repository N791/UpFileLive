import os
import httpx
from loguru import logger

class UpFileLiveHttpx:
    """ upfile.live 文件分享工具类 (httpx 实现) """
    def __init__(self, file_path):
        self.file_path = file_path
        self.share_link = ''
        self.download_url = ''
        
        self.check_file()

    def get_share_link(self):
        return self.share_link
    
    def get_download_link(self):
        return self.download_url
    
    def check_file(self):
        try:
            if not os.path.exists(self.file_path):
                raise Exception("File does not exist")
        except Exception as e:
            logger.info(f"Error: {e}")
            
        file_size = os.path.getsize(self.file_path) / (1024 * 1024)
        try:
            if file_size > 500:
                raise Exception("File size exceeds 500MB")
        except Exception as e:
            logger.info(f"Error: {e}")

    def sync_upfile(self):
        """ 同步方式上传文件，获取分享链接 """
        file_size = os.path.getsize(self.file_path)
        # upfile.live 可能对 apk 后缀有限制，我们可以在请求 getUploadLink 时将其伪装成 zip
        original_name = os.path.basename(self.file_path)
        if original_name.endswith('.apk'):
            file_name = original_name.replace('.apk', '.zip')
        else:
            file_name = original_name

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        with httpx.Client(timeout=800.0, verify=False) as client:
            # 1. 获取上传链接
            try:
                resp = client.post(
                    'https://upfile.live/api/file/getUploadLink/', 
                    data={'vipCode': '', 'file_name': file_name}, 
                    headers=headers
                )
                resp.raise_for_status()
            except Exception as e:
                logger.error(f"Failed to get upload link: {e}")
                return

            data = resp.json().get('data', {})
            upload_url = data.get('upload_url')
            file_key = data.get('file_key')

            if not upload_url or not file_key:
                logger.error(f"Failed to get upload link: {resp.text}")
                return

            # 2. 上传文件到云存储 (S3/R2)
            with open(self.file_path, 'rb') as f:
                resp2 = client.put(upload_url, content=f)
            
            if resp2.status_code != 200:
                logger.error(f"Failed to upload file to S3, status: {resp2.status_code}")
                return

            # 3. 确认上传并获取 file_id
            resp3 = client.post(
                'https://upfile.live/api/file/upload/', 
                data={
                    'file_size': file_size,
                    'file_name': file_name,
                    'file_key': file_key
                }, 
                headers=headers
            )
            
            res_data = resp3.json().get('data', {})
            file_id = res_data.get('file_id')
            if file_id:
                # 拼接分享链接
                self.share_link = f"https://upfile.live/files/{file_id}"
                logger.info(f"Upload successful. Share link: {self.share_link}")
            else:
                logger.error(f"Failed to confirm upload: {resp3.text}")
    async def async_upfile(self):
        """ 异步方式上传文件，获取分享链接 """
        file_size = os.path.getsize(self.file_path)
        # upfile.live 可能对 apk 后缀有限制，我们可以在请求 getUploadLink 时将其伪装成 zip
        original_name = os.path.basename(self.file_path)
        if original_name.endswith('.apk'):
            file_name = original_name.replace('.apk', '.zip')
        else:
            file_name = original_name

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        async with httpx.AsyncClient(timeout=800.0, verify=False) as client:
            # 1. 获取上传链接
            try:
                resp = await client.post(
                    'https://upfile.live/api/file/getUploadLink/', 
                    data={'vipCode': '', 'file_name': file_name}, 
                    headers=headers
                )
                resp.raise_for_status()
            except Exception as e:
                logger.error(f"Failed to get upload link: {e}")
                return

            data = resp.json().get('data', {})
            upload_url = data.get('upload_url')
            file_key = data.get('file_key')

            if not upload_url or not file_key:
                logger.error(f"Failed to get upload link: {resp.text}")
                return

            # 2. 上传文件到云存储 (S3/R2)
            with open(self.file_path, 'rb') as f:
                resp2 = await client.put(upload_url, content=f)
            
            if resp2.status_code != 200:
                logger.error(f"Failed to upload file to S3, status: {resp2.status_code}")
                return

            # 3. 确认上传并获取 file_id
            resp3 = await client.post(
                'https://upfile.live/api/file/upload/', 
                data={
                    'file_size': file_size,
                    'file_name': file_name,
                    'file_key': file_key
                }, 
                headers=headers
            )
            
            res_data = resp3.json().get('data', {})
            file_id = res_data.get('file_id')
            if file_id:
                # 拼接分享链接
                self.share_link = f"https://upfile.live/files/{file_id}"
                logger.info(f"Upload successful. Share link: {self.share_link}")
            else:
                logger.error(f"Failed to confirm upload: {resp3.text}")


    def sync_download(self):
        """ 同步方式根据分享链接获取真实的下载链接 """
        if not self.share_link:
            logger.error("No share link available")
            return
            
        file_id = self.share_link.split('/')[-1]
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'referer': self.share_link,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
        
        with httpx.Client(timeout=30.0, verify=False) as client:
            try:
                resp = client.get(
                    f'https://upfile.live/download/{file_id}/',
                    headers=headers,
                    follow_redirects=False
                )
                
                if resp.status_code in (301, 302):
                    self.download_url = resp.headers.get('Location', '')
                    if self.download_url:
                        logger.info(f"Download URL obtained: {self.download_url}")
                    else:
                        logger.warning("No Location header found in response")
                else:
                    logger.warning(f"Unexpected status code {resp.status_code} when fetching download URL: {resp.text}")
            except Exception as e:
                logger.error(f"Error fetching download URL request: {e}")
    async def async_download(self):
        """ 异步方式根据分享链接获取真实的下载链接 """
        if not self.share_link:
            logger.error("No share link available")
            return
            
        file_id = self.share_link.split('/')[-1]
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'referer': self.share_link,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            try:
                resp = await client.get(
                    f'https://upfile.live/download/{file_id}/',
                    headers=headers,
                    follow_redirects=False
                )
                
                if resp.status_code in (301, 302):
                    self.download_url = resp.headers.get('Location', '')
                    if self.download_url:
                        logger.info(f"Download URL obtained: {self.download_url}")
                    else:
                        logger.warning("No Location header found in response")
                else:
                    logger.warning(f"Unexpected status code {resp.status_code} when fetching download URL: {resp.text}")
            except Exception as e:
                logger.error(f"Error fetching download URL request: {e}")

    def sync_upfile_download(self):
        """ 上传文件并直接获取下载链接 """
        self.sync_upfile()
        if self.share_link:
            self.sync_download()
    
    async def async_upfile_download(self):
        """ 异步方式上传文件并直接获取下载链接 """
        await self.async_upfile()
        if self.share_link:
            await self.async_download()