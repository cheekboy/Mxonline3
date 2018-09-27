from django.db import connection
import os
import sys
import subprocess
import redis
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import datetime
# import win32gui
import os
from PIL import Image
from selenium.webdriver.support.ui import Select
# import win32con
import time, platform, sys, getopt, paramiko, random, re


def save_image(chrome,element,save_path):

    location = element.location_once_scrolled_into_view
    size = element.size
    chrome.save_screenshot(save_path)


    image = Image.open(save_path)
    left = location ['x']
    top=location['y']
    right = location ['x'] + size ['width']
    bottom = location ['y'] + size ['height']
    image = image.crop((left,top,right,bottom))#，右，下））＃定义裁剪点
    image.save(save_path,'png')

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("select name,pid,id from organization_p8logo where id >23016")
        row = cursor.fetchall()

    return row
if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    e = webdriver.Chrome(chrome_options=chrome_options)
    e.implicitly_wait(10)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mxonline3.settings")
    results=my_custom_sql()
    for row in results:
        name = row[0]
        pid = row[1]
        id = row[2]
        e.get("https://www.google.com.hk/search?newwindow=1&safe=strict&biw=1440&bih=698&tbm=isch&sa=1&ei=3-CpW8CBOYGD8wWKkpjoCg&q="+name +" logo&oq=%E6%B5%99%E6%B1%9F%E7%AC%AC%E4%BA%8C%E5%8C%BB%E9%99%A2+logo&gs_l=img.3...10860.12024.0.12430.5.5.0.0.0.0.109.480.3j2.5.0....0...1c.1j4.64.img..0.1.94...0i12i24k1.0.zICcQBKHp_8)")
        print ("fname=%s,lname=%s,id=%s" % \
         (name, pid,id))
        a=e.find_element_by_xpath("//*[@id='rg_s']/div[1]/a/img")
        save_image(e,a,"/Volumes/disk0s3/1/"+pid+".png")
        a=e.find_element_by_xpath("//*[@id='rg_s']/div[2]/a/img")
        save_image(e,a,"/Volumes/disk0s3/2/"+pid+".png")
        a=e.find_element_by_xpath("//*[@id='rg_s']/div[3]/a/img")
        save_image(e,a,"/Volumes/disk0s3/3/"+pid+".png")
        a=e.find_element_by_xpath("//*[@id='rg_s']/div[4]/a/img")
        save_image(e,a,"/Volumes/disk0s3/4/"+pid+".png")

# import socks
# import socket
# import requests

# back=socket.socket
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",1080)
# print(requests.get('http://ifconfig.me/ip').text)

def l(url):
    global index1
    index1 = index1 + 1
    e.get(url)
    for index in range(40):
        index = index + 1
        try:
            e.find_element_by_xpath("//*[@id='main-layout-sidebar']/div/div[1]/ol/li[" + str(index) + "]").click()

            page = e.page_source
            filename = 'c:\\setup.log'
            f = open("c://qianduan//" + str(index1) + "_" + str(index) + ".htm", mode="w", encoding="UTF-8")
            f.write(page)
            f.close()
        except:
            break


# //*[@id="main-layout-content"]/div/div[1]/div/div/ol/li[13]/div[2]/h2/a
# //*[@id="main-layout-content"]/div/div[1]/div/div/ol/li[1]/div[2]/h2/a
# //*[@id="main-layout-content"]/div/div[1]/div/div/ol/li[9]/div[2]/h2/a
# //*[@id="main-layout-content"]/div/div[1]/div/div/ol/li[1]/div[2]/h2/a
# https://classroom.udacity.com/nanodegrees/nd001/parts/00113454015
def o(url):
    e.get(url)
    time.sleep(10)
    print(url)
    for index in range(10):
        index = index + 1
        try:
            e.find_element_by_xpath(
                "//*[@id='main-layout-content']/div/div[1]/div/div/ol/li[" + str(index) + "]/div[2]/h2/a").click()
        except:
            break
    for index in range(10):
        index = index + 1
        try:
            l(href[index])
        except:
            break


def login(root, passwd):
    url1 = "https://auth.udacity.com/sign-in?next=https%3A%2F%2Fclassroom.udacity.com%2Fauthenticated"
    e.get(url1)
    e.find_element_by_xpath(
        '//*[@id="app"]/div/div[2]/div/div/div/div[2]/div/div[1]/div/form/div/div[1]/input').send_keys(root)
    e.find_element_by_xpath(
        '//*[@id="app"]/div/div[2]/div/div/div/div[2]/div/div[1]/div/form/div/div[2]/input').send_keys(passwd)
    e.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div[2]/div/div[1]/div/form/button').click()


#	e.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div/div/div[2]/div/div/form/div/div[1]/input").send_keys(root)
#	e.find_element_by_css_selector("#app > div > div.main-container--content--1CGTM > div > div > div > div.tabbed-pane--content--2o3OQ > div > div > form > div > div:nth-child(2) > input").send_keys(passwd)
#	e.find_element_by_css_selector("#app > div > div.main-container--content--1CGTM > div > div > div > div.tabbed-pane--content--2o3OQ > div > div > form > button").click()
