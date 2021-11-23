import requests


class Notify:
    mytoken = 'input your token here!!!'
    
    def production_notify(job_no, status, production_line, machine, symptom, downtime_time_record, recorder):
        url = 'https://notify-api.line.me/api/notify'

        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Bearer '+mytoken}

        msg = [
            '\n----------------------'
            f'\nJob No: {job_no}'
            f'\nสถานะ: {status}'
            f'\nLine: {production_line}'
            f'\nเครื่องจักร: {machine}'
            f'\nอาการที่พบ: {symptom}'
            f'\nเวลา: {downtime_time_record}'
            f'\nผู้บันทึก: {recorder}'
            '\n-----------------------'
        ]

        r = requests.post(url, headers=headers, data={'message': msg})

    def maintenance_notify(job_no, status, production_line, machine, symptom, cause, action, downtime_time_record, repairing_time_record, finished_time_record, total_downtime, total_repairing_time, recorder):
        url = 'https://notify-api.line.me/api/notify'

        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Bearer '+mytoken}

        msg = [
            '\n----------------------'
            f'\nJob No: {job_no}'
            f'\nสถานะ: {status}'
            f'\nLine: {production_line}'
            f'\nเครื่องจักร: {machine}'
            f'\nอาการที่พบ: {symptom}'
            f'\nสาเหตุ: {cause}'
            f'\nแก้ไข: {action}'
            f'\nเวลาเครื่องเสีย: {downtime_time_record}'
            f'\nเวลาเริ่มซ่อม: {repairing_time_record}'
            f'\nเวลาซ่อมเสร็จ: {finished_time_record}'
            f'\nเวลาสูญเสียรวม: {total_downtime}'
            f'\nเวลาซ่อมรวม: {total_repairing_time}'
            f'\nผู้บันทึก: {recorder}'
            '\n-----------------------'
        ]

        r = requests.post(url, headers=headers, data={'message': msg})

