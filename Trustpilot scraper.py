import pandas as pd
import time
from bs4  import BeautifulSoup
from selenium import webdriver
#Automatic installation of chrome driver
from webdriver_manager.chrome import ChromeDriverManager

#%%

#Define which website you want to scrape and then press play!
website_to_scrape = 'www.shiply.com'

#%%

#Start browser 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

#Set browser
browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

#initialise data frame
df = pd.DataFrame(columns=[
    'target_website'
    ,'link'
    ,'page_num'
    ,'name'
    ,'date'    
    ,'invited_flag'
    ,'title'
    ,'review'
    ,"stars"
    ])

url='https://uk.trustpilot.com/review/'+website_to_scrape+'?page=1'  
browser.get(url)
page_num = browser.find_element_by_css_selector("a[name='pagination-button-last']").text

for page in range(1,page_num): 
    

    url='https://uk.trustpilot.com/review/'+website_to_scrape+'?page=' + str(page)
    
    browser.get(url)
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    results = soup.find_all("div",class_="paper_paper__29o4A paper_square__XVMAC card_card__2F_07 card_noPadding__1tkWv styles_cardWrapper__2fU-g styles_show__NvJab styles_reviewCard__1LyWJ")
    if len(results) > 0:
        for review in results:
                           
            try:
                name = review.find("div", class_ ='typography_typography__23IQz typography_bodysmall__24hZa typography_weight-medium__34H_5 typography_fontstyle-normal__1_HQI styles_consumerName__1Lm3h').text
            except:
                name = 'None'
                    
            try:
                date = review.time['datetime']
            except:
                date = 'None'
                
            try:
                invited = review.find("div", class_ ='typography_typography__23IQz typography_bodysmall__24hZa typography_color-gray-6__11VpO typography_weight-regular__iZYoT typography_fontstyle-normal__1_HQI styles_detailsIcon__1xfzl').text
            except:
                invited = 'None'
            
            try:
                title = review.find("h2", class_ ='typography_typography__23IQz typography_h4__IhMYK typography_color-black__1uBz2 typography_weight-regular__iZYoT typography_fontstyle-normal__1_HQI styles_reviewTitle__8VDr1').text
            except:
                title = 'None'
            
            try:
                review_text = review.find("p", class_ ='typography_typography__23IQz typography_body__2OHdw typography_color-black__1uBz2 typography_weight-regular__iZYoT typography_fontstyle-normal__1_HQI').text
            except:
                review_text = 'None'
            
            try:
                stars = review.find_all('img')[-1]['alt']
            except:
                stars = 'None'
        
           
            df = df.append({'target_website':website_to_scrape,
                            "link":url,
                            "page_num":page,
                            "name":name,
                             "date":date, 
                             "invited_flag": invited,
                             "title": title,
                             "review": review_text,
                             "stars":stars
                            }
                           , ignore_index=True) 
            print(df)    
    else : 

        input("check browser is still running")


#Export to CSV
df.to_csv('trustpilot_scraper_export_full.csv')
               