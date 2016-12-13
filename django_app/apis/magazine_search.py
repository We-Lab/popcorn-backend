from bs4 import BeautifulSoup
from movie.models import Actor, Magazine
import requests
import re


def magazine_search():
    """
    1. 현재 db에 있는 배우 아이디로 다음 매거진을 검색합니다.
    2. 다음 크롤링으로 매거진의 아이디를 확인합니다.
    3. 매거진 아이디가 db에 존재하니 않은 매거진이면 저장을 시도합니다.
    4. 메거진의 본문이 20자가 안되면 저장하지 않습니다.

    """
    actors = Actor.objects.all()

    for actor in actors:
        actor_id = actor.daum_id
        response = requests.get("http://movie.daum.net/person/main?personId={}".format(actor_id))
        bs_response = BeautifulSoup(response.text, "html.parser")
        try:
            link = bs_response.select('a.link_magazine')[0]['href']
            img_link = bs_response.select('a.link_magazine')[0].select('span.magazine_img')
            img_url = re.findall(r'\((.*)\)', img_link[0]['style'])
            mag_id = re.findall(r'\d+', link)[1]
            if Magazine.objects.filter(mag_id=mag_id).exists():
                pass
            else:
                text = []
                mag = requests.get(link)
                bs_mag = BeautifulSoup(mag.text, 'html.parser')
                mag_title = bs_mag.select('h3.tit_view')[0].text
                body = bs_mag.select('div.section_view.section_editor p')
                for count in range(len(body)):
                    main_body = body[count].text
                    text.append(main_body)

                mag_text = "\n".join(text)
                if len(mag_text) > 20:
                    Magazine.objects.create(
                        mag_id=mag_id,
                        img_url=img_url[0],
                        title=mag_title,
                        content=mag_text,
                    )
                else:
                    pass
        except:
            pass
