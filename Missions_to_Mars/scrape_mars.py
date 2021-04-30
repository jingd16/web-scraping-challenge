# import necessary libraries
from flask import Flask, render_template
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time

def scrape():

    #==========================================NASA Mars News==================================================
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(10)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.find('ul', class_='item_list')

    #********Result to put into Dictionary: title1 & para
    nasa_title=soup.find('ul', class_='item_list').find("li").find('div', class_='content_title').find('a').text
    para=soup.find('ul', class_='item_list').find("li").find('div', class_='article_teaser_body').text

    browser.quit()

    #=================================JPL Mars Space Images - Featured Image=====================================
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    time.sleep(10)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(10)


    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')

    img = soup.find("div", class_="fancybox-wrap fancybox-desktop fancybox-type-image fancybox-opened").find('img', class_="fancybox-image")["src"]

    url_1= url.split("index.html")[0]
    
    #********Result to put into Dictionary: img_url
    img_url = url_1 + img

    browser.quit()

    #=====================================================Mars Facts Table=============================

    #Broswer to open the website
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(10)
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    mars_df = tables[0]
    mars_df.columns = ["Mars Details","Measurements"]

    #=========Result to put into dictionary: html_table
    html_table = mars_df.to_html()
    html_table.replace("\n", "")

    browser.quit()

    #================================ Mars Hemispheres=========================================
    #Broswer to open the website
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html_mars_main = browser.html
    soup = BeautifulSoup(html_mars_main, 'html.parser')
    all_div=soup.find_all("div", class_="description")

    #Create a list for the headlines and append them.
    title=[]
    for x in all_div:
        title.append(x.find("h3").text)

    url_2= url.split("/search")[0]
    url_2

    #Loop throught the headline list and visit each link to get url details
    img_url=[]
    for x in title:
        browser.links.find_by_partial_text(x).click()
        html_mars = browser.html
        soup = BeautifulSoup(html_mars, 'html.parser')
        img_url1 = soup.find("img", class_="wide-image")["src"]
    
        #combine 2 variables to get the right img_url
        #=====================Result to add to dictionary: img_url (list)
        img_url.append(url_2 + img_url1)
    
        #ask the browser to go back to the main page
        browser.back()

    #add title and img_url to a list of dictionary
    hemisphere_image_urls=[]
    for x in range(0,3):
        hemisphere_image_urls.append({"title": title[x], "img_url": img_url[x]})

    browser.quit()

    
    listings={}
    listings["Nasa_News_Title"] = nasa_title
    listings["Nasa_News_Para"] = para
    listings["Featured_Image"] = img_url
    listings["Mars_Information"]=html_table
    listings["Mars_Img_Url"]=hemisphere_image_urls

    return listings
    

    
    

