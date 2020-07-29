from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import re

def get_movies_urls():
    in_loop = True
    browse_movies_url = 'https://www.rottentomatoes.com/browse/dvd-streaming-all/'
    movies = {}
    url_pattern = re.compile(r'href\s*=\"/m/\w*\"')
    name_pattern = re.compile('<h3 class=\"movieTitle\">.*</h3>')
    driver = webdriver.Firefox()
    driver.get(browse_movies_url)
    #soup = BeautifulSoup(driver.page_source,"html.parser")
    while(in_loop == True):
        elements = driver.find_elements_by_class_name('mb-movie')
        for e in elements:
            attrib = e.get_attribute('outerHTML')
            name = re.findall(name_pattern, str(attrib))
            url = re.findall(url_pattern, str(attrib))
            if (len(name) > 0) and (len(url) > 0):
                for i in range (0, len(name)):
                    name[i] = re.sub('<h3 class=\"movieTitle\">', '',name[i])
                    name[i] = re.sub('</h3>', '',name[i])
                    url[i] = re.sub('href=\"','', url[i])
                    url[i] = re.sub('\"','', url[i])
                    movies[name[i]] = url[i]
        try:
            button = driver.find_element_by_css_selector('.btn.btn-secondary-rt.mb-load-btn')
            button.click()
            print("Cliquei!")
        except NoSuchElementException:
            print("NAO Cliquei!")
            in_loop = False
            break
    #open file
    urls_file = open('movies_urls.txt', 'w+')
    for i in movies.keys():
        urls_file.write(str(i) + " " + movies[i] + '\n')
    urls_file.close()
get_movies_urls()