# -*- coding: utf-8 -*-
import pandas as pd
import requests
from tqdm import tqdm
import urllib.request

PAGES = range(1,11)
CATEGORY = ['백팩', '힙색', '핸드백', '크로스백','숄더백','에코백']
SAVE_PATH = 'D:/sesac/data/raw/'


def get_item_data(item, PAGES):
    total_df = pd.DataFrame()
    
    for page in tqdm(PAGES):
        pid_list = [] # 아이템 리스트 담기
        bunjang_url = f'https://api.bunjang.co.kr/api/1/find_v2.json?q={item}&order=date&page={page}&stat_device=w&stat_category_required=1&req_ref=search&version=4'
        response = requests.get(bunjang_url)
        
        try:
            item_list = response.json()["list"]
            ids = [item["pid"] for item in item_list]
            pid_list.extend(ids)
        except:
            continue
        
        df = pd.DataFrame()
        product_id, image_link = [],[]
        for pid in pid_list:
            url = f"https://api.bunjang.co.kr/api/1/product/{pid}/detail_info.json?version=4"
            response = requests.get(url)
            product_id.append(item)
            try :
                image_link.append(response.json()['item_info']['product_image'])
            except : 
                image_link.append(0)
        df['product_id'] = product_id
        df['image'] = image_link
        total_df = pd.concat([total_df, df]).reset_index(drop=True)
    return total_df
    
    
def save_img(df):
    cnt=0
    for i, url in enumerate(df['image'].tolist()):
        # name = cvt_item_name(df['product_id'][i]) + '_' + str(cnt) + '.jpg'
        name = df['product_id'][i] + '_' + str(cnt) + '.jpg'
        try:
            urllib.request.urlretrieve(url, SAVE_PATH + name)
            cnt +=1
        except:
            continue
        
        
        
def cvt_item_name(item):
    if item == '여성지갑':
        return 'w_wallet'
    if item == '남성지갑':
        return 'm_wallet'
    if item == '여성가방':
        return 'w_bag'
    if item == '남성가방':
        return 'm_bag'
    if item == '가방':
        return 'bag'
    if item == '지갑':
        return 'wallet'    
    else:
        return 'none'
    
    
if __name__ == "__main__":
    for item in CATEGORY:
        df = get_item_data(item, PAGES)
        save_img(df)
        print(f'===========save {item} image Done===========')