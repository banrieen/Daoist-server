## 爬取同花顺金融报表
# 指定上市公司股票编码
# 获取在同花顺上的财务信息
# 整合格式和图表--可以自动下载
# 导出为 excel

# import scrapy

# class StockSpider(scrapy.Spider):
#     name = "stock_financial"
#     allowed_domains = ["stockpage.10jqka.com.cn"]
#     start_urls = ['https://stockpage.10jqka.com.cn/603986/operate/#analysis']

#     def parse(self, response):
#         # 这里需要根据网页结构解析财务报表数据
#         # 使用 scrapy Shell 可以帮助你分析网页结构，例如：response.xpath('//div[@class="report"]')
#         # 你可以提取你需要的数据并将其存储到字典或其他合适的数据结构中
#         # 例如：

#         financial_data = {
#             'revenue': response.xpath('//span[@class="item-value"]/text()').get(),
#             'profit': response.xpath('//span[@class="item-value"]/text()').get(),
#             # ... 其他财务指标
#         }
#         yield financial_data



# def pachong(url, params):

#     # 发送请求，获取网页源码
#     response = requests.get(url, params=params)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # 找到想要的数据元素（例如表格）
#     table = soup.find('table', class_='stock-report-table')
#     print(f"=======> {table}")

# def output():
#     pass
#     # # 将表格转换为 Pandas 数据框
#     # data = []
#     # for row in table.find_all('tr'):
#     #     cols = row.find_all('td')
#     #     if len(cols) > 0:
#     #         data.append([col.text.strip() for col in cols])

#     # df = pd.DataFrame(data)

#     # # 导出到 Excel 文件中
#     # df.to_excel('stock_report.xlsx', index=False)

import requests

def export_excel(url,stock_code):


    # url = "https://www.example.com/your_excel_file.xlsx"  # Replace with the actual URL
    response = requests.get(url)

    if response.status_code == 200:
        with open("downloaded_excel.xlsx", "wb") as f: 
            f.write(response.content)
        print("Excel file downloaded successfully!")
    else:
        print(f"Error downloading file: {response.status_code}")


if __name__ == "__main__":
    # 指定网址和参数
    stock_code = 603986     ## 兆易创新
    url = f'https://stockpage.10jqka.com.cn/{stock_code}/finance/' 
    url = f'http://basic.10jqka.com.cn/api/stock/export.php?export=cash&type=simple&code={stock_code}'
    params = {'type': 'report'}
    export_excel(url,stock_code) 
    ## Error downloading file: 403