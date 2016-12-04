import re
import requests
from bs4 import BeautifulSoup
from pyparsing import makeHTMLTags, withAttribute
from movie.models import Movie, Grade, Genre, MakingCountry, MovieImages, Actor, MovieActor, Director
from mysite import settings

__all__ = [
    'movie_search',
]


def movie_search(keyword):
    r = requests.get("https://apis.daum.net/contents/movie?apikey={}&q={}&output=json".format(settings.DAUM_API_KEY, keyword))
    movie_search = r.json()
    movies_search = []
    daum_ids = []
    num_of_movies = movie_search.get("channel").get("totalCount")
    for num in range(num_of_movies):
        title_link = movie_search.get("channel").get("item")[int(num)].get("title")[0].get("link")
        daum_id = re.findall(r'\d+', title_link)
        if Movie.objects.filter(daum_id=daum_id[0]):
            daum_ids.append(daum_ids)
        else:
            img_url = movie_search.get("channel").get("item")[int(num)].get("thumbnail")[0].get("content")
            # 이미지 사이즈 (S M L)
            image_split = img_url.rsplit('/', 5)
            index = 4
            replacement = ['R200x0.q99', 'R500x0.q99', 'R700x0.q99']
            movie_img_url = []
            for nums in range(3):
                image_split[index] = replacement[nums]
                movie_img_url.append('/'.join(image_split))
            title_eng = movie_search.get("channel").get("item")[int(num)].get("eng_title")[0].get("content")
            title_kor = movie_search.get("channel").get("item")[int(num)].get("title")[0].get("content")
            created_year = movie_search.get("channel").get("item")[int(num)].get("year")[0].get("content")
            run_time = movie_search.get("channel").get("item")[int(num)].get("open_info")[2].get("content")
            grade = movie_search.get("channel").get("item")[int(num)].get("open_info")[1].get("content")
            synopsis = movie_search.get("channel").get("item")[int(num)].get("story")[0].get("content")


            photo_list = []
            count = 1
            while True:
                try:
                    photos = movie_search.get("channel").get("item")[int(num)].get("photo{}".format(count)).get("content")
                    photo_list.append(photos)
                    count += 1
                except:
                    break


            resized_photo_url = []
            for image in photo_list:
                image_split = image.rsplit('/', 5)
                index = 4
                replacement = ['R200x0.q99', 'R500x0.q99', 'R700x0.q99']
                each_movie_photo_url = []
                for nums in range(3):
                    image_split[index] = replacement[nums]
                    each_movie_photo_url.append('/'.join(image_split))
                resized_photo_url.append(each_movie_photo_url)
                resized_photo_url.append(image)


            count = 0
            nation_list = []
            while True:
                try:
                    nations = movie_search.get("channel").get("item")[int(num)].get("nation")[count].get("content")
                    nation_list.append(nations)
                    count += 1
                except:
                    break


            count = 0
            genre_list = []
            while True:
                try:
                    genres = movie_search.get("channel").get("item")[int(num)].get("genre")[count].get("content")
                    genre_list.append(genres)
                    count += 1
                except:
                    break


            director_info = []
            actor_info = []
            try:
                title_link = movie_search.get("channel").get("item")[int(num)].get("title")[0].get("link")
                response = requests.get(title_link)
                bs = BeautifulSoup(response.text, "html.parser")
                count = 0

                while True:
                    used_link = bs.select("ul.list_join li")[count]

                    # 역할
                    actor_role = used_link.select('span.txt_join')[0].text
                    if "감독" in actor_role:
                        name_kor = used_link.select('em.emph_point')[0].text
                        name_kor_eng = used_link.select('strong.tit_join')[0].text
                        len_of_name_kor = len(name_kor) + 1
                        # 영문 이름
                        name_eng = name_kor_eng[len_of_name_kor:]
                        a_tag = used_link.findAll('a', attrs={'href': re.compile("/person/")})[0]
                        # 배우 아이디
                        actor_id = re.findall(r'\d+', a_tag['href'])
                        img_tag = used_link.select("img")[0]
                        # 배우 사진
                        profile_url = img_tag['src']

                        director_info.append(
                            {'daum_id': actor_id, 'name_eng': name_eng, 'name_kor': name_kor, 'profile_url': profile_url}
                        )
                        count += 1
                    else:
                        name_kor = used_link.select('em.emph_point')[0].text
                        name_kor_eng = used_link.select('strong.tit_join')[0].text
                        len_of_name_kor = len(name_kor) + 1
                        # 영문 이름
                        name_eng = name_kor_eng[len_of_name_kor:]
                        a_tag = used_link.findAll('a', attrs={'href': re.compile("/person/")})[0]
                        # 배우 아이디
                        actor_id = re.findall(r'\d+', a_tag['href'])
                        img_tag = used_link.select("img")[0]
                        # 배우 사진
                        profile_url = img_tag['src']

                        actor_info.append(
                            {'daum_id': actor_id, 'name_eng': name_eng, 'name_kor': name_kor, 'profile_url': profile_url,
                             'character_name': actor_role}
                        )
                        count += 1
            except:
                pass


            video_list = []
            count = 0
            while True:
                try:
                    videos = movie_search.get("channel").get("item")[int(num)].get("video")[count].get("link")
                    if videos:
                        response_videos = requests.get(videos)
                        bs_videos = BeautifulSoup(response_videos.text, "html.parser")
                        meta, metaEnd = makeHTMLTags("meta")
                        img_meta = meta.copy().setParseAction(withAttribute(('property', 'og:image')))
                        img_ref = img_meta
                        for img in img_ref.searchString(bs_videos):
                            content = img.content
                        video_trailer_id = content.split("/")[-2]
                        video_trailer_url = "http://videofarm.daum.net/controller/video/viewer/Video.html?vid={}&play_loc=daum_movie&autoplay=true".format(
                            video_trailer_id)
                        video_list.append(video_trailer_url)
                    count += 1
                except:
                    break


            trailer_link = movie_search.get("channel").get("item")[int(num)].get("trailer")[0].get("link")
            if trailer_link:
                response = requests.get(trailer_link)
                bs = BeautifulSoup(response.text, "html.parser")
                meta, metaEnd = makeHTMLTags("meta")
                img_meta = meta.copy().setParseAction(withAttribute(('property', 'og:image')))
                img_ref = img_meta
                for img in img_ref.searchString(bs):
                    content = img.content
                trailer_id = content.split("/")[-2]
                trailer_url = "http://videofarm.daum.net/controller/video/viewer/Video.html?vid={}&play_loc=daum_movie&autoplay=true".format(trailer_id)


            for genres in genre_list:
                try:
                    genre = Genre.objects.create(
                        genre=genres,
                    )
                except:
                    genre = Genre.objects.filter(genre=genres)


            try:
                grade = Grade.objects.create(
                    grade=grade,
                )
            except:
                grade = Grade.objects.get(grade=grade)


            for nations in nation_list:
                try:
                    nation = MakingCountry.objects.create(
                        making_country=nations,
                    )
                except:
                    pass
                    nation = MakingCountry.objects.filter(making_country=nations)


            movie = Movie.objects.create(
                daum_id=daum_id[0],
                title_kor=title_kor,
                title_eng=title_eng,
                created_year=created_year,
                synopsis=synopsis,
                grade=grade,
                run_time=run_time,
                img_url=movie_img_url,
            )


            for actor in actor_info:
                actors = Actor.objects.get_or_create(
                    daum_id=actor['daum_id'][0],
                    name_eng=actor['name_eng'],
                    name_kor=actor['name_kor'],
                    profile_url=actor['profile_url']
                )
                movie_actor = MovieActor.objects.get_or_create(
                    movie=movie,
                    actor=actors[0],
                    character_name=actor['character_name']
                )


            for directors in director_info:
                director = Director.objects.get_or_create(
                    daum_id=directors['daum_id'][0],
                    name_eng=directors['name_eng'],
                    name_kor=directors['name_kor'],
                    profile_url=directors['profile_url']
                )


            for photo in resized_photo_url:
                try:
                    movie_image = MovieImages.objects.create(
                        movie=movie,
                        url=photo,
                    )
                except:
                    pass


            specific_movie = Movie.objects.get(daum_id=daum_id[0])
            for genre in genre_list:
                g, created = Genre.objects.get_or_create(genre=genre)
                specific_movie.genre.add(g)


            for nation in nation_list:
                n, created = MakingCountry.objects.get_or_create(making_country=nation)
                specific_movie.making_country.add(n)


            for director in director_info:
                d, created = Director.objects.get_or_create(
                    daum_id=director['daum_id'][0],
                    name_eng=director['name_eng'],
                    name_kor=director['name_kor'],
                    profile_url=director['profile_url']
                )
                specific_movie.director.add(d)