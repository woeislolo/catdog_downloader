import uuid
import requests

from django.conf import settings

from celery import shared_task


animal_urls = {'cat': 'https://cataas.com/cat',
#   'cat': 'https://api.thecatapi.com/v1/images/search',
    'dog': 'https://dog.ceo/api/breeds/image/random'
    }


@shared_task
def download_cat_dog(animal):
    url = animal_urls[animal]
    response = requests.get(url)
    if animal == 'dog':
        response_url = response.json().get('message')
        response = requests.get(response_url)
    file_ext = response.headers.get('Content-Type').split('/')[1]
    file_name = settings.BASE_DIR / animal / f'{uuid.uuid4()}.{file_ext}'
    with open(file_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)
    return True
