import requests
import json

token = '316109efc4cbdeb2997daf111c8fe14d520fc1763473c258a4e58c05959c9f21b6f35e26c3d662d4907a1'


def write_json (data):
    with open('photos_json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_largest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']


def download_photo(url):
    r = requests.get(url, stream=True)

    filename = '1/' + url.split('/')[-1]

    with open(filename, 'bw') as file:

        for chunk in r.iter_content(4096):
            file.write(chunk)

# r = requests.get('https://api.vk.com/method/photos.get',
#                 params={'owner_id': 169106238,
#                         'album_id': 'profile',
#                         'photo_sizes': True,
#                         'access_token': token})
# write_json(r.json())

photos = json.load(open('photos_json'))['response']

for photo in photos:
    sizes = photo['sizes']

    max_sizes_url = max(sizes, key=get_largest)['src']
    download_photo(max_sizes_url)