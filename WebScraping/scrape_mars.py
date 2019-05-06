# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from time import sleep
import pandas as pd
import os


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_data = {}

    #--------------------------------------------------------------
    # NASA News Scrape
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2019%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the parent divs for all articles
    result = soup.find(class_='slide')
    news_title = result.find(class_='content_title').text
    news_p = result.find(class_='article_teaser_body').text

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    browser.quit()


    #--------------------------------------------------------------
    # JPL Mars Space Images - Featured Image
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #base url for later use
    url_base = 'https://www.jpl.nasa.gov'

    browser.click_link_by_id('full_image')
    sleep(20)
    browser.click_link_by_partial_text('more info')

    # scrape page into Soup
    image_page = browser.html
    mars_image_soup = BeautifulSoup(image_page,"html.parser")
    mars_image_soup
    # find the image in soup
    search_image = mars_image_soup.find(class_="main_image")

    featured_image_url = url_base + search_image["src"]
    print(featured_image_url)

    mars_data["featured_image_url"] = featured_image_url

    browser.quit()


    #--------------------------------------------------------------
    # Mars Weather

    # create a browser instance
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Soupify webpage
    html_weather_twitter = browser.html
    soup = BeautifulSoup(html_weather_twitter,"html.parser")

    # Find today's Mars weather
    mars_weather = soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)

    mars_data["mars_weather"] = mars_weather

    browser.quit()


    #--------------------------------------------------------------
    # Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    table = pd.read_html(mars_facts_url)
    df = table[0]

    # Assign the columns
    df.columns = ['Parameters','Values']

    # Set the index to the `Parameters`
    df.set_index('Parameters', inplace=True)

    # Save html code 
    fact = df.to_html()

    # Dictionary entry from MARS FACTS
    mars_data['table'] = fact


    #--------------------------------------------------------------
    # Mars Hemispheres

    # create a browser instance
    browser = init_browser()

    # url to be scraped
    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Create list to hold images
    Hemispheres=['Cerberus','Schiaparelli','Syrtis','Valles']
    image_list = []

    # get image url for each hemisphere
    for Hemi in Hemispheres:
        browser.visit(url)
        browser.click_link_by_partial_text(Hemi)
        soup = BeautifulSoup(browser.html, 'html.parser')
        image_url=soup.find('a',text='Sample')['href']
        image_list.append(image_url)

    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "image_url": image_list[0]},
        {"title": "Schiaparelli Hemisphere", "image_url": image_list[1]},
        {"title": "Syrtis Major Hemisphere", "image_url": image_list[2]},
        {"title": "Valles Marineris Hemisphere", "image_url": image_list[3]}
    ]

    mars_data["mars_hemisphere"]=image_list

    browser.quit()

    return mars_data
