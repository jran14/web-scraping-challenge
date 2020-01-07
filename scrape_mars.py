from bs4 import BeautifulSoup as bs
import requests
from json import dumps
from splinter import Browser
import time
import pandas as pd

def init_browser():
    exec_path={'executable_path':'C:/Users/jenni/web-scraping-challenge/chromedriver.exe'}
    return Browser('chrome', **exec_path, headless=True)

def scrape():
    browser = init_browser()

    #scrape all data and return information in a mars_data dictionary
    mars_data={}

    #ACTIVITY 1: Collect the latest News Title and Paragraph Text
    nasa_url= 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    #save title as news_title
    time.sleep(2)
    news = bs(browser.html, 'html.parser')
    news_find=news.select_one('ul.item_list li.slide') #first match 
    print(news_find)
    news_title =news_find.find("div",class_="content_title")

    mars_data["news_title"] =news_title.get_text()

    #save description as news_p
    news_p= news_find.find("div",class_='rollover_description_inner')

    mars_data["news_p"] =news_p.get_text()

    # ACTIVITY 2: Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    jpl_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = Browser('chrome', headless=True)
    browser.visit(jpl_url)
    jpl = bs(browser.html, 'html.parser')
    jpl_find =jpl.find("div",class_="carousel_items")
    featured_image_url = jpl_find.a['data-fancybox-href']
    featured_image_url='https://www.jpl.nasa.gov'+featured_image_url 

    mars_data["featured_image_url"] =featured_image_url

    # ACTIVITY 3: Scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
    twitter_url= 'https://twitter.com/marswxreport?lang=en'
    response_twitter= requests.get(twitter_url)
    soup_twitter = bs(response_twitter.text, 'lxml')
   
    #latest tweet
    tweet = soup_twitter.find('div', class_='js-tweet-text-container').\
        find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    mars_data["latest_tweet"] = tweet.text.lstrip()

    # ACTIVITY 4: Scrape the table containing facts. Convert the data to a HTML table string.
    space_url= 'https://space-facts.com/mars/'
    response_space= requests.get(space_url)
    soup_space = bs(response_space.text, 'html.parser')
    #table scrape
    # mars_facts = soup_space.find('div', class_='site-content container clearfix').\
    #     find('section',class_='sidebar widget-area clearfix').\
    #     find('div',class_='textwidget').\
    #     find('table')
    browser.visit(space_url)
    mars_data = pd.read_html(space_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts


    mars_data["mars_facts"] = mars_facts

    #click each of the links to the hemispheres in order to find the image url to the full resolution image
    astro_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser('chrome', headless=True)
    browser.visit(astro_url)
    astro = bs(browser.html, 'html.parser')

    hemisphere_images=[]
    
    search= astro.find('div', class_='result-list')
    hemispheres= search.find_all('div',class_='item')

    for hemisphere in hemispheres:
        title= hemisphere.find('h3').get_text()
        img_find= hemisphere.find('a')['href'] 
        img_link= 'https://astrogeology.usgs.gov/'+img_find
        browser.visit(img_link)
        html= browser.html
        soup= bs(html, 'html.parser')
        download= soup.find('div', class_='downloads')
        img_url= download.find('a')['href']
        hemisphere_images.append({'Title': title, 'url': img_url})
    mars_data['hemisphere_images']=hemisphere_images


    return mars_data


if __name__ == '__main__':
    mars_data= scrape()
    print("The url for the image is")
    print(mars_data['mars_facts'])