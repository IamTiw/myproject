import datetime


class calculate:
    def change_time_to_int(time_row):
        cal_time = time_row
        cal_time_split = cal_time.split()
        cal_time_split_date = cal_time_split[0].split('-')
        cal_time_split_time = cal_time_split[1].split(':')
        cal_time_final = datetime.datetime(
            int(cal_time_split_date[2]),
            int(cal_time_split_date[1]),
            int(cal_time_split_date[0]),
            int(cal_time_split_time[0]),
            int(cal_time_split_time[1]),
            int(cal_time_split_time[2])
        )

        return cal_time_final

    def cal_repairing_time(repairing_time, finished_time):
        total_repairing_time = calculate.change_time_to_int(
            finished_time) - calculate.change_time_to_int(repairing_time)

        return total_repairing_time

    def cal_downtime(start_time, finished_time):
        total_downtime = calculate.change_time_to_int(
            finished_time) - calculate.change_time_to_int(start_time)

        return total_downtime
