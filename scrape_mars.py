from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDiverManager
import pandas as pd
import time

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # Store the Mars data in mars_data 
    mars_data = {}
    
    # -- Mars News --
    # Visit the page URL
    mars_news_url = 'https://redplanetscience.com/'
    browser.visit(mars_news_url)
    time.sleep(3)

    # Create an HTML object
    html = browser.html

    # Parse the HTML with BeautifulSoup
    mars_soup = bs(html, 'html.parser')

    # Extract the news title
    mars_title = mars_soup.find('div', class_='content_title').text.strip()
    mars_data['mars_title'] = mars_title

    # Extract the paragraph text
    mars_para = mars_soup.find('div', class_='article_teaser_body').text.strip()
    mars_data['mars_para'] = mars_para


    # -- Featured Image --
    # Visit the page URL
    mars_pic_url = 'https://spaceimages-mars.com/'
    browser.visit(mars_pic_url)
    time.sleep(3)

    # Create an HTML object
    html = browser.html

    # Parse the HTML with BeautifulSoup
    mars_soup = bs(html, 'html.parser')

    # Grab the featured image's URL
    featured_image_url = mars_soup.find('img', class_='headerimage fade-in').get("src")

    # Combine the base URL with the featured image URL to get the full URL
    full_image_url = mars_pic_url + featured_image_url
    mars_data['full_image_url'] = full_image_url


    # -- Mars Facts --
    # Go to the facts page URL
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    time.sleep(3)

    # Read the table and pull the data
    mars_table_url = pd.read_html(mars_facts_url)

    # Create Mars Facts dataframe
    mars_table_df = mars_table_url[0]

    # Rename columns to first row data
    mars_table_df = mars_table_df.rename(columns=mars_table_df.iloc[0])

    # Drop first row data
    mars_table_df = mars_table_df.drop([0])

    # Set index of the table
    mars_table_df = mars_table_df.set_index('Mars - Earth Comparison')

    # Remove the index name
    mars_table_df.index.name = None

    # Convert to HTML table
    html_table = mars_table_df.to_html()
    mars_data['html_table'] = html_table


    # -- Mars Hemispheres --
    # Visit the page URL
    hemis_url = "https://marshemispheres.com/"
    browser.visit(hemis_url)
    time.sleep(3)

    # Create an HTML object and parse it with BeautifulSoup
    html = browser.html
    mars_soup = bs(html, 'html.parser')

    #parse the landing page, isolate the image links in the item div
    hemi_links = mars_soup.find_all("div", class_ = "item")

    #create a list for the names and image links
    hemispheres = []

    #loop thru each link and grab the name and full size image
    for link in hemi_links:
        #dictionary to hold the name/link pairs
        hemi_dict = {}
        img_link = link.find("img", class_ = "thumb").get("src")
        #add the base url
        base_url = "https://marshemispheres.com/"
        visit_link = base_url + img_link
    
        #add to dictionary as hemi_img_name, hemi_img_url
        hemi_dict['hemi_img_name'] = img_name
        hemi_dict['hemi_img_url'] = base_url + img_link
        hemi_dict['hemi_source_url'] = visit_link
        #put dictionary into hemi_img_urls
        hemispheres.append(hemi_dict)
        browser.back()
    mars_data['hemispheres'] = hemispheres

    browser.quit()

    return mars_data

    