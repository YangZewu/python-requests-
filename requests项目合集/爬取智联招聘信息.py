"""
爬虫项目：按照地区和心仪岗位爬取智联招聘的数据
代码思路：
1.获取网页地址，伪装请求头
2.通过使用正则表达式提取返回数据中的'公司名称', '公司规模', '学历要求', '职位名称', '薪酬范围', '工作经验', '城市', '地区'
3.通过openpyxl模块将数据写入到excel中
4.使用面向对象的编程思维
5.将抓取到的职位信息写入到excel表格中
"""
import requests
import re
import openpyxl as op


class ZhiLianDemo:
    # 初始化地址和请求头信息
    def __init__(self, city, position_name):
        self.city = city
        self.position_name = position_name
        self.url = 'https://sou.zhaopin.com/?jl={}&kw={}&p=1'.format(self.city, self.position_name)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
            'cookie': 'x-zp-client-id=ea766688-7dba-4904-c427-9a7da3660f66; urlfrom2=121114589; adfcid2=cn.bing.com; adfbid2=0; at=082532847c3e4eb393956760fe381e81; rt=301cd29c9d5d4e3eadf87feb2f638283; sts_deviceid=1805a93a76db25-0172505183c761-7b422f23-1638720-1805a93a76ebc3; ZP_OLD_FLAG=false; TEMPLATESWAY=0; LastCity%5Fid=682; LastCity=%E5%8E%A6%E9%97%A8; FSSBBIl1UgzbN7NO=5OYUL2tfKHp0vbpJHi1MpyI22cC5CwxjpgfgdGsn82GkdNp9jEOUHs0eJ_6Zd63MOrnEitzX7krgy.xIIV.umSG; _uab_collina=165087955160902467486257; locationInfo_search={%22code%22:%22687%22%2C%22name%22:%22%E6%BC%B3%E5%B7%9E%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; selectCity_search=682; urlfrom=121114589; adfcid=cn.bing.com; adfbid=0; acw_tc=2760829416509406929584171e6950069c757b604507b69884844b2636b3b8; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221132905362%22%2C%22first_id%22%3A%221805a934adb516-00e747256f2ddcc-7b422f23-1638720-1805a934adc664%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221805a934adb516-00e747256f2ddcc-7b422f23-1638720-1805a934adc664%22%7D; FSSBBIl1UgzbN7NP=53bwfICxv3UZqqqDq3eVE9aXVz1n4PG5OaKc3GBdIqaN3NdFNCsGp7Rv2nFyiY6irnYNijo3phJJ5w81mgq8B_R0pZ3iuIcQyEv0L30pxojTYbCQk28I5twFahZtKmZVt_yqZb8LcULCVyhJX7PcVvAPVEQ5h.aXiiKeNWC2xn1aZS9wizUQ9hhQKurb8crcfqpidhGSXJRR2MeI7U4gAgY3KijbzTUsG1WwZ8wz0JJ_jfVRnRUdjk_E.jtQOUZKwdypd6yEf8uGjdApN1FVZNeeg5j2AX6FBXQk5.9hLyDIRDvF4Ad.uNbpqS3IruN6mGesCfPgQI16AzWqvkXJHUK; ssxmod_itna=iqjxci0Q9DgD2Dl8Ys5DQ6xiInDCTwhrnuaoDsNmDSxGKidDqxBWelDDtvkHkKHRZxP0ep/CO7q4HWhC7t3A8zb4GLDmKDybjEehYD4+KGwD0eG+DD4DW4qAoDexGPc0wLKGWD4qDOD3qGyn+=DAS=Dbr=RDiUZDDtH04G2D7tc+qdKVkbDAdhBzBxcD0U3xBdqtZ4czeaaXAUBDaWerhjDqeGuDG6VWqGmn8bDCE6MiQ+=KDppwA30QipezY5=UYx4KAmAbiA=9AhKW/41YGDhzBwbzIZdDDf2LbD==; ssxmod_itna2=iqjxci0Q9DgD2Dl8Ys5DQ6xiInDCTwhrnuPikvNkeDlrCxGq03WNuLUD6mQs=vY2IFSUZucXkMQ+dxrIdZhk7rELYUxynTDKMbdDLxijd4D=; ZL_REPORT_GLOBAL={%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%22325678ab-2ec1-4c57-9b7c-bfb462844b66-job%22}}',
        }

    # 伪装请求头
    def init_demo(self):
        resp = requests.get(url=self.url, headers=self.headers)
        return resp.content.decode('utf8')

    # 使用正则表达式抓取对应信息,并将其写入到excel
    def re_demo(self, url_list):
        data = url_list
        # 公司名称
        companyName = re.findall('"companyName":"(.*?)"', data)
        # 职位名称
        name = re.findall('"menVipLevel":(.*?),"name":"(.*?)"', data)
        # 公司规模
        companySize = re.findall('"companySize":"(.*?)"', data)
        # 学历要求
        education = re.findall('"education":"(.*?)"', data)
        # 薪酬范围
        salary60 = re.findall('"salary60":"(.*?)"', data)
        # 工作经验
        workingExp = re.findall('"workingExp":"(.*?)"', data)
        # 城市
        workCity = re.findall('"workCity":"(.*?)"', data)
        # 区域
        cityDistrict = re.findall('"cityDistrict":"(.*?)"', data)
        # 因为职位名称中包含两个参数，这里使用元组解包并添加为新的列表
        position_name_list = []
        for i, j in name:
            position_name_list.append(j)
        position_list = []
        title = ['公司名称', '公司规模', '学历要求', '职位名称', '薪酬范围', '工作经验', '城市', '地区']
        wk = op.Workbook()
        sheet = wk.create_sheet(self.position_name, 0)
        sheet.append(title)
        for cn, cs, ed, pos, sal, we, wc, cd in zip(companyName,
                                                    companySize,
                                                    education,
                                                    position_name_list,
                                                    salary60,
                                                    workingExp,
                                                    workCity,
                                                    cityDistrict):
            position_list = [cn, cs, ed, pos, sal, we, wc, cd]
            sheet.append(position_list)
        wk.save('智联招聘{}地区{}职位招聘信息.xlsx'.format(self.city, self.position_name))

    def run(self):
        self.re_demo(self.init_demo())


if __name__ == '__main__':
    zhilian = ZhiLianDemo('厦门', 'python')
    zhilian.run()
