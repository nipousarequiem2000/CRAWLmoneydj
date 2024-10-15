#MONEY_DJ
#拿到文章超連結
import requests
from lxml import html
from lxml import etree
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote

# 基本 URL
base_url = "https://www.moneydj.com/kmdj/news/newsreallist.aspx"
params = {
    'a': 'mb010000'  # 固定參數
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
}
#####################
# 根據需要更改頁數  #
#####################500-1000
# 用來儲存結果的列表
results = []
start_page=1
end_page=100
# 遍歷每一頁
for page in range(start_page, end_page):
    if page > 1:
        params['index1'] = str(page)  # 從第二頁開始，加入 index1 參數

    # 發送請求
    list_req = requests.get(base_url, params=params,headers=headers)
    #將整個網站的程式碼爬下來

    soup = BeautifulSoup(list_req.content, "html.parser")
    #找到table這個標籤裡面要的

    getAllNews= soup.find('table',{'class':'forumgrid'})
    #找到各標題、時間、連結
    #夾在<td>裡面

    td = getAllNews.find_all('td')


    for i in range(0,len(td),3):
        time=td[i].text
        title=td[i+1].text
        full_link='https://www.moneydj.com/'+ td[i+1].a.get("href")


        results.append({'文章時間': time,'文章標題': title, '文章超連結': full_link})
        #print(time)
        #print(title)
        print(full_link)



# 將結果轉換為 DataFrame
df = pd.DataFrame(results)
#進入每篇連結抓取內文資料
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 設置重試機制
session = requests.Session()
retry_strategy = Retry(
    total=5,  # 重試次數
    backoff_factor=1,  # 重試之間的等待時間增長係數
    status_forcelist=[429, 500, 502, 503, 504],  # 在這些HTTP狀態碼下重試
    allowed_methods=["GET"]  # 對GET請求重試
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

def scrape_news_content(news_urls):
    news_data = []

    for url in news_urls:
        try:
            # 發送HTTP請求
            response = session.get(url, headers=headers)
            response.raise_for_status()  # 確保響應成功
            # 解析網頁內容
            html = etree.HTML(response.content)

            # 使用XPath抓取資料
            title = html.xpath('//span[@id="MainContent_Contents_lbTitle"]/text()')
            time = html.xpath('//span[@id="MainContent_Contents_lbDate"]/text()')
            # 嘗試提取<p>中的文字
            content = html.xpath('//p/text()')

            # 嘗試提取<p>中的<font>文字
            if len(''.join(content).strip()) < 100:
                content = html.xpath('//p/font/text()')

            # 嘗試提取<p>中的<span>文字
            if len(''.join(content).strip()) < 100:
                content = html.xpath('//p/span/text()')
            # 嘗試提取<p>中的<br>文字
            if len(''.join(content).strip()) < 100:
                content = html.xpath('//p/br/text()')

            # 提取<p>中的所有文字
            if len(''.join(content).strip()) < 100:
                content = html.xpath('//*[@id="highlight"]/article/text()')



            # 清理和格式化數據
            title = title[0] if title else 'N/A'
            time = time[0] if time else 'N/A'
            content = ''.join(content).strip() if content else 'N/A'


            # 添加到新聞數據列表
            news_data.append({
                '新聞標題': title,
                '日期': time,
                '內文': content,
            })

        except (requests.exceptions.RequestException, IndexError) as e:
            print(f'無法從 {url} 獲取數據：{e}')
            time.sleep(2)  # 等待一段時間後重試

    return news_data

link_list=df['文章超連結']
result2=scrape_news_content(link_list)
DF=pd.DataFrame(result2)
print(DF)