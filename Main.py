from func import saving_files,drop_duplicate,create_product_dir,create_each_product_dir
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import requests
import random
import shutil
import time
import os



def Getting_urls():
    category_listing = []
    for x in range(1,60):
        print(f'\n X CURRENTLY ON {x} \n ')
        url = f'https://www.jumia.com.ng/baby-products/?page={x}#catalog-listing'
        res = requests.get(url)

        soup = BeautifulSoup(res.content,"html.parser")
        # tree = html.fromstring(res.content)

        #   GETTING LINK SECTION
        links = [name.get('href') for name in soup.findAll('a')]
        # print(links)

        all_link = []
        for link in links:
            try:
                if '.html' in link and link not in all_link:
                    all_link.append('https://www.jumia.com.ng'+link)
            except:
                pass
        # USING LINKS TO GET ELEMENT IN THAT TEAMS
        # print('LENGHT OF ALL LINKS = ',len(all_link))

        url_saving_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'All Urls/ALL URL.csv')
        data = {'CATEGORY':[],'URLS':[]}
        for docs in all_link:
            data['CATEGORY'].append(url.split('/')[3])
            data['URLS'].append(docs)

        saving_files(data=data,path=url_saving_path)
        print('LENGHT OF ALL LINKS = ',len(all_link))
        print(f'\n X PREVIOUSLY ON {x} \n ')
    drop_duplicate(path=url_saving_path)

# Getting_urls()



def save_product_pic(url,pic_saving_dir):
    res = requests.get(url)
    soup = BeautifulSoup(res.content,"html.parser")

    #   GETTING LINK SECTION
    links = [name.get('href') for name in soup.findAll('a')]

    all_link = []
    for link in links:
        try:
            if '.jpg' in link or '.png' in link or '.jpeg' in link and link not in all_link:
                all_link.append(link)
        except:
            pass

    for img_ind,img_url in enumerate(all_link):
        res = requests.get(img_url)
        with open( os.path.join(pic_saving_dir,f'pic_{img_ind}.jpg') ,'wb') as f:
            f.write(res.content)





def product_info(url,data,product_info_saving_path,each_product_saving_dir):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content,"html.parser")

        product_name = soup.find('h1',class_="-fs20 -pts -pbxs").text
        try:
            product_brand = [x.text.split('|')[0].split(':')[1].strip() for x in soup.find_all('div',class_="-pvxs") if 'Brand' in x.text ][0]
        except:
            product_brand = 0
        product_price = int(soup.find('div',class_="-hr -mtxs -pvs").text.split('₦')[1].replace(',','').strip())
        naira_product_price = '₦'+soup.find('div',class_="-hr -mtxs -pvs").text.split('₦')[1].strip()
        # print(product_name,product_brand,product_price,naira_product_price)


        data['NAME'].append(product_name)
        data['BRAND'].append(product_brand)
        data['PRODUCT_PRICE'].append(product_price)
        data['NAIRA_PRICE'].append(naira_product_price)


        key_features_list = []
        for key_features in range(1,20):
            try:
                info = soup.select("#jm > main > div:nth-child(2) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(1) > div > div > ul > li:nth-child("+str(key_features)+")")
                # print(info[0].text)
                key_features_list.append(info[0].text.replace('\xa0',' '))
            except:
                pass
        if len(key_features_list) < 1:
            info = soup.select("#jm > main > div:nth-child(2) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(1) > div > div")
            for x in info:
                # print(x.text)
                key_features_list.append(x.text.replace('\xa0',' '))
        data['KEY_FEATURES'] = [key_features_list]


        specifications_list = []
        for specifications in range(1,20):
            try:
                info = soup.select("#jm > main > div:nth-child(2) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(2) > div > ul > li:nth-child("+str(specifications)+")")
                if len(info) == 0:
                    info = soup.select("#jm > main > div:nth-child(2) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(3) > div > ul > li:nth-child("+str(specifications)+")")
                # print(info[0].text)
                specifications_list.append(info[0].text.replace('\xa0',' '))
            except:
                pass
        if len(specifications_list) < 1:
            info = soup.select("#jm > main > div:nth-child(2) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(2) > div > ul")
            for x in info:
                # print(x.text)
                specifications_list.append(x.text.replace('\xa0',' '))
        data['SPECIFICATION'] = [specifications_list]


        bag_infos_list = []
        for bag_infos in range(1,20):
            try:
                bag_infos = soup.select('#jm > main > div:nth-child(2) > div.col12 > section.card.aim.-mtm.-fs16 > div.row.-pas > article:nth-child(2) > div > div > ul > li:nth-child('+str(bag_infos)+')')
                # print(bag_infos[0].text)
                bag_infos_list.append(bag_infos[0].text)
            except:
                pass
        if len(bag_infos_list) < 1:
            data['BAG_INFO'] = 0
        else:
            data['BAG_INFO'] = [bag_infos_list]


        seller_infos_list = []
        for seller_infos in range(2,6):
            try:
                seller_info = soup.select('#jm > main > div:nth-child(1) > div.col4 > div > section > div.-pas.-bt.-fs12 > div:nth-child('+str(seller_infos)+')')
                # print(seller_info[0].text)
                seller_infos_list.append(seller_info[0].text.replace('\xa0',' '))
            except:
                pass 
        data['SELLER_INFO'] = [seller_infos_list]


        # --------> [[[ SAVING IMAGES FUNCTION ]]]
        save_product_pic(url=url,pic_saving_dir=each_product_saving_dir)

      
        # all_pic_url = [[ os.path.join(each_product_saving_dir, all_pic_dir).replace(each_product_saving_dir,  'C:\\Users\\USER\\PycharmProjects\\MY MAIN FILES\\Jumia\\Products\\'+ each_product_saving_dir.split('/')[-1]).replace('/','\\')  for all_pic_dir in os.listdir(each_product_saving_dir) if '.jpg' in all_pic_dir]]
        # data['PRODUCT_PIC_URLS'] = all_pic_url

        all_pic_url = [[ os.path.join(each_product_saving_dir, all_pic_dir)  for all_pic_dir in os.listdir(each_product_saving_dir) if '.jpg' in all_pic_dir]]
        data['PRODUCT_PIC_URLS'] = all_pic_url

        # print(data)
        saving_files(data=data,path=product_info_saving_path)
    except Exception as e:
        print(f'\n {e} ::::: ERROR OCCURED \n') 




