# MoneyDJ 新聞爬蟲

從 [MoneyDJ](https://www.moneydj.com/kmdj/news/newsreallist.aspx?a=mb010000) 網站爬取財經新聞資料的爬蟲程式。資料包括每篇文章的新聞標題、發布時間以及內文。

## 需求套件

在執行程式之前，請先安裝以下 Python 套件：

- `requests`
- `lxml`
- `pandas`
- `bs4` (BeautifulSoup)
- `urllib`

## 使用說明

**設定爬取頁數範圍**  
   在執行程式之前，請修改程式中的變數來設置爬取的頁數範圍，例如：

```python
   start_page = 1
   end_page = 100
```
