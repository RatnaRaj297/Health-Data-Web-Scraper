from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup as soup
import requests
import time
import csv


filename = "final.csv"
links = []
names = []

binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
my_urrl="https://my.clevelandclinic.org/health/drugs?letter="

#Creating 26 alphabets for 26 different links
alphabets=[]
for i in range(26):
    alphabets.append(chr(i+65))

driver = webdriver.Firefox(firefox_binary=binary)

for alphabet in alphabets:
    url = my_urrl+alphabet

    driver.get(url)
    time.sleep(6)

    html = driver.execute_script("return document.documentElement.outerHTML")

    sel_soup = soup(html,'html.parser')


    #column 1
    for i in range(3):
        x=str(int(i)+1)
        containers = sel_soup.findAll("div",{"class":"l-3col--"+x})
        y=(len(containers))
        if y==1:
            for container in containers:
                linkez= container.findAll("a",{"class" : "index-list-link"})
            for link in linkez:
                names.append(link.text)
                links.append(link['href'])

with open("final.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Medicine name" , "URL" , "Medicine Description?" , "Common Brand Name(s)" , "Things one should tell thier health care provider before they take this medicine" , "How should one use this medicine" , "What if one miss a dose?" , "What may interact with this medicine?" , "What should one watch for while using this medicine" , "What side effects may one notice from receiving this medicine?" , "Where should I keep my medicine?"])

    for i in range(len(links)):

        my_url=links[i]
        page_html=requests.get(my_url).text

        page_soup=soup(page_html,"html.parser")

        try:
            containers = page_soup.findAll("div",{"class": "l-66-33--1 main-content"})

            container = containers[0]
            ans = container.text        
       
       # medicine_name     What is this medicine?
        # brand_name        COMMON BRAND NAME(S):
        # medicine_take     What should I tell my health care provider before I take this medicine?
        # medicine_use      How should I use this medicine?
        # miss_dose         What if I miss a dose?
        # medicine_interact What may interact with this medicine?
        # medicine_watch    What should I watch for while using this medicine?
        # medicine_effect   What side effects may I notice from receiving this medicine?
        # medicine_keep     Where should I keep my medicine?
        
            temp = ans.split("What is this medicine?")
            temp = temp[1]
            temp2 = temp.split("COMMON BRAND NAME(S):")
            medicine_name = temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("What should I tell my health care provider before I take this medicine?")
            brand_name = temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("How should I use this medicine?")
            medicine_take = temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("What if I miss a dose?")
            medicine_use=temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("What may interact with this medicine?")
            miss_dose=temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("What should I watch for while using this medicine?")
            medicine_interact=temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("What side effects may I notice from receiving this medicine?")
            medicine_watch=temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("Where should I keep my medicine?")
            medicine_effect=temp2[0].strip()
            temp = temp2[1]
            temp2 = temp.split("NOTE: This sheet is a summary.")
            medicine_keep=temp2[0].strip()

            # A bit of formatting
            medicine_name = (medicine_name.replace(',',';')).strip()
            brand_name = (brand_name.replace(',',';')).strip()
            medicine_take=(medicine_take.replace(',',';')).strip()
            medicine_use=(medicine_use.replace(',',';')).strip()
            miss_dose=(miss_dose.replace(',',';')).strip()
            medicine_interact=(medicine_interact.replace(',',';')).strip()
            medicine_watch=(medicine_watch.replace(',',';')).strip()
            medicine_effect=(medicine_effect.replace(',',';')).strip()
            medicine_keep = (medicine_keep.replace(',',';')).strip()

            writer.writerow([names[i],links[i],medicine_name,brand_name,medicine_take,medicine_use,miss_dose,medicine_interact,medicine_watch,medicine_effect,medicine_keep])
        except:
            print('Invalid URL Found')
