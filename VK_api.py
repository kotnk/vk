import requests
import time
from urllib.parse import urlencode


def app_init():
    url = 'https://oauth.vk.com/authorize'
    try:
        app_id = int(input('Введите ID вашего приложения: '))
        params = {
            'client_id': app_id,
            'display': 'page',
            'scope': 'friends',
            'response_type': 'token',
            'v': '5.52'
        }
        token = input(
            f"Пройдите по ссылке {'?'.join((url, urlencode(params)))} и скопируйте токен из адресной строки:\n>")
        return token
    except ValueError:
        print('Значение должно состоять из цифр')
        app_init()


class User:

    def __init__(self, uid, token):
        self.uid = uid
        self.token = token
        self.link = 'https://vk.com/id' + str(self.uid)
        url = 'https://api.vk.com/method/users.get'
        params = {
            'v': '5.52',
            'access_token': token,
            'user_ids': self.uid
        }
        response = requests.get(url, params=params)
        if 'error' not in response.json().keys():
            self.first_name = response.json()['response'][0]['first_name']
            self.last_name = response.json()['response'][0]['last_name']
        else:
            print('Ошибка запроса. Проверьте токен.')
            main()

    def __and__(self, target):
        url = 'https://api.vk.com/method/friends.getMutual'
        params = {
            'v': '5.52',
            'access_token': self.token,
            'source_uid': self.uid,
            'target_uid': target.uid
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print('*' * 20, 'Список общих друзей', '*' * 20)
            for i in response.json()['response']:
                time.sleep(0.34)
                temp_user = User(i, self.token)
                print(f'{temp_user.first_name} {temp_user.last_name} ({temp_user})')
            print('>>>Конец списка.\n')
        else:
            print('Что-то пошло не так, давайте попробуем снова.')
            main()

    def __str__(self):
        return self.link


def user_selector(token):
    user1 = int(input('Введите ID первого пользователя: '))
    user2 = int(input('Введите ID второго пользователя: '))
    user_comparison(user1, user2, token)


def user_comparison(user1, user2, token):
    user1 = User(user1, token)
    user2 = User(user2, token)
    print(f'Сравниванием {user1} и {user2}')
    user1 & user2


def main():
    token = app_init()
    user_selector(token)


main()
