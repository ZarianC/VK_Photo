import requests, json, os, zipfile, datetime

count_d_photo = 0
now_date = datetime.datetime.now()

# Получаем токен из файла
with open('data/token.txt') as token_object:
    token = token_object.readline()


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
def save_photo(url, folder_name):
    r = requests.get(url, stream=True)

    filename = 'photo/' + folder_name.rstrip() + '/' + url.split('/')[-1]

    with open(filename, 'bw') as file:

        for chunk in r.iter_content(4096):
            file.write(chunk)

        global count_d_photo
        global count_photo
        count_d_photo += 1
        print('[ ' + str(now_date) + ' ]' + ' Скачано ' + str(count_d_photo) + ' из ' + str(count_photo) + ' фотографий ')


# Получаем фото пользователя с максимальным расширением
def download_photo(id, count):
    r = requests.get('https://api.vk.com/method/photos.get',
                     params={'owner_id': id,
                             'album_id': 'profile',
                             'photo_sizes': True,
                             'count': count,
                             'rev': 0,
                             'access_token': token})

    write_json(r.json())

    photos = json.load(open('photos_json'))['response']

    for photo in photos:
        sizes = photo['sizes']

        max_sizes_url = max(sizes, key=get_largest)['src']
        save_photo(max_sizes_url, id)


# Основной блок работы скрипта

print("Выберите режим работы:")
print("1. Скачивание фотографии по id пользователей")
print("2. Уникализация фото из указанной папки")

operation_mode = input('Ваш выбор - ')

if operation_mode == '1':
    count_photo = input('Сколько фото скачивать у каждого id? - ')

    with open('data/id_user.txt') as file_object:
        id_users = file_object.readlines()
        for id_user in id_users:
            print('[ ' + str(now_date) + ' ]' + ' Начинаем скачивать фото у пользователя с id ' + id_user)
            if os.path.exists('photo/' + id_user.rstrip()):
                print('[ ' + str(now_date) + ' ]' + ' Фото пользователя с id '
                              + id_user.rstrip() +
                              ' уже скачаны')
                continue
            else:
                os.mkdir('photo/' + id_user.rstrip())
                download_photo(id_user, count_photo)
                print('[ ' + str(now_date) + ' ]' + ' Скачали фото у пользователя с id ' + id_user)
                count_d_photo = 0

# Начимнаем архивацию результатов парсинга
    print()
    print('[ ' + str(now_date) + ' ]' + ' Начинаем архивацию фотографий')
    yourfolder = 'photo'
    path_archive = 'result/photo-' + str(now_date) + '.zip'
    arch = zipfile.ZipFile(path_archive, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(yourfolder):
        print
        root + '/' + str(files)
        for tarfile in files:
            if tarfile != '':
                arch.write(root + '/' + tarfile)
    arch.close()
    print('[ ' + str(now_date) + ' ]' + ' Архивация фотографий закончена. Путь к архиву - ' + path_archive)
