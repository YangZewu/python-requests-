import requests
from bs4 import BeautifulSoup
import openpyxl as op


class JingDong_Demo:
    # 设置url地址，请求头
    def __init__(self):
        self.url = 'https://search.jd.com/Search?'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&suggest=1.def.0.SAK7|MIXTAG_SAK7R,SAK7_M_AM_L5388,SAK7_M_COL_L19738,SAK7_S_AM_R,SAK7_SC_PD_R,SAK7_SM_PB_R,SAK7_SS_PM_R|&wq=shouji&pvid=e0afcb4b249042e68a9b7a1652951ff4',
        }

    # 设置页码参数，并通过bs4CSS选择器提取网页数据
    def re_data(self):
        num = 1
        name_list = []
        price_list = []
        for i in range(1, 3):
            params = {
                'keyword': '手机',
                'enc': 'utf-8',
                'wq': '手机',
                'pvid': 'cdb2d206ce00480fa68390a069aab4b0',
                'page': i,
                's': num,
                'click': '0',
                'psort': '3'
            }
            resp = requests.get(url=self.url, params=params, headers=self.headers)
            if resp.status_code == 200:
                try:
                    # 使用BS4提取网页文本
                    soup = BeautifulSoup(resp.text)
                    # 提取商品名称所在的标签
                    phone_name = soup.select(
                        "#J_searchWrap #J_container #J_main #J_goodsList .gl-warp .gl-item .gl-i-wrap .p-name a em")
                    # 提取价格所在的标签
                    phone_price = soup.select(
                        "#J_searchWrap #J_container #J_main #J_goodsList .gl-warp .gl-item .gl-i-wrap .p-price strong i")
                    # 去除无用的标签
                    [BeautifulSoup.extract(s) for s in soup('font')]
                    [BeautifulSoup.extract(s) for s in soup('span')]
                    # 遍历商品名称和价格，去除制表符和换行符
                    for name in phone_name:
                        name_list.append(name.text.replace('\t', '').replace('\n', ''))
                    for price in phone_price:
                        price_list.append(price.text)
                except Exception:
                    pass
            else:
                print('请求超时')
                self.re_data()
        self.write_data(name_list, price_list, num)

    # 将提取的数据写入到excel中
    def write_data(self, name, price, num):
        title = ['商品名称', '商品价格']
        li = []
        wk = op.Workbook()
        sheet = wk.create_sheet('手机', 0)
        sheet.append(title)
        for i, j in zip(name, price):
            li = [i, j]
            sheet.append(li)
        num += 30
        wk.save("按照销量爬取京东商城商品信息.xlsx")

    def run(self):
        self.re_data()


jd = JingDong_Demo()
jd.run()
