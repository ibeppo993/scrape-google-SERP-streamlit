import streamlit as st
st.set_page_config(
    page_title="Scrape Google SERP",
    layout="wide",
    initial_sidebar_state="expanded",
)

import requests, urllib, bs4, selenium, datetime, re, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from parserp import organic_results
from parserp import related_searches
from parserp import paa_results




def main():
    #casa = 'casa'
    #casa1 = 'casa1'
    user_input = st.sidebar.text_input("Keyword", '')
    'Keyword: ',user_input

    nazioni = ['Italia','Regno Unito','Francia','Spagna','Germania','Olanda']
    result_for_page_df = pd.DataFrame(nazioni)  
    streamlit_option = st.sidebar.selectbox('Nazione?', result_for_page_df)
    'Nazione: ', streamlit_option

    if user_input:

        # result_for_page = [10,20,30,40,50,100]
        # result_for_page_df = pd.DataFrame(result_for_page)  
        # streamlit_option = st.sidebar.selectbox('Quanti risultati?', result_for_page_df)
        # 'You selected:', streamlit_option



        #creazione e apertura browsers
        option = webdriver.ChromeOptions()
        #Heroku 
        option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        
        
        #Removes navigator.webdriver flag
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument('--disable-blink-features=AutomationControlled')
        #Proxy
        #option.add_argument(f'proxy-server={proxy}')
        #headless
        option.add_argument("--headless")
        #incognito
        option.add_argument('--incognito')
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--no-sandbox")
        #creazione e apertura browsers
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=option)

        #driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
        #driver = webdriver.Chrome('./chromedriver',options=option)
        driver.maximize_window()

        #Singola Keyword
        #keyword_old = 'scarpe nere adidas uomo'
        keyword_old = user_input
        domain = 'https://www.google.it/search?q='
        keyword = keyword_old
        keyword = urllib.parse.quote_plus(keyword)
        hl = 'hl=IT'
        gl= 'gl=it'
        tci = 'tci=g:2380'
        uule = 'uule=w+CAIQICIFSXRhbHk'
        driver.get(f'{domain}{keyword}&{hl}&{gl}&{tci}&{uule}&sourceid=chrome&ie=UTF-8')
        soup = BeautifulSoup(driver.page_source,'html.parser')

        st.title('risultati organici')
        data_organico = organic_results.get_organic_results(soup)
        data_organico
        st.title('ricerche correlate')
        data_correlata = related_searches.get_related_searches(soup)
        data_correlata
        st.title('ricerche correlate')
        data_paa = paa_results.get_paa_results(soup)
        data_paa


        # S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        # driver.set_window_size(S('Width'), S('Height'))
        # driver.find_element_by_tag_name('body').screenshot('serp_screen.png')
        # display(Image(f'{dt_string}_{keyword}_screen.png'))


if __name__ == "__main__":
    main()
