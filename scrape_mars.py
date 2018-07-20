import time
from splinter import Browser
import selenium
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# Define functions for application
def scrape():
    title, text = scrape_news()
    featured_image_url = scrape_photo()
    mars_weather = scrape_weather()
    html_table = scrape_fact_table()
    img_url_list = scrape_hemi_photos()
    results = {}
    results['weather'] = mars_weather
    results['news_title'] = title
    results['news_text'] = text
    results['html_table'] = html_table
    results['img_url_list'] = img_url_list
    results['featured_img_url'] = featured_image_url
    return results

def init_browser():
    # this code requires chromedriver to be present in the same directory
    # as the notebook or python script file
    # NOTE IF YOU ARE RUNNING WINDOWS YOU MUST UNCOMMENT THE LINE BELOW
    # AND ENSURE CHROMEDRIVER.EXE IS IN THE SAME DIRECTORY AS THIS FILE
    #executable_path = {"executable_path": "./chromedriver.exe"}
    # , **executable_path
    return Browser("chrome", headless=True)

def scrape_news():
    '''scrape_news is a function that uses splinter to access a
    NASA url for mars news, it then uses BS4 to scrape the html
    and parses it to find the most recent article title and teaser
    text. The relevant strings are further extracted from the HTML
    and these variables, title and text, are returned as a tuple'''

    # Initialize browser
    browser = init_browser()    

    # Set URL to NASA's Mars News Page
    # use splinter browser to navigate headless
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # Wait for the redirect on the page to occur before pulling HTML
    time.sleep(2)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Use soup.find to find instances of div's containing
    # the top story's (first result) title and teaser text
    try:
        title = (soup.find('div',class_='content_title')).text
    except AttributeError:
        print("An AttributeError occurred looking for the title")
        scrape_news()
    try:
        text = (soup.find('div',class_='article_teaser_body')).text
    except AttributeError:
        print("An AttributeError occurred looking for the teaser text")
        scrape_news()
    
    # Return results
    return title,text

def scrape_photo():
    '''scrape_photo is a function that utilizes splinter to access the page
    https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars and click on the'''

    # Initialize browser
    browser = init_browser()

    # Use the browser to retrieve html
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    # Use BS4 to extract the featured image URL from the Mars page
    soup = BeautifulSoup(html, 'html.parser')
    full_image = soup.find_all("li",class_="slide")
    featured_image_url = full_image[0].find('a').get("data-fancybox-href")
    # Concat relative URL into absolute URL
    featured_image_url = "https://www.jpl.nasa.gov"+featured_image_url

    # Return URL
    return featured_image_url

def scrape_weather():
    '''scrape_weather is a function that utilizes splinter to acess the curiosity
    rover climate twitter page that tweets a once per day weather summary. This function
    will return the latest weather tweet (whatever it is!) as a string mars_weather'''
    # Initialize browser
    browser = init_browser()
    # Use the browser to retrieve html
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    # Use BS4 to extract the latest weather tweet
    soup = BeautifulSoup(html,'html.parser')
    tweets = soup.find_all("div",class_="tweet")
    for tweet in tweets:
        userid = tweet.find('a').get("data-user-id")
        if userid == "786939553":
            mars_weather = tweet.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
            mars_weather = mars_weather.text
            _first3 = mars_weather[:3]
            if _first3 != 'Sol':
                next
            else:
                break
        else:
            next
    return mars_weather

def scrape_fact_table():
    '''scrape_fact_table is a very simple python script with no inputs that uses pandas
    built in HTML table reader to import from http://space-facts.com/mars/ a table of data
    about the red planet. It will then reform the table into HTML code and return it for
    deployment to a website'''
    list_of_df = pd.read_html(io='http://space-facts.com/mars/',flavor="bs4",header=None,attrs={'id':'tablepress-mars'})
    df = list_of_df[0]
    df = df.rename(columns={0:'Property',1:'Value'})
    html_table = df.to_html(index=False)
    return html_table

def scrape_hemi_photos():
    '''scrape_hemi_photos is an inputless function that navigates using Splinter to the USGS website
    of Martian hemispheres. It will use partial link text matches to click to each hemispheres page
    record the name of the hemisphere and a link to a full-size image of the hemisphere. It stores these
    values in a list of dictionaries with keys: title and img_url and returns that list'''
    hemisphere_image_urls = []
    # Initialize browser
    browser = init_browser()
    # Use the browser to navigate the page
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    # Use click_link_by_partial_text to target the first hemisphere
    browser.click_link_by_partial_text('Cerberus Hemisphere')
    # Retrieve page HTML
    html = browser.html
    # Parse HTML with BS4
    soup = BeautifulSoup(html,'html.parser')
    # Extract hemisphere title and full size image URL
    title = soup.find('h2',class_="title").text
    img_url = soup.find('a',target="_blank").get('href')
    # Append dictionary into list
    hemisphere_image_urls.append({'title':title,'img_url':img_url})
    # Use the back button to navigate back to the main page
    browser.click_link_by_partial_text('Back')
    # Rinse and repeat for the next 3 hemispheres
    browser.click_link_by_partial_text('Schiaparelli Hemisphere')
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find('h2',class_="title").text
    img_url = soup.find('a',target="_blank").get('href')
    hemisphere_image_urls.append({'title':title,'img_url':img_url})
    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Syrtis Major Hemisphere')
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find('h2',class_="title").text
    img_url = soup.find('a',target="_blank").get('href')
    hemisphere_image_urls.append({'title':title,'img_url':img_url})
    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Valles Marineris Hemisphere')
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find('h2',class_="title").text
    img_url = soup.find('a',target="_blank").get('href')
    hemisphere_image_urls.append({'title':title,'img_url':img_url})
    return hemisphere_image_urls

    if __name__ == "__main__":
        scrape()