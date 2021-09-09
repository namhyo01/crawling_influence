import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import pandas as pd

class Crawling:
    def __init__(self):
        self.influence_list_link = []

    def crawling(self):
        URL = "https://in.naver.com/intro/influencers"
        category="라이프"

        driver = webdriver.Chrome(executable_path='chromedriver')
        driver.implicitly_wait(time_to_wait=5)
        driver.get(url=URL)
        category_tag = driver.find_elements_by_class_name('CategoryTabList__item___1-Jlu')


        # 메인 카테고리 클릭
        for main_category in category_tag:
            if(main_category.text=='라이프'):
                main_category.click()
        #서브 카테고리 클릭
        sub_category_tag = driver.find_elements_by_class_name('IntroCategoryGroup__keyword_item___332no')
        for sub_category in sub_category_tag:
            print(sub_category.text)
            if(sub_category.text=='육아'):
                sub_category.click()
        # 몇개를 가져올지 계속해서 내려가면서 가져온다.
        start = 5
        finish = 50
        scroll = int(finish/20)+1
        print(scroll)
        SCROLL_PAUSE_SEC = 1

        # 스크롤 높이 가져옴
        last_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(scroll):
            # 끝까지 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 1초 대기
            time.sleep(SCROLL_PAUSE_SEC)

            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(5) # 기달려서데이터 로딩
        influence_cnt = 0
        influence_list = driver.find_elements_by_class_name('IntroInfluencerItem__root___2aP9V')
        #인플루언서 리스트 링크 모으기 시작
        for influence in influence_list:
            influence_cnt+=1
            if(influence_cnt > finish): # finish를 넘으면 끝낸다 
                break
            if(influence_cnt<start):
                continue
            influence = influence.find_element_by_tag_name('a')
            self.influence_list_link.append(influence.get_attribute("href"))
            print(influence_cnt)
             # 인플루언서 리스트 링크 모음
        print(len(self.influence_list_link))

    def list_crawling(self):
        df = pd.DataFrame(columns=['이름','인스타그램','유튜브','블로그','네이버TV','포스트','스마트스토어'])
        for link in self.influence_list_link:
            #link 하나씩 처리
            req = Request(link,headers={'User-Agent':'Mozilla/5.0'})
            try:
                with urlopen(req) as response:
                    data = {'이름': '','인스타그램':'','유튜브':'','블로그':'','네이버TV':'','포스트':'','스마트스토어':''}
                    html = response.read()
                    soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
                    #이름
                    name = soup.find("div",{'class':'hm-component-homeCover-profile-info'})
                    name = name.find("strong")
                    name = name.string
                    data['이름'] = name

                    #인플루언서 url겟
                    influence_socials = soup.find_all("div",{"class":"hm-component-channel-title-inner"})
                    for social in influence_socials:
                        social_link = social.find("a",{"class":"hm-component-channel-title-link"})
                        influence_social_link = social_link['href']
                        social_link = social_link.find("span",{"class":"hm-component-channel-logo"})
                        try:
                            data[social_link['aria-label']] = str(influence_social_link)
                            
                        except:
                            # 정규표현식 처리하고 싶으나 혹시모르는 다른 예제들 덕에 방지
                            if(influence_social_link.find('//blog.naver')!=-1):
                                data['블로그'] = influence_social_link
                            elif influence_social_link.find('//www.instagram.com')!=-1:
                                data['인스타그램'] = influence_social_link
                            elif influence_social_link.find('//www.youtube.com')!=-1:
                                data['유튜브'] = influence_social_link
                            elif influence_social_link.find('//post.naver.com')!=-1:
                                data['포스트'] = influence_social_link
                            elif influence_social_link.find('//smartstore.naver.com')!=-1:
                                data['스마트스토어'] = influence_social_link
                    df = df.append(data, ignore_index=True)
            except Exception as e:
                print(e)
        df.to_excel('influence.xlsx', index=False)
        
if(__name__=="__main__"):
    crawl = Crawling()
    crawl.crawling()
    crawl.list_crawling()