import requests


class Notify:
    def prod_notify(prod_line, date_today, start_time, stop_time, total_good):
        url = 'https://notify-api.line.me/api/notify'
        token = 'Input your token here!!!'
        header = {'content-type': 'application/x-www-form-urlencoded',
                  'Authorization': 'Bearer ' + token}
        msg = {
            'message': [
                f'\nLine: {prod_line}'
                f'\nDate: {date_today}'
                f'\nTime: {start_time} - {stop_time}'
                f'\nGood: {total_good}'
            ]}
        request = requests.post(url, headers=header, data=msg)
