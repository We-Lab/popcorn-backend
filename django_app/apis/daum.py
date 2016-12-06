import re
import requests
from bs4 import BeautifulSoup
from pyparsing import makeHTMLTags, withAttribute
from movie.models import Movie, Grade, Genre, MakingCountry, MovieImages, Actor, MovieActor, Director
from mysite import settings

__all__ = [
    'movie_search',
]


def people(request):
    people_info = []
    try:
        people_response = requests.get(request)
        bs_people = BeautifulSoup(people_response.text, "html.parser")
        count = 0

        while True:
            used_link = bs_people.select("ul.list_join li")[count]
            actor_role = used_link.select('span.txt_join')[0].text
            name_kor = used_link.select('em.emph_point')[0].text
            name_kor_eng = used_link.select('strong.tit_join')[0].text
            len_of_name_kor = len(name_kor) + 1
            name_eng = name_kor_eng[len_of_name_kor:]
            a_tag = used_link.findAll('a', attrs={'href': re.compile("/person/")})[0]
            actor_id = re.findall(r'\d+', a_tag['href'])
            img_tag = used_link.select("img")[0]
            profile_url = img_tag['src']
            people_info.append(
                {'character_name': actor_role, 'daum_id': actor_id, 'name_eng': name_eng, 'name_kor': name_kor, 'profile_url': profile_url})
            count += 1
    except:
        pass
    return people_info


def video_search(request):
    video_response = requests.get(request)
    bs_videos = BeautifulSoup(video_response.text, 'html.parser')
    meta, metaEng = makeHTMLTags("meta")
    img_meta = meta.copy().setParseAction(withAttribute(('property', 'og:image')))
    for img in img_meta.searchString(bs_videos):
        content = img.content
        video_trailer_id = content.split("/")[-2]
        video_trailer_url = "http://videofarm.daum.net/controller/video/viewer/Video.html?vid={}&play_loc=daum_movie&autoplay=true".format(video_trailer_id)
    return video_trailer_url


def resize_image(request):
    index = 4
    image_split = request.rsplit('/', 5)
    replacement = ['R200x0.q99', 'R500x0.q99', 'R700x0.q99']
    movie_img_url = []
    for nums in range(3):
        image_split[index] = replacement[nums]
        movie_img_url.append('/'.join(image_split))
    return movie_img_url


def list_genorater(movie_search, num, request):
    count = 0
    list = []
    while True:
        try:
            detail = movie_search.get("channel").get("item")[int(num)].get(request)[count].get("content")
            list.append(detail)
            count += 1
        except:
            break
    return list


def resized_image_list_genorater(movie_search, num, request):
    count = 1
    resized_list = []
    while True:
        try:
            detail = movie_search.get("channel").get("item")[int(num)].get(request + "{}".format(count)).get("content")
            resized_detail = resize_image(detail)
            resized_list.append(resized_detail)
            count += 1
        except:
            break
    return resized_list


def movie_search(keyword):
    r = requests.get("https://apis.daum.net/contents/movie?apikey={}&q={}&output=json".format(settings.DAUM_API_KEY, keyword))
    movie_search = r.json()
    title = []
    num_of_movies = movie_search.get("channel").get("totalCount")
    title_eng = movie_search.get("channel").get("item")[0].get("eng_title")[0].get("content")
    title_kor = movie_search.get("channel").get("item")[0].get("title")[0].get("content")
    title.append(title_kor)
    title.append(title_eng)
    for num in range(num_of_movies):
        title_link = movie_search.get("channel").get("item")[int(num)].get("title")[0].get("link")
        daum_id = re.findall(r'\d+', title_link)
        if Movie.objects.filter(daum_id=daum_id[0]):
            pass
        else:
            title_eng = movie_search.get("channel").get("item")[int(num)].get("eng_title")[0].get("content")
            title_kor = movie_search.get("channel").get("item")[int(num)].get("title")[0].get("content")
            created_year = movie_search.get("channel").get("item")[int(num)].get("year")[0].get("content")
            run_time = movie_search.get("channel").get("item")[int(num)].get("open_info")[2].get("content")
            grade = movie_search.get("channel").get("item")[int(num)].get("open_info")[1].get("content")
            synopsis = movie_search.get("channel").get("item")[int(num)].get("story")[0].get("content")

            sub_movie_images = resized_image_list_genorater(movie_search, num, 'photo')
            nation_list = list_genorater(movie_search, num, 'nation')
            genre_list = list_genorater(movie_search, num, 'genre')

            title_link = movie_search.get("channel").get("item")[int(num)].get("title")[0].get("link")
            people_info = people(title_link)

            grade = Grade.objects.get_or_create(
                grade=grade,
            )

            movie = Movie.objects.create(
                daum_id=daum_id[0],
                title_kor=title_kor,
                title_eng=title_eng,
                created_year=created_year,
                synopsis=synopsis,
                grade=grade[0],
                run_time=run_time,
            )


            for photo in sub_movie_images:
                MovieImages.objects.create(
                    movie=movie,
                    url=photo,
                    )

            specific_movie = Movie.objects.get(daum_id=daum_id[0])
            try:
                trailer_link = movie_search.get("channel").get("item")[int(num)].get("trailer")[0].get("link")
                main_trailer = video_search(trailer_link)
                specific_movie.main_trailer = main_trailer
                specific_movie.save()

                img_url = movie_search.get("channel").get("item")[int(num)].get("thumbnail")[0].get("content")
                movie_main_image = resize_image(img_url)
                specific_movie.img_url = movie_main_image
                specific_movie.save()
            except:
                pass


            for genres in genre_list:
                genre = Genre.objects.get_or_create(
                    genre=genres,
                )
                specific_movie.genre.add(genre[0])


            for nations in nation_list:
                country = MakingCountry.objects.get_or_create(
                    making_country=nations,
                )
                specific_movie.making_country.add(country[0])


            for person in people_info:
                if person['character_name'] == '감독':
                    director = Director.objects.get_or_create(
                        daum_id=person['daum_id'][0],
                        name_eng=person['name_eng'],
                        name_kor=person['name_kor'],
                        profile_url=person['profile_url']
                    )
                    specific_movie.director.add(director[0])
                else:
                    actors = Actor.objects.get_or_create(
                        daum_id=person['daum_id'][0],
                        name_eng=person['name_eng'],
                        name_kor=person['name_kor'],
                        profile_url=person['profile_url']
                    )
                    MovieActor.objects.get_or_create(
                        movie=movie,
                        actor=actors[0],
                        character_name=person['character_name']
                    )
    return title