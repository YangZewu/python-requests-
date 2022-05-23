import requests
import re
import openpyxl as op
import time

# 根据销量排行爬取淘宝商品信息
class TaoBao_Spider:
    # 初始化连接以及请求标头
    def __init__(self, name):
        self.name = name
        self.url = "https://s.taobao.com/search?q=" + name
        self.headers = {
            'user - agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 101.0.4951.64Safari / 537.36Edg / 101.0.1210.47',
            'referer': 'https://s.taobao.com/search?q=%E6%89%AB%E5%9C%B0%E6%9C%BA%E5%99%A8%E4%BA%BA&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_20170306',
            'cookie': 'Gnj2KutYxyyjIxxpscO0lcHUIn1ExskKp0qqum8rQvOJ1bR15WReGZusKBRk0V%2FHC92m72yk%2Fr7KQ54i99RNeeZbczcUZaiPZFfmVcBuMenI1R8ZsZr; uc3=vt3=F8dCvC%2B%2Bv%2B95XHtVHLo%3D&nk2=u%2F55GK8xdU0dhYRM&id2=UU6m2ESS67qpdg%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; lgc=%5Cu4E36%5Cu711A%5Cu4E16%5Cu7EA2%5Cu83B2%5Cu4E36; uc4=nk4=0%40uQxdg0edRaQ%2BjyeN0B9Dd1G%2BxpMltzE%3D&id4=0%40U2xrdVzLvlU3DlkHVVyC4s9Lcr%2FG; tracknick=%5Cu4E36%5Cu711A%5Cu4E16%5Cu7EA2%5Cu83B2%5Cu4E36; _cc_=URm48syIZQ%3D%3D; thw=cn; enc=D2QxCOQVWILtQ9QyFw8xGRIdzUZysp0nfaJWXduvwCf0AzMdoySixodEhhFvtWuS58C%2B8xDm13bDc2Qzwbxqkg%3D%3D; mt=ci=-1_0; _m_h5_tk=a863e7714b94b2b70a8143c6d5bab7d9_1652796514641; _m_h5_tk_enc=8cf789004dc60a89148e4ad7c7a2c2e4; _tb_token_=3387e9eee49e7; uc1=cookie14=UoexMNMyt3n6ug%3D%3D; cookie2=1f8b669a73c38dd395eecc1209778cbc; l=eBrWvDWlgtWafNGCBOfanurza77OSIRYjuPzaNbMiOCPOWfp5cFFW6fmO-Y9C3GVh65eR3rk8yKDBeYBqgjonxvtIosM_Ckmn; isg=BBwcoS_qkqx892UcTgscxEG-7TrOlcC_WKCPU_Yd9YfqQbzLHqCvTK2zpam5cvgX'
        }

    # 伪装参数信息并获取解析数据
    def re_deta(self):
        # 定义商品名称的列表
        sp_name = []
        # 定义商品价格的列表
        sp_price = []
        # 定义商品店铺的列表
        sp_shop = []
        # 设置页数信息爬取对应页数的数据
        for i in range(0, 5):
            params = {
                'imgfile': '',
                'js': '1',
                's': i * 44,
                'stats_click': 'search_radio_all%3A1&initiative_id=staobaoz_20220517',
                'ie': 'utf8',
                'sort': 'sale-desc',
                'bcoffset': '0',
                'p4ppushleft': '%2C44'
            }
            # 伪装请求
            response = requests.get(url=self.url, headers=self.headers, params=params)
            if response.status_code == 200:
                try:
                    # 页面数据
                    data = response.content.decode('utf8')
                    # 商品名称
                    name = re.findall('"raw_title":"(.*?)"', data)
                    # 商品价格
                    price = re.findall('"view_price":"(.*?)"', data)
                    # 商品店铺
                    shop = re.findall('"nick":"(.*?)"', data)
                    sp_name.append(name)
                    sp_price.append(price)
                    sp_shop.append(shop)
                except Exception as e:
                    with open('异常信息.txt', 'w+') as f:
                        f.write(str(e) + '\n')
            else:
                print('连接超时')
                self.re_deta()
        # 调用写入数据的方法
        self.write_data(self.name, sp_name, sp_price, sp_shop)

    # 将数据写入到excel
    def write_data(self, title, name, price, shop):
        # 定义列名
        title_list = ['商品名称', '商品价格', '店铺名称']
        # 商品信息
        commodity_info = []
        # 模块实例化
        wk = op.Workbook()
        # 定义工作簿
        sheet = wk.create_sheet(title, 0)
        # 写入列名
        sheet.append(title_list)
        # 解析数据并写入
        for i, j, k in zip(name, price, shop):
            for n, s, p in zip(i, j, k):
                commodity_info = [n, s, p]
                print('开始保存信息：{}'.format(n))
                time.sleep(0.1)
                sheet.append(commodity_info)
        # 保存文件
        wk.save('淘宝关于{}按销量排行信息.xlsx'.format(title))
        print('保存成功')
    # 执行
    def run(self):
        self.re_deta()


# 程序入口
if __name__ == '__main__':
    taobao = TaoBao_Spider("扫地机器人")
    taobao.run()
