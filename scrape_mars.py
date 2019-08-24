#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# In[1]:


#Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
#dependencies
from urllib.parse import urlsplit
#dependencies
import pandas as pd

def scrape_info():

    ##### Windows Users

    # In[2]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # #### URL1 | NASA Mars News

    # In[3]:


    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url1)
    #print(browser.html)


    # In[4]:


    html1 = browser.html
    soup = BeautifulSoup(html1, 'html.parser')
    #print(soup.prettify())


    # In[5]:



    results = soup.find('ul', class_='item_list')
    #print(news_title)
    news_titles=results.find_all('div',class_='content_title')
    #print(news_titles[0].a.getText())
    news_title=news_titles[0].a.getText()
    #print(news_title)


    # In[6]:


    news_ps=results.find_all('div',class_='article_teaser_body')
    #print(news_ps[0].getText())
    news_p=news_ps[0].getText()
    #print(news_p)


    # #### URL2 | JPL Mars Space Images - Featured Image

    # In[7]:


    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    #print(browser.html)


    # In[8]:


    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    #print(soup2.prettify())


    # In[9]:


    results2 = soup2.find('a', class_='button fancybox')
    #print(results2)

   # print(results2.attrs['data-fancybox-href'])
    featured_image_url = 'https://www.jpl.nasa.gov' + results2.attrs['data-fancybox-href']
    #print(featured_image_url)


    # #### URL3 | Mars Weather

    # In[10]:


    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    #print(browser.html)


    # In[11]:



    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    #print(soup3.prettify())


    # In[12]:


    results3 = soup3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(results3)

    #Split the tweet if it has text and image url to just retrieve the text
    try:
        mars_weather = results3.split('pic.twitter.com/')[0]
    except:
        mars_weather=results3
   # print(mars_weather)


    # ####  URL4 | Mars Facts

    # In[13]:





    # In[14]:


    url4 = 'https://space-facts.com/mars/'


    # In[15]:


    tables = pd.read_html(url4)


    df = tables[1]
    df = df.rename({0:'Description' , 1: 'value'}, axis='columns')

    df_mars_facts = df.set_index(["Description"])
    df_mars_facts


    # In[16]:


    #generate HTML tables from DataFrames

    html_table = df_mars_facts.to_html()
    html_table


    # In[17]:


    html_table.replace('\n', '')


    # In[18]:


    #df.to_html('table.html')


    # #### URL 5 | Mars Hemispheres

    # In[19]:


    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    #print(browser.html)


    # In[20]:





    # In[21]:


    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url5))
    #print(base_url)


    # In[22]:


    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')
    #print(soup2.prettify())


    # In[23]:


    results5 = soup5.find_all('div', class_='item')
    results5


    # In[24]:


    #List of dictionaries to hold title & url of the hemispheres
    hemisphere_image_urls = []


    # In[25]:


    for result in results5:
        title =result.find('h3').text
        
        hemisphere_url = result.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(base_url + hemisphere_url)
        
        # HTML Object of individual hemisphere information website 
        hemisphere_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup_hemisphere = BeautifulSoup( hemisphere_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = base_url + soup_hemisphere.find('img', class_='wide-image')['src']
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        


    # In[26]:


    #print(hemisphere_image_urls)

    #Final Dictionary with all scraped data
    scrape_dict = {
        'MarsNews': {'news_title': news_title,
                'news_p': news_p},
        'FeaturedImage': featured_image_url,
        'MarsWeather' : mars_weather,
        'MarsFacts' : html_table,
        'MarsHemispheres' : hemisphere_image_urls
            
    }
    browser.quit()
    return scrape_dict

    # In[ ]:

#print("Mission to Mars -> insid")
#scrape_result_combined=scrape()
#print(scrape_result_combined)

