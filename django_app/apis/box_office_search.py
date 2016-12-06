import re
import requests
from bs4 import BeautifulSoup

from apis import movie_search
from movie.models import BoxOfficeMovie, Movie


def box_office_search():
    response = requests.get('http://movie.daum.net/premovie/released')
    bs = BeautifulSoup(response.text, "html.parser")
    movie_title_list = bs.select("ul.list_boxthumb li div.desc_boxthumb strong")
    movie_key_elements = bs.select("ul.list_boxthumb li a.link_boxthumb")
    box_office_elements = bs.select("ul.list_boxthumb div.desc_boxthumb dl.list_state")

    for i in range(len(movie_title_list)-10):
        # 파싱한 영화 제목으로 영화 DB에 저장
        movie_title = movie_title_list[i].text
        print(movie_title)
        try:
            movie_search(movie_title)
        except:
            pass

        # 다음 영화ID 파싱 후 DB에서 Foreignkey 추출
        movie_key_element = movie_key_elements[i]
        movie_key_list = re.findall(r'\d+', movie_key_element['href'])
        movie_key = movie_key_list[0]
        print(movie_key)
        movie = Movie.objects.get(daum_id=movie_key)
        print(movie)

        # 개봉일 파싱
        release_date_element = box_office_elements[i].select('dd')[0].text
        release_date_first = re.findall(r'\b[0-9]{4}[./:][0-9]{1,2}[./:][0-9]{1,2}\b', release_date_element)
        release_date = release_date_first[0].replace('.', '-')
        print(release_date)

        # 예매율 파싱
        ticketing_rate_element = box_office_elements[i].select('dd')[1].text
        ticketing_parsed = re.findall(r'\d+\.\d+', ticketing_rate_element)
        ticketing_list = ticketing_parsed[0]
        ticketing_rate = float(ticketing_list)
        print(ticketing_rate)

        # BoxOfficeMovie instance 생성
        try:
            BoxOfficeMovie.objects.create(
                rank=i+1,
                movie=movie,
                release_date=release_date,
                ticketing_rate=ticketing_rate,
            )
        except:
            pass


