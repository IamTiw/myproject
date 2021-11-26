import requests
import csv
import win32com.client as win32


class ConvertText:
    def convert_list_to_string(org_word, separator=' '):
        return separator.join(org_word)


class Notify:
    def prod_notify(data):
        url = 'https://notify-api.line.me/api/notify'
        token = 'Input your token'  # <<<<<<<<<<<<<<<<<<<<<<<<< [1/6]
        header = {'content-type': 'application/x-www-form-urlencoded',
                  'Authorization': 'Bearer '+token}
        msg = {'message': data}
        request = requests.post(url, headers=header, data=msg)


class CsvDatabase:
    global csv_location, csv_name
    csv_location = r"Input your path"  # <<<<<<<<<<<<<<<<<<<<<<<<< [2/6]
    csv_name = 'Input your filename'  # <<<<<<<<<<<<<<<<<<<<<<<<< [3/6]

    def update_csv(datasets):
        new_csv = open(f'{csv_location}\{csv_name}',
                       'a', encoding="UTF-8", newline='')
        writer_csv = csv.writer(new_csv)
        writer_csv.writerow(list(datasets))

    def read_csv():
        open_csv = open(f'{csv_location}\{csv_name}', 'r', encoding='UTF-8')
        reader_csv = csv.reader(open_csv)
        return list(reader_csv)


class Email:
    def send_email(tar_date, body_email):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        # mail.TO = "xxx@email.com"#<<<<<<<<<<<<<<<<<<<<<<<<< [4/6]
        # mail.CC = 'xxx@email.com'#<<<<<<<<<<<<<<<<<<<<<<<<< [5/6]
        # <<<<<<<<<<<<<<<<<<<<<<<<< [6/6]
        recipients = ['xxx@email.com', 'xxx@email.com']

        for rp in recipients:
            mail.Recipients.Add(rp)

        mail.Subject = f'Daily Production Output on: {tar_date}'
        mail.Body = f'Dear All \n{body_email} \n\nThis is an automated message please do not reply.'
        attachment = f'{csv_location}\{csv_name}'
        mail.Attachments.Add(attachment)

        mail.Send()
