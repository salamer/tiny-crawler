import requests
from bs4 import BeautifulSoup
from leapcell import Leapcell, LeapcellField
from io import BytesIO
from typing import List, Dict


leapclient = Leapcell("http://localhost:8080", "1662758095545237504")
table = leapclient.table("test1/myproject", "1662758095545237504")

header = {
    'Host': 'www.adscientificindex.com',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://www.adscientificindex.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1811) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Site': 'same-origin',
}

def get_page(page:int):
    url = 'https://www.adscientificindex.com/?s={}&sl5h=1'
    return url.format(page * 100)

def insert_data(item : Dict):
    the_insert_data = dict()
    if item["avatar"] is not None:
        try:
            image_url = "https://www.adscientificindex.com" + item["avatar"]
            response = requests.get(image_url, headers=header)
            if response.status_code != 200:
                print("error {} {}".format(response.status_code, image_url))
                return
            if len(response.content) == 0:
                print("error {} {}".format(response.status_code, image_url))
                return
            image_info = leapclient.upload(response.content)
            image_info = image_info["raw"]
        except Exception as e:
            print("error {}".format(e))
            image_info = None
    the_insert_data["1662758654872453120"] = item["name"]
    the_insert_data["1662759717960744960"] = [image_info]
    the_insert_data["1662758690834415616"] = item["country"]
    the_insert_data["1662758800314138624"] = item["institution"]
    the_insert_data["1662758853590188032"] = item["subject"]
    the_insert_data["1662758964416282624"] = item["sub_subject"]
    the_insert_data["1662759052781879296"] = float(item["h_index_total"])
    the_insert_data["1662759172244045824"] = int(item["citation_total"])
    return the_insert_data

def insert_multi_data(datas:List[Dict]):
    if datas is None:
        return
    the_insert_data = []
    for item in datas:
        if table.get({
            "1662758654872453120" : item["name"]
        }):
            continue
        print("ohoihiohioioh")
        res = insert_data(item)
        if res is None:
            continue

        table.create(res)
    return

def process_page(page:int):
    url = get_page(page)
    print(url)
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.findAll(True, {'class': 'table table-striped table-bordered table-sm'.split(' ')})
    if len(table) == 0:
        return
    
    data = []

    for item in table[0].findAll('tr'):
        item_data = dict()

        tds = item.findAll('td')
        
        if len(tds) < 14:
            print("error {}",len(tds))
            continue

        name = tds[4].get_text().strip()
        avatar = tds[4].find('img')['src']
        country = tds[5].text.strip()
        institution = tds[6].text.strip()
        subject_info = tds[7].text.strip().split('\n')
        subject = subject_info[0].strip().split("/")
        h_index_total = tds[8].text.strip()
        citation_total = tds[14].text.strip()
        sub_subject = None
        if len(subject_info) > 1:
            sub_subject = subject_info[2].strip().split("|")

        item_data['name'] = name.replace('                                               i', '')
        item_data['avatar'] = avatar
        item_data['country'] = country
        item_data['institution'] = institution
        item_data['subject'] = subject
        item_data['sub_subject'] = sub_subject
        item_data['h_index_total'] = h_index_total
        item_data['citation_total'] = citation_total
        data.append(item_data)

    # print(data)


    return data

def get_ad_index():
    for i in range(1, 100):
        url = get_page(1)
        r = requests.get(url, headers=header)
        return r.json()
    
def all_ad_index():
    for i in range(1, 13512):
        item_datas = process_page(i)
        insert_multi_data(item_datas)

if __name__ == '__main__':
    # table.delete(
    #     LeapcellField("1662759172244045824") > 0
    #     )
    all_ad_index()