from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import re
import json

name_xpath = '//*[@id="topSection"]/div[2]/div[1]/h1'
tomatometer_xpath = '//*[@id="tomato_meter_link"]/span[2]'
user_score_xpath = '//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/h2/a/span[2]'
rating_xpath = ['//*[@id="mainColumn"]/section[3]/div/div/ul/li[1]/div[2]', '//*[@id="mainColumn"]/section[2]/div/div/ul/li[1]/div[2]']
genre_xpath = ['//*[@id="mainColumn"]/section[3]/div/div/ul/li[2]/div[2]', '//*[@id="mainColumn"]/section[2]/div/div/ul/li[2]/div[2]']
directors_xpath = ['//*[@id="mainColumn"]/section[3]/div/div/ul/li[3]/div[2]','//*[@id="mainColumn"]/section[2]/div/div/ul/li[3]/div[2]']
writters_xpath =['//*[@id="mainColumn"]/section[3]/div/div/ul/li[4]/div[2]', '//*[@id="mainColumn"]/section[2]/div/div/ul/li[4]/div[2]']
synopsis_xpath = '//*[@id="movieSynopsis"]'
cast_xpath = '//*[@id="movie-cast"]/div/div'

chrome_options = Options()
chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-proxy-server')
def get_movies_urls():
    in_loop = True
    browse_movies_url = 'https://www.rottentomatoes.com/browse/dvd-streaming-all/'
    movies = {}
    #create the patterns to find the urls and the names of the movies
    url_pattern = re.compile(r'href\s*=\"/m/\w*?\"')
    name_pattern = re.compile('<h3 class=\"movieTitle\">.*?</h3>')
    #open the browser
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")
    browser.get(browse_movies_url)

    #search through the movies list, adding each movie and it's url into the dictionary
    while(in_loop == True):            
        try:
            button = browser.find_element_by_css_selector('.btn.btn-secondary-rt.mb-load-btn')
            button.click()
        except NoSuchElementException:
            in_loop = False
            break
    elements = []
    try:
        elements = browser.find_elements_by_class_name('mb-movie')
    except NoSuchElementException:
        print("Movies not found!")
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
    browser.close()
    return movies

def get_movie_info(movie_url):
    site_layout = 0
    url = "https://www.rottentomatoes.com" + movie_url
    names = []
    directors = []
    ratings = []
    genres = []
    tomatometers = []
    user_scores = []
    writters = []
    synop = []
    cast = []
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")
    browser.get(url)
    #movie's name
    try:
        names.append(browser.find_element_by_xpath(name_xpath))
    except NoSuchElementException:
        print("Name of the movie not found")
    name = ''
    if(len(names) > 0):
        name = str(names[0].get_attribute('innerHTML'))
    #scores
    try:
        tomatometers.append(browser.find_element_by_xpath(tomatometer_xpath))
    except NoSuchElementException:
        print("Tomatometer of the movie not found")
    tomatometer = ''
    if(len(tomatometers) > 0):
        tomatometer = str(tomatometers[0].get_attribute('innerHTML'))
    try:
        user_scores.append(browser.find_element_by_xpath(user_score_xpath))
    except NoSuchElementException:
        print("User score of the movie not found")
    user_score = ''
    if(len(user_scores) > 0):
        user_score = str(user_scores[0].get_attribute('innerHTML'))
    #movie's info
    try:
        ratings.append(browser.find_element_by_xpath(rating_xpath[site_layout]))
    except NoSuchElementException:
        site_layout = 1
        try:
            ratings.append(browser.find_element_by_xpath(rating_xpath[site_layout]))
        except NoSuchElementException:
            print('Rating of the movie not found')
    rating = ''
    if(len(ratings) > 0):
        rating = str(ratings[0].get_attribute('innerHTML'))
    try:
        genres.append(browser.find_element_by_xpath(genre_xpath[site_layout]))
    except NoSuchElementException:
        print("Genre of the movie not found")
    genre = ''
    if(len(genres) > 0):
        genre = str(genres[0].get_attribute('innerHTML'))
    try:
        directors.append(browser.find_element_by_xpath(directors_xpath[site_layout]))
    except NoSuchElementException:
        print('Directors of the movie not found')
    director = ''
    if(len(directors) > 0):
        director = str(directors[0].get_attribute('innerHTML'))
        director = re.sub(r'\s*<a href=\".*\">', '', director)
        director = re.sub(r'</a>', '', director)
    try:
        writters.append(browser.find_element_by_xpath(writters_xpath[site_layout]))
    except NoSuchElementException:
        print('Writters of the movie not found')
    writter = ''
    if(len(writters) > 0):
        writter = str(writters[0].get_attribute('innerHTML'))
        writter = re.sub(r'\s*<a href=\".*\">', '', writter)
        writter = re.sub(r'</a>', '', writter)
    #synopsis
    try:
        synop.append(browser.find_element_by_xpath(synopsis_xpath))
    except NoSuchElementException:
        print("Synopsis of the movie not found")
    synopsis = ''
    if(len(synop) > 0):
        synopsis = str(synop[0].get_attribute('innerHTML'))
    #cast
    cast_temp = []
    try:
        cast_temp.append(browser.find_element_by_xpath(cast_xpath))
    except NoSuchElementException:
        print("Cast of the movie not found")
    cast_block = ''
    if(len(cast_temp) > 0):
        cast_block = str(cast_temp[0].get_attribute('innerHTML'))
        cast_actors_reg = []
        cast_actors_reg = re.findall('<span title=\"[\w\s]*\">[\w\s]*</span>', cast_block)
        for ac in cast_actors_reg:
            temp = re.sub(r'<span title=\"[\w\s]*\">\s*', '', ac)
            temp = re.sub(r'</span>', '', temp)
            cast.append(temp)
    
    browser.close()
    #data treatment
    rating = rating.strip()
    name = name.strip()
    tomatometer = re.sub('[\s%]*', '', tomatometer)
    user_score = re.sub('[\s%]*', '', user_score)
    genre = re.sub('\s*', '', genre)
    director = director.replace('\n', '')
    director = director.strip()
    writter = writter.replace('\n', '')
    writter = writter.strip()
    synopsis = synopsis.strip()
    for i in range(0, len(cast)):
        cast[i] = cast[i].strip()
    genre_list = genre.split(',')
    director_list = director.split(',')
    writters_list = writter.split(',')
    movie_json = {"Name": name,
                "Tomatometer": tomatometer,
                "User score": user_score,
                "Rating": rating,
                "Genre": genre_list,
                "Directed by": director_list,
                "Written by": writters_list,
                "Synopsis": synopsis,
                "Cast": cast
                }
    return movie_json

def get_movie_info_from_file(input_file, output_file = None):
    l = 0
    bak_open = False
    try:
        input_file = open(input_file, 'r')
    except IOError:
        print("Error when opening the file!")
        return
    try:
        backup_file = open(output_file + '_backup.txt','w+', buffering=1)
        bak_open = True
    except IOError:
        print("Warning! Impossible to create a backup file")
    json_file = []
    for line in input_file:
        l+=1
        print(l)
        try:
            result = get_movie_info(line)
            json_file.append(result)
            if bak_open == True:
                backup_file.write(str(result) + '\n')
        except: 
            pass
    input_file.close()
    if bak_open == True:
        backup_file.close()
    if(output_file != None):
        try:
            out_file = open(output_file, 'w+', encoding='utf-8')
        except IOError:
            print('Error when saving the file')
            return
        json.dump(json_file, out_file, indent=4, ensure_ascii=False)
        out_file.close()