# def main_func():
#     all_urls_path = pd.read_csv( os.path.join(os.path.dirname(os.path.dirname(__file__)),'All Urls/ALL URL.csv') )
#     for urls_in_path in range(len(all_urls_path)):
#         print(f'\n X CURRENTLY ON {urls_in_path} \n ')
#         product_url = all_urls_path['URLS'][urls_in_path]
#         print(product_url)    

#         data = {'NAME':[],
#                 'BRAND':[],
#                 'PRODUCT_PRICE':[],
#                 'NAIRA_PRICE':[],
#                 'KEY_FEATURES':'',
#                 'SPECIFICATION':'',
#                 'BAG_INFO':'',
#                 'SELLER_INFO':'',
#                 'PRODUCT_PIC_URLS':''}
        

#         each_product_saving_dir = create_each_product_dir(each_product_dir_name= f'product{urls_in_path}_'+all_urls_path['CATEGORY'][urls_in_path] )
        
#         product_info(url=product_url,data=data,each_product_saving_dir=each_product_saving_dir,product_info_saving_path=os.path.join(each_product_saving_dir,product_url.split('/')[3].replace('.html','.csv')  ))

#         print('LENGHT OF ALL LINKS = ',len(all_urls_path))
#         print(f'\n X PREVIOUSLY ON {urls_in_path} \n ')





def main_func_random():
    all_urls_path = pd.read_csv( os.path.join(os.path.dirname(os.path.dirname(__file__)),'All Urls/ALL URL.csv') )
    
    product_url = random.choice(all_urls_path['URLS'])
    print(product_url)    
    data = {'NAME':[],
            'BRAND':[],
            'PRODUCT_PRICE':[],
            'NAIRA_PRICE':[],
            'KEY_FEATURES':'',
            'SPECIFICATION':'',
            'BAG_INFO':'',
            'SELLER_INFO':'',
            'PRODUCT_PIC_URLS':''}
    

    each_product_saving_dir = r'C:\Users\USER\PycharmProjects\MY MAIN FILES\Jumia\CURRENTLY FILE'
    product_info(url=product_url,data=data,each_product_saving_dir=each_product_saving_dir,product_info_saving_path=os.path.join(each_product_saving_dir,product_url.split('/')[3].replace('.html','.csv')  ))
