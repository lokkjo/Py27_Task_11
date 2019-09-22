import requests
import json
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

def open_file(file):
    text = ''
    with open(file, encoding='utf-8') as file:
        for line in file:
            text += line
    return text

def write_file(file, text):
    with open(file, 'wt', encoding='utf-8') as file:
        file.write(text)

def translate_it(from_file, to_file, from_lang, to_lang='ru'):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """
    API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    from_text = open_file(from_file)
    params = {
        'key': API_KEY,
        'text': from_text,
        'lang': '{}-{}'.format(from_lang, to_lang),
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    write_file(to_file, ''.join(json_['text']))
    print(f'Файл {from_file}, направление перевода: '
          f'{from_lang.upper()}-{to_lang.upper()}. \n '
          f'Результат: {to_file}. Перевод завершён.\n')


def translate_it_to_ya_disk(from_file, to_file, from_lang, to_lang='ru'):
    translate_it(from_file, to_file, from_lang, to_lang)

    up_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    up_path = f'disk:/translate_upload/{to_file}'
    up_headers = {
        'Authorization': 'OAuth AgAAAAAAgSCLAAXh4MV_1qnuMksRsjwfYB1wLmE'
    }
    up_params = {
        'path': up_path,
        'overwrite': True,
    }

    response_URL = requests.get(up_URL, headers=up_headers, params=up_params)
    json_ = response_URL.json()

    with open(to_file, 'rt', encoding="utf-8") as f:
        text = f.read()
        response_upload = requests.put(json_['href'], text.encode('utf-8'))
    print(f'Бэкап файла {to_file} завершён. Ваш Яндекс.Диск\n')

# print(translate_it('В настоящее время доступна единственная опция — признак включения в ответ автоматически определенного языка переводимого текста. Этому соответствует значение 1 этого параметра.', 'no'))

if __name__ == '__main__':
    # print(translate_it('привет', 'en'))
    print('Задача 1: Решение\n')
    translate_it('DE.txt', 'DE_RU.txt', 'de', 'ru')
    translate_it('ES.txt', 'ES_RU.txt', 'es')
    translate_it('FR.txt', 'FR_RU.txt', 'fr')
    translate_it('FR.txt', 'FR_DE.txt', 'fr', 'de')

    print('Задача 2: Решение\n')
    print('Ссылка на папку с результатом: https://yadi.sk/d/F7FNw1lcANVU6A\n')
    translate_it_to_ya_disk('ES.txt', 'ES_EN.txt', 'es', 'en')
    translate_it_to_ya_disk('DE.txt', 'DE_ES.txt', 'de', 'es')
    translate_it_to_ya_disk('FR.txt', 'FR_RU.txt', 'fr')
