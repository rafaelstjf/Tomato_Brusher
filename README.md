# Tomato Brusher
Web scraping script to use in the rotten tomatoes website


## Introduction

Tomato Brusher is a script to get the movie info from Rotten Tomatoes' website. The script has 3 functions:

* `get_movies_urls() `: Goes through all<sup>1</sup> the [movie list](https://www.rottentomatoes.com/browse/dvd-streaming-all/) scraping the movies' urls, after that the function returns a dictionary containing the tuple (name, url).

* `get_movie_info(movie_url)`: Receiving a movie's url (e.g. `/m/you_should_have_left`) the function uses _Selenium_ and scrapes the movie's info and saves in a JSON like format.

* `get_movie_info_from_file(input_file, output_file)`: Receives a list of urls and scrapes all of them, saving in the output file.


## Known issues

I developed this script to do some research for a project in my master's degree course. As the webscraping isn't the main focus of the project, it didn't go throught a bug hunt. Some of the bugs I noticed are:

1 - There is a problem that the last movie in the movie list isn't added to the list of urls.

2 - The movie info is gathered finding the elements by XPATH, therefore if the page's structure changes, the script won't work properly.
