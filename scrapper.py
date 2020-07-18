from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep,time
from random import randint
from warnings import warn


pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2010,2020)]


names = []
years = []
imdb_ratings = []
metascores = []
votes = []

start_time = time()
requests = 0
headers = {"Accept-Language": "en-US, en;q=0.5"}


for year_url in years_url:

    for page in pages:

        response = get('http://www.imdb.com/search/title?release_date=' + year_url +'&sort=num_votes,desc&page=' + page, headers = headers)
        sleep(randint(8,15))
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))

        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

        html_soup = BeautifulSoup(response.text, 'html.parser')
        movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

        for container in movie_containers:
            if container.find('div', class_ = 'ratings-metascore') is not None:
                name = container.h3.a.text
                names.append(name)

                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)

                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                m_score = container.find('span', class_ = 'metascore').text
                metascores.append(int(m_score))

                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))

movie_ratings = pd.DataFrame({'movie': names,'year': years,'imdb': imdb_ratings,'metascore': metascores,'votes': votes})

movie_ratings.to_csv('movies.csv')