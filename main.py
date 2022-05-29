from copyreg import pickle
import requests
import time
import json
import pickle
from pprint import pprint
from ya_poligon_private_token import YA_POLIGON_TOKEN

TOKEN = '2619421814940190'

class SuperHeroAPI():

    def get_smartest(self, heros_list):
        heros_info_list = list()
        for hero_name in heros_list:
            r = requests.get(f'https://superheroapi.com/api/{TOKEN}/search/{hero_name}')
            if r.status_code != 200:
                pprint(f'name={hero_name}. Запрос не успешен')
                time.sleep(1.0)
                continue
            heros_info_list.append(r.json())
            time.sleep(0.1)

        smartest = list()
        intell_list = list()
        max_intell = 0
        for hero_info in heros_info_list:
            results_list = hero_info['results']
            for li_dict in results_list:
                if 'powerstats' in li_dict:
                    _in = li_dict['powerstats']['intelligence']
                    intell = int(_in)
                    intell_list.append( [li_dict['name'], intell] )
                    if intell > max_intell:
                        max_intell = intell

        for item in intell_list:
            if item[1] == max_intell:
                smartest.append(item[0])
        
        return smartest

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload(self, file_path: str, file_name):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        href = self._get_upload_link(disk_file_path=f'Netology/{file_name}').get('href', '')
        response = requests.put(href, data=open(file_path + f'{file_name}', 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')


if __name__ == '__main__':

    # Задание 1
    shapi = SuperHeroAPI()
    heros_list = ['Hulk', 'Captain America', 'Thanos']
    smartest_hero = shapi.get_smartest(heros_list)
    pprint(smartest_hero)


    # Задание 2
    path_to_file = 'D:/'
    file_name = 'some_awesome_file.txt'
    uploader = YaUploader(YA_POLIGON_TOKEN)
    result = uploader.upload(path_to_file, file_name)
    