import requests
import json

token = '316109efc4cbdeb2997daf111c8fe14d520fc1763473c258a4e58c05959c9f21b6f35e26c3d662d4907a1'


# Сохраняем ответ сервера ВК в файл photos_json
def write_json (data):
    with open('photos_json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# Определяем ориентацию фото (горизонтальное или вертикальное)
def get_largest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']


# Сохраняем фото на жесткий диск
def save_photo(url):
    r = requests.get(url, stream=True)

    filename = '1/' + url.split('/')[-1]

    with open(filename, 'bw') as file:

        for chunk in r.iter_content(4096):
            file.write(chunk)


# Получаем фото пользователя с максимальным расширением
def download_photo(id_user, count):
    r = requests.get('https://api.vk.com/method/photos.get',
                     params={'owner_id': id_user,
                             'album_id': 'profile',
                             'photo_sizes': True,
                             'count': count,
                             'access_token': token})
    write_json(r.json())

    photos = json.load(open('photos_json'))['response']

    for photo in photos:
        sizes = photo['sizes']

        max_sizes_url = max(sizes, key=get_largest)['src']
        save_photo(max_sizes_url)

print("Выберите режим работы:")
print("1. Скачивание фотографии по id пользователя")
print("2. Уникализация фото из указанной папки")

operation_mode = input('Ваш выбор - ')

if operation_mode == '1':
    count_photo = input('Сколько фото скачивать? - ')
    download_photo('169106238б', count_photo)
