from tomatobrusher import *


'''
movies_urls = get_movies_urls()

f = open('urls.txt', 'w+')
for i in movies_urls.keys():
    f.write(movies_urls[i] + '\n')
'''

get_movie_info_from_file('urls.txt', 'completo.json')