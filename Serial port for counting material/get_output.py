import serial
import csv
import os
import time
from tkinter import *


class Get_weight:
    global database_path
    database_path = f'{os.getcwd()}\\Database\\'

    def get_output_from_balacer():
        ser = serial.Serial('COM3')
        read_ser = ser.read(7)    # get output only "weight"
        output = float(read_ser.decode('UTF-8'))
        # output = ser.readline().decode('ascii')

        return output  # return int output

    def record_to_csv(item_no, quantity, weight):
        open_file = open(f'{database_path}part_log.csv', 'a', newline='')
        record = csv.writer(open_file)
        record.writerow([item_no, quantity, weight])

    def get_avg_part_weight(item_no):
        open_file = open(f'{database_path}part_log.csv', 'r')
        read_file = list(csv.reader(open_file))

        sum_qty = 0.0
        sum_weight = 0.0
        avg_weight = 0.0

        for item in read_file:
            if item[0] == item_no:
                sum_qty = sum_qty + int(item[1])
                sum_weight = sum_weight + float(item[2])

        try:
            avg_weight = sum_weight/sum_qty
        except:
            pass

        return avg_weight

    def show_on_led_arduino(quantity):
        ser = serial.Serial('COM5')
        time.sleep(2)
        ser.write(bytes(str(quantity), encoding='UTF-8'))
