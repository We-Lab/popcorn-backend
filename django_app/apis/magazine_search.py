from bs4 import BeautifulSoup
from movie.models import Actor, Magazine
import requests
import re


def magazine_search():
    actors = Actor.objects.all()

    for actor in actors:
        actor_id = actor.daum_id
        print('actor: {}'.format(actor_id))
        response = requests.get("http://movie.daum.net/person/main?personId={}".format(actor_id))
        bs_response = BeautifulSoup(response.text, "html.parser")
        try:
            link = bs_response.select('a.link_magazine')[0]['href']
            img_link = bs_response.select('a.link_magazine')[0].select('span.magazine_img')
            img_url = re.findall(r'\((.*)\)', img_link[0]['style'])
            mag_id = re.findall(r'\d+', link)[1]
            print(mag_id)
            if Magazine.objects.filter(mag_id=mag_id).exists():
                pass
            else:
                text = []
                mag = requests.get(link)
                bs_mag = BeautifulSoup(mag.text, 'html.parser')
                mag_title = bs_mag.select('h3.tit_view')[0].text
                body = bs_mag.select('div.section_view.section_editor')
                for count in range(len(body)):
                    main_body = body.select('div.section_view.section_editor p')[count].text
                    text.append(main_body)
                mag_text = "\n".join(text)
                if len(text) > 20:
                    Magazine.objects.get_or_create(
                        mag_id=mag_id,
                        img_url=img_url[0],
                        title=mag_title,
                        content=mag_text,
                    )
                else:
                    pass

        except:
            pass