import requests       #引入requests模組
from lxml import etree
import time
#import xpath
#import xml.etree.ElementTree as ET
#import etree

#key=['ldlfsldsflsldfs','sdfsd']
def google_search(string, choice):
    
    key = string.split()
    # key=['dangerous','object']

    key_added='+'.join(key)
    #print(key_added)
    url = f"https://www.google.com/search?hl=en&q={key_added}"

    # print("input your choice:")      #choice=0or1  0為一般搜尋 1為進階搜尋
    # choice = int(input())
    #print("%d" %choice )


    #用GET下載網頁
    #一般搜尋
    if choice == 0:
        url = f"https://www.google.com/search?hl=en&q={key_added}"
        #print(url)
    #進階搜尋
    elif choice == 1:
        url = f"https://www.google.com/search?hl=en&q=\"{key_added}\"&oq=\"{key_added}\""
        #print(url)
    #錯誤輸入
    else:
        print("Wrong input")

    #if同時有一般也有進階 eat "apple pie"


    #加上user agent讓網頁識別身分
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }

    response = requests.get(url, headers=headers)

    html = response.text

    # print(response.text)
    page = etree.HTML(html)
    num = -1 
    if html.find("did not match any documents") > 0 or html.find("No results found for") > 0:
        # print("0 result")
        num = 0

    else:
        #print(page.xpath(u'//*[@id="result-stats"]/text()'))
        
        #print(response.status_code)       #伺服器回應的狀態碼

        result=page.xpath(u'//*[@id="result-stats"]/text()')
        result="".join(result)     #List to string
        result=result.split(" ")
        for i in range(len(result)):
            if result[i].find("result")!=-1:
                num = int(float(result[i-1].replace(',','')))
                # print(result[i-1])
        # print(result)
        # result = int(float(result[1].replace(',','')))

    return num

re = google_search("person is inherently entitled", 1)
sec = 0
while re == -1:
    print(sec)
    sec += 1
    time.sleep(1)
    re = google_search("person is inherently entitled", 1)
# print(google_search("is a water resource", 1))

