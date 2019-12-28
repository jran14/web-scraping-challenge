from bs4 import BeautifulSoup as bs
import os
import requests
from json import dumps
from splinter import Browser

# ACTIVITY 1: Collect the latest News Title and Paragraph Text
nasa_url= 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
response= requests.get(nasa_url)
soup = bs(response.text, 'lxml')

# news_items = soup.find_all('div', class_='list_text')
# news_items_lst = [{'title':news.find('div', class_='content_title').text,
#                     'Description':news.find('div', class_='article_teaser_body')} for news in news_items]


news_items_lst= []
# for news in news_items:
#     news_title= news.find('a').text
#     news_p= news.find('div', class_='article_teaser_body').text
#     news_dict= {'Title':news_title,
#                 'Description':news_p}
#     news_items_lst.append(news_dict)

news_items = soup.find_all('ul', class_='item_list')
for news in news_items:
    news_title= news.find('div', class_='image_and_description_container').find('a')
    if news_title:
        news_title_text= news_title.text.strip()
    else:
        news_title_text= ' '
    news_p= news.find('div', class_='rollover_description_inner')
    if news_p:
        news_p_text= news_p.text.strip()
    else:
        news_p_text= ' '
    news_dict= {'Title':news_title_text,
                'Description':news_p_text}
    news_items_lst.append(news_dict)


    print(news_items.prettify())



# print(news_items_lst)



# ACTIVITY 2: Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
jpl_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser = Browser('chrome', headless=True)
browser.visit(jpl_url)
 # Find and click the 'full image' feature image button 
button = browser.find_by_name('FULL IMAGE')
button.click()
featured_image_url=soup.find('div', class_='carousel_items').find('article', style='background-image')
print(featured_image_url.text.strip())




# ACTIVITY 3: Scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather
# https://twitter.com/marswxreport?lang=en

# ACTIVITY 4: Scrape the table containing facts. Convert the data to a HTML table string.
# https://space-facts.com/mars/

# ACTIVITY 5: Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

# ACTIVITY 6: