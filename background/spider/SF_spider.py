# coding:utf-8
'''
@author:    Fan
@python:    2.7
@description:
            爬取segmentfault问题
'''
import os,sys
import requests
from bs4 import BeautifulSoup as bs
import time,json,random


class SF_spider():

    def __init__(self,urls):
        self.urls = urls
        self.links = []
        User_Agent = [
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17',
                    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
                    'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124'
                    ]
        n = random.randint(0,4)
        self.headers = {'User-Agent':User_Agent[n]}
    def get_url(self):
        for url in self.urls.values():
            for page in range(2,7):
                self.get_link(url)
                url = url.split('type=votes')[0] + 'type=votes&page={}'.format(page)

    def get_link(self,url):
        r = requests.get(url, headers=self.headers, timeout = 5)
        if r.status_code == 200:
            soup = bs(r.text, "html.parser")
            # print r.text
            for i in soup.find_all(class_ = 'stream-list__item'):
                link = 'https://segmentfault.com{}'.format(i.find_all('a')[2].get('href'))
                self.links.append(link)

    def get_question(self):
        index = 0
        questions = []
        for link in self.links:
            time.sleep(10)
            r = requests.get(link, headers = self.headers, timeout = 10)
            soup = bs(r.text, "html.parser")
            url = r.url
            title = soup.find_all(id = 'questionTitle')[0].find_all('a')[0].get_text()
            tags = []
            for tag in soup.find_all(class_ = 'tagPopup mb5'):
                word = tag.find_all('a')[0].get_text()
                tags.append(word)
            dsc = soup.find_all(class_ = 'question fmt')[0]
            haha = soup.find_all(class_ = 'post-topheader__side list-unstyled')[0].find_all('strong')
            attention = haha[0].get_text()
            favourite = haha[1].get_text()
            glance = haha[2].get_text()
            answers = soup.find_all(class_ = 'widget-answers')[0].find_all(class_ = 'answer fmt')
            try:
                answer_accepted = answers[0]
                answer1 = answers[1]
                answer2 = answers[2]
            except:
                answer_accepted = ''
                answer1 = ''
                answer2 = ''
            p_time = soup.find_all(class_ = 'question__author')[0].get_text()
            p_time = p_time.split('日')[0].split(' ')[-1].replace('年','-').replace('月','-')
            dict = {'title':title, 'url':url, 'tags':tags, 'dsc':str(dsc), 'attention':attention, 'favourite':favourite, 'glance':glance, 'answer_accepted':str(answer_accepted), 'answer1':str(answer1), 'answer2':str(answer2), 'time':p_time}
            index += 1
            questions.append(dict)
            print('{} : {}\n{}'.format(index,title,url))
        all_questions = {'python':questions}
        with open('a.json', 'a') as f:
            # json乱码，输入python为ascii
            f.write(json.dumps(all_questions, sort_keys=True, indent=2, ensure_ascii=False))
            # json正常，输入python为乱码
            # f.write(json.dumps(all_questions, sort_keys=True, indent=2)

if __name__=="__main__":
    urls = {
            'cpp' : 'https://segmentfault.com/t/c%2B%2B?type=votes',
            'c' : 'https://segmentfault.com/t/c?type=votes',
            'java' : 'https://segmentfault.com/t/java?type=votes',
            '数据库' : 'https://segmentfault.com/t/%E6%95%B0%E6%8D%AE%E5%BA%93?type=votes',
            'linux' : 'https://segmentfault.com/t/linux?type=votes',
            'python': 'https://segmentfault.com/t/python?type=votes'
           }
    # s = SF_spider(urls)
    # s.get_url()
    # s.get_question()

with open('a.json', 'r') as f:
    a = json.load(f)
    print (a['python'][1]['title'].encode('utf-8','ignore'))
