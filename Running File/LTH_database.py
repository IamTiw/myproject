import csv
import datetime
import os


class LTH_DB:
    global database_path
    database_path = f"{os.getcwd()}\\Database\\"

    def get_user_info(LTH_id):
        user_record = open(f"{database_path}LTH_User_DB.csv", 'r',
                           newline='', encoding='utf-8')
        users = csv.reader(user_record)
        users = list(users)[1:]

        data = ''

        for user_info in users:
            if LTH_id == user_info[0]:
                data = {
                    'Username': user_info[0],
                    'Password': user_info[1],
                    'Name_EN': user_info[2],
                    'Name_TH': user_info[3],
                    'Department_EN': user_info[4],
                    'Department_TH': user_info[5],
                }

        return data

    def record_to_share_drive(record):
        downtime_file = open(f"{database_path}LTH_DowntimeRecord_DB.csv",
                             'a', newline='', encoding='UTF-8')
        write_downtime_file = csv.writer(downtime_file)
        write_downtime_file.writerow(record)

    def get_record():
        downtime_file = open(f"{database_path}LTH_DowntimeRecord_DB.csv",
                             'r', encoding='UTF-8')
        read_downtime_file = csv.reader(downtime_file)
        read_downtime_file = list(read_downtime_file)

        return read_downtime_file

    def log_transaction(LTH_id):
        # Write
        file_record = open(f"{database_path}LTH_Login_transaction.csv", 'a',
                           newline='', encoding='utf-8')
        record_file = csv.writer(file_record)

        # Read
        user_record = open(f"{database_path}LTH_User_DB.csv", 'r',
                           newline='', encoding='utf-8')
        users = csv.reader(list(user_record))

        for user in users:
            if user[0] == LTH_id:
                user.append(LTH_DB.time_record())
                record_file.writerow(user)

    def get_log_transaction():
        log_file = open(f"{database_path}LTH_Login_transaction.csv", 'r', encoding='utf-8')
        read_file = csv.reader(log_file)

        for user_id in read_file:
            pass

        return user_id

    def update_to_share_drive():
        column_name = ['รายการ', 'สถานะ', 'ไลน์', 'เครื่องจักร', 'อาการที่พบ', 'สาเหตุ', 'การแก้ไขปัญหา',
                       'เวลาเครื่องเสีย', 'เวลาเริ่มซ่อม', 'เวลาซ่อมเสร็จ', 'ผู้บันทึก', 'ผู้ซ่อม', 'เวลาเครื่องเสียทั้งหมด (นาที)', 'เวลาซ่อมทั้งหมด (นาที)','แผนก']

        clear_file = open(f"{database_path}LTH_DowntimeRecord_DB.csv",
                          'w', newline='', encoding='UTF-8')
        write_downtime_file = csv.writer(clear_file)
        write_downtime_file.writerow(column_name)

    def time_record():
        time = datetime.datetime.now().strftime("%d-%m-%Y %X")

        return time
