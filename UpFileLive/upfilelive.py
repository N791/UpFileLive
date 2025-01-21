from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

class UpFileLive:
    """ upfile.live 文件分享工具类，用于上传文件并生成分享链接或下载链接 """
    def __init__(self, file_path):
        self.file_path = file_path  # 文件路径
        self.share_link = ''        # 分享链接
        self.download_link = ''     # 下载链接

    def get_share_link(self):
        """ 获取分享链接 """
        return self.share_link
    
    def get_download_link(self):
        """ 获取下载链接 """
        return self.download_link

    def sync_upfile(self):
        """ 
        同步方式上传文件，上传完成后将分享链接保存在 `share_link` 中。
        使用 Playwright 的同步 API 与浏览器交互。 
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto('https://upfile.live')
            page.wait_for_selector('button.button')
            page.click('button.button')
          
            file_input = page.locator('input[type="file"]') 
            file_input.set_input_files(self.file_path)  
            page.wait_for_url('**/files/*')  
            self.share_link = page.url
            
            browser.close()
    
    async def async_upfile(self):
        """ 
        异步方式上传文件，上传完成后将分享链接保存在 `share_link` 中。
        使用 Playwright 的异步 API 与浏览器交互。
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
        
            await page.goto('https://upfile.live')
            await page.wait_for_selector('button.button')
            await page.click('button.button')
          
            file_input = page.locator('input[type="file"]') 
            await file_input.set_input_files(self.file_path)  
            await page.wait_for_url('**/files/*')  
            self.share_link = page.url
            
            await browser.close()
            
    def sync_download(self):
        """ 
        同步方式根据分享链接获取下载链接，并将其保存在 `download_link` 中。
        使用 Playwright 的同步 API 实现。
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto(self.share_link)
            page.click('a:has-text("Download File")') 
            with page.expect_download() as download_info:
                page.click('a:has-text("Confirm")')
                
            download = download_info.value
            self.download_url = download.url
            
            browser.close()
            
    async def async_download(self):
        """ 
        异步方式根据分享链接获取下载链接，并将其保存在 `download_link` 中。
        使用 Playwright 的异步 API 实现。
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(self.share_link)
            await page.click('a:has-text("Download File")') 
            async with page.expect_download() as download_info:
                await page.click('a:has-text("Confirm")')
            
            download = await download_info.value
            self.download_url = download.url
            
            await browser.close()
            
    def sync_upfile_download(self):
        """ 
        同步方式上传文件并直接获取下载链接。
        上传完成后获取分享链接，随后访问分享链接页面以生成下载链接。
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto('https://upfile.live')
            page.wait_for_selector('button.button')
            page.click('button.button')
          
            file_input = page.locator('input[type="file"]') 
            file_input.set_input_files(self.file_path)  
            page.wait_for_url('**/files/*')  
            self.share_link = page.url
            
            page.click('a:has-text("Download File")') 
            with page.expect_download() as download_info:
                page.click('a:has-text("Confirm")')
                
            download = download_info.value
            self.download_url = download.url
            
            browser.close()
            
    async def async_upfile_download(self):
        """ 
        异步方式上传文件并直接获取下载链接。
        上传完成后获取分享链接，随后访问分享链接页面以生成下载链接。
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
        
            await page.goto('https://upfile.live')
            await page.wait_for_selector('button.button')
            await page.click('button.button')
          
            file_input = page.locator('input[type="file"]') 
            await file_input.set_input_files(self.file_path)  
            await page.wait_for_url('**/files/*')  
            self.share_link = page.url
        
            await page.click('a:has-text("Download File")') 
            async with page.expect_download() as download_info:
                await page.click('a:has-text("Confirm")')
            
            download = await download_info.value
            self.download_url = download.url
            
            await browser.close()
    