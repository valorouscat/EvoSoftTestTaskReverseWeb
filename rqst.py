import requests


# получаем ip 
response = requests.get('https://2ip.ru/')
ip = [item[22:-2] for item in response.iter_lines(decode_unicode=True) if "let realIp" in item][0]

# для получения токена необходимо только два параметра, с этой страницы мы их и получаем
response = requests.get('https://www.maxmind.com/en/geoip2-precision-demo')
mm_session = response.cookies.get('mm_session')
csrf = [item[33:-2] for item in response.iter_lines(decode_unicode=True) if "window.MaxMind.X_CSRF_TOKEN" in item][0]

# инициализируем cookie и headers для запроса на получение токена
cookies = {
    'mm_session': f'{mm_session}'
}

headers = {
    'x-csrf-token': f'{csrf}'
}

# получаем токен для GET запроса с таймзоной
response = requests.post('https://www.maxmind.com/en/geoip2/demo/token', cookies=cookies, headers=headers)
token = response.json()['token']

# указываем токен в header
headers_get = {
    'Authorization': f'Bearer {token}'
    }

# отправляем запрос и вычленяем таймзону
response = requests.get(f'https://geoip.maxmind.com/geoip/v2.1/city/{ip}?demo=1', headers=headers_get)
time_zone = response.json()['location']['time_zone']

# парсим список регионов
result_line = []
response = requests.get('https://gist.githubusercontent.com/salkar/19df1918ee2aed6669e2/raw/84215d4a3fcdfeaabad32e87817ae5bc1073a3b7/Timezones%2520for%2520Russian%2520regions')
for line in response.iter_lines(decode_unicode=True):
    if time_zone in line:
        new_line = line[4:-1]
        result_line.append(new_line[:new_line.find(',')-1])

# записываем результат
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(time_zone + '\n' + ', '.join(result_line))