from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import re

def get_movies_urls(save_file = False):
    in_loop = True
    browse_movies_url = 'https://www.rottentomatoes.com/browse/dvd-streaming-all/'
    movies = {}
    #create the patterns to find the urls and the names of the movies
    url_pattern = re.compile(r'href\s*=\"/m/\w*?\"')
    name_pattern = re.compile('<h3 class=\"movieTitle\">.*?</h3>')
    #open the browser
    browser = webdriver.Firefox()
    browser.get(browse_movies_url)

    #search through the movies list, adding each movie and it's url into the dictionary
    while(in_loop == True):
        elements = []
        try:
            elements = browser.find_elements_by_class_name('mb-movie')
        except NoSuchElementException:
            print("Movies not found!")
            break
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
            button = browser.find_element_by_css_selector('.btn.btn-secondary-rt.mb-load-btn')
            button.click()
        except NoSuchElementException:
            in_loop = False
            break
    #open file
    if(save_file == True):
        urls_file = open('movies_urls.txt', 'w+')
        for i in movies.keys():
            urls_file.write(str(i) + " " + movies[i] + '\n')
        urls_file.close()
    browser.close()
    return movies

def get_movie_info(movie_url):
        url = "https://www.rottentomatoes.com/" + movie_url
        browser = webdriver.Firefox()
        browser.get(url)
        names = []
        ratings = []
        info = []
        synopsis = []
        cast = []
        try:
            names = browser.find_elements_by_css_selector('.mop-ratings-wrap__title.mop-ratings-wrap__title--top')
        except NoSuchElementException:
            print("Name of the movie not found")
        try:
            ratings = browser.find_elements_by_class_name('mop-ratings-wrap__percentage')
        except NoSuchElementException:
            print("Ratings of the movie not found")
        try:
            info = browser.find_elements_by_css_selector('.content-meta.info')
        except NoSuchElementException:
            print("Info of the movie not found")
        try:
            synopsis = browser.find_elements_by_id('movieSynopsis')
        except NoSuchElementException:
            print("Synopsis of the movie not found")
        '''
        try:
            cast = browser.find_element_by_class_name('castSection')
        except NoSuchElementException:
            print("Cast of the movie not found")
        clean_name = ''
        if(len(names) > 0):
            clean_name = str(names[0].get_attribute('outerHTML')).replace('<h1 class=\"mop-ratings-wrap__title mop-ratings-wrap__title--top\">','')
            clean_name = clean_name.replace('</h1>','')
        tomatometer = ''
        user_score = ''
        if(len(ratings) > 1):
            tomatometer = re.sub('<.*?\">\s*', '', str(ratings[0].get_attribute('outerHTML')))
            tomatometer = re.sub('\s*?</span>', '', tomatometer)
            user_score = re.sub('<.*?\">\s*', '', str(ratings[1].get_attribute('outerHTML')))
            user_score = re.sub('\s*?</span>', '', user_score)
        rating = ''
        genre = []
        directors = []
        writters = []
        if(len(info) > 0):
            r = info[0].get_attribute('outerHTML')
            rating = re.findall(r'Rating:</div>\s*?<div class=\"meta-value\">\w*?', str(r))[0]
            rating = re.sub(r'Rating:</div>\s*?<div class=\"meta-value\">','', str(rating))
            gen= re.findall(r'Genre:</div>\s*?<div class=\"meta-value\">[\w\s\,\-]*?', str(r))[0]
            gen = re.sub(r'Genre:</div>\s*?<div class=\"meta-value\">', '', str(gen))
            gen = re.sub(r'\s*?', '', str(gen))
            genre = gen.split(',')
            dr= re.findall(r'Directed By:(.|\s)*?</li>', str(r))[0]
            dr_href = re.findall(r'>[\w\s]*</a>', str(dr[0]))
            for i in range(len(dr_href)):
                temp = dr_href[i].replace('>', '')
                temp = temp.replace('</a>', '')
                directors.append(str(temp))
            wr= re.findall(r'Written By:(.|\s)*?</li>', str(r))[0]
            wr_href = re.findall(r'>[\w\s]*</a>', str(wr[0]))
            for i in range(len(wr_href)):
                temp = wr_href[i].replace('>', '')
                temp = temp.replace('</a>', '')
                writters.append(str(temp))
            '''
        synop = ''
        if(len(synopsis) > 0):
            synop = re.findall('>\s*.*\s*<', str(synopsis[0].get_attribute('outerHTML')))[0]
            synop = synop.replace('>', '')
            synop = synop.replace('<', '')
            
#get_movies_urls()
get_movie_info('m/a_nice_girl_like_you')