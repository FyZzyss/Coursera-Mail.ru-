import requests
import datetime

ACCESS_TOKEN = 'secret'

class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        return other.obj < self.obj

def has_letters(input_string):
    return any(char.isalpha() for char in input_string)


def get_dates(id):
    params = {'v': '5.71', 'access_token': ACCESS_TOKEN, 'user_id': id, 'fields': 'bdate'}
    user_date = requests.get('https://api.vk.com/method/friends.get', params=params)
    now = datetime.datetime.now()
    dates_dict = {}
    for i in user_date.json()['response']['items']:
        if 'bdate' in i.keys():
            date = i['bdate'].split('.')
            if len(date) == 3:
                age = now.year - int(date[2])
                if age not in dates_dict.keys():
                    dates_dict[age] = 1
                else:
                    dates_dict[age] += 1
    final_date = [(k, v) for k, v in dates_dict.items()]
    return sorted(final_date, key=lambda x: (reversor(x[1]), x[0]))


def calc_age(uid):
    if has_letters(uid):
        params = {'v': '5.71', 'access_token': ACCESS_TOKEN, 'user_ids': uid}
        user_id = requests.get('https://api.vk.com/method/users.get', params=params)
        return get_dates(user_id.json()['response'][0]['id'])
    else:
        return get_dates(uid)
