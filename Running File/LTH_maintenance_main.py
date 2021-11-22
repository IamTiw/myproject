from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
from LTH_database import LTH_DB
from LTH_notify import Notify
from LTH_calculate import calculate


class Maintenance_screen:
    def __init__(self, root):
        # Get LTH_id
        self.LTH_id = LTH_DB.get_log_transaction()

        # Screen
        self.root = root
        self.root.title('(ฝ่ายซ่อมบำรุง) ระบบแจ้งซ่อมเครื่องจักรออนไลน์')
        self.root['bg'] = '#F8FFFE'

        self.root.screen_width = int(self.root.winfo_screenwidth()/2)
        self.root.screen_height = int(self.root.winfo_screenheight()/2)
        self.root.screen_position_x = int(self.root.screen_width/2)
        self.root.screen_position_y = int(self.root.screen_height/2)
        self.root.geometry(
            f"{self.root.screen_width}x{self.root.screen_height}+{self.root.screen_position_x}+{self.root.screen_position_y}")
        self.root.resizable(False, False)

        # Title
        maintenance_title = Label(self.root, text='รายการแจ้งซ่อม', font=(
            'Arial', '18', 'bold'), fg='black', bg='#F8FFFE')
        maintenance_title.place(x=5, y=10)

        # Table Frame
        frame_table = Frame(self.root, bg='lightgrey')
        frame_table.place(x=10, y=70, width=self.root.screen_width -
                          30, height=self.root.screen_height-80)

        self.data_table = ttk.Treeview(frame_table, columns=(
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), show='headings', height=100)
        self.data_table.place(x=0, y=0, width=self.root.screen_width -
                              46, height=self.root.screen_height-80)

        column_no = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        column_name = ['รายการ', 'สถานะ', 'ไลน์', 'เครื่องจักร', 'อาการที่พบ', 'สาเหตุ', 'การแก้ไขปัญหา',
                       'เวลาเครื่องเสีย', 'เวลาเริ่มซ่อม', 'เวลาซ่อมเสร็จ', 'ผู้บันทึก', 'ผู้ซ่อม', 'เวลาเครื่องเสียทั้งหมด (นาที)', 'เวลาซ่อมทั้งหมด (นาที)']
        table_width = [130, 100, 100, 100, 150,
                       150, 150, 200, 200, 200, 50, 50, 200, 200]

        for cn, tw, name in zip(column_no, table_width, column_name):
            self.data_table.column(cn, width=tw, anchor='center')
            self.data_table.heading(cn, text=name)

        # Initial Data
        self.refresh_data()

        # Scroll Bar
        sb_y = Scrollbar(frame_table, orient=VERTICAL)
        sb_y.pack(side=RIGHT, fill=Y)
        self.data_table.config(yscrollcommand=sb_y.set)
        sb_y.config(command=self.data_table.yview)

        sb_x = Scrollbar(frame_table, orient=HORIZONTAL)
        sb_x.pack(side=BOTTOM, fill=X)
        self.data_table.config(xscrollcommand=sb_x.set)
        sb_x.config(command=self.data_table.xview)

        # Finished Button
        button_finished = Button(self.root, command=self.create_finished_window, text='ซ่อมเสร็จแล้ว', font=(
            'Arial', '10', 'bold'), fg='Black', bg='#00FF00')
        button_finished.place(
            x=self.root.screen_position_x*2-110, y=10, width=100, height=30)

        # Repairing Button
        button_repairing = Button(self.root, command=self.change_status_to_repairing, text='เริ่มซ่อม', font=(
            'Arial', '10', 'bold'), fg='Black', bg='Yellow')
        button_repairing.place(
            x=self.root.screen_position_x*2-240, y=10, width=100, height=30)

    def change_status_to_repairing(self, *args):
        target = self.data_table.focus()
        data = self.data_table.item(target, 'values')
        status = 'กำลังซ่อม'
        try:
            if data[1] != 'กำลังซ่อม' and data[1] != 'ซ่อมเสร็จแล้ว':
                repairing = self.data_table.item(target, values=(
                    data[0],
                    status,
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    LTH_DB.time_record(),
                    data[9],
                    data[10],
                    self.LTH_id[3],
                ))
                messagebox.showinfo(
                    'แจ้งเตือน', 'เปลี่ยนสถานะเป็น "กำลังซ่อม" แล้ว')

                self.update_data()

                Notify.maintenance_notify(
                    data[0],
                    status,
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    LTH_DB.time_record(),
                    '',
                    '',
                    '',
                    self.LTH_id[3],
                )

            else:
                messagebox.showerror(
                    'แจ้งเตือน', 'กรุณาเลือกเฉพาะ "เครื่องจักรเสีย" เท่านั้น')
        except:
            pass

    def update_data(self):
        new_data = []
        for data in self.data_table.get_children():
            new_data.append(self.data_table.item(data)["values"])

        LTH_DB.update_to_share_drive()

        for new in new_data:
            LTH_DB.record_to_share_drive(new)

        self.refresh_data()

    def create_finished_window(self):
        target = self.data_table.focus()
        data = self.data_table.item(target, 'values')
        status = 'ซ่อมเสร็จแล้ว'

        try:
            if data[1] == 'ซ่อมเสร็จแล้ว':
                # New Window
                self.new_window = tkinter.Toplevel(self.root)
                self.new_window.title('แจ้งซ่อม')

                self.nw_width = int(self.root.screen_width*0.50)
                self.nw_height = int(self.root.screen_height*0.50)
                self.nw_position_x = int(self.root.screen_position_x*1.5)
                self.nw_position_y = int(self.root.screen_position_y*1.5)

                self.new_window.geometry(
                    f"{self.nw_width}x{self.nw_height}+{self.nw_position_x}+{self.nw_position_y}")
                self.new_window.resizable(False, False)

                # Cause
                cause_label = Label(self.new_window, text='สาเหตุของปัญหา:',
                                    font=('Arial', '10', 'bold'))
                cause_label.place(x=10, y=10)

                self.cause_entry = Text(self.new_window)
                self.cause_entry.place(x=self.nw_position_x/4,
                                       y=11, width=180, height=50)

                # Action
                action_label = Label(
                    self.new_window, text='วิธีที่ใช้แก้ปัญหา:', font=('Arial', '10', 'bold'))
                action_label.place(x=10, y=75)

                self.action_entry = Text(self.new_window)
                self.action_entry.place(x=self.nw_position_x/4,
                                        y=75, width=180, height=50)

                # Button create
                create_new = Button(self.new_window, text='บันทึกการซ่อม',
                                    command=self.change_status_to_finished, width=10, fg='black', bg='#00FF00', font=('Arial', '8', 'bold'))
                create_new.place(x=self.nw_position_x/4, y=140)
                
            elif data[1] == 'เครื่องจักรเสีย':
                messagebox.showerror(
                    'แจ้งเตือน', 'กรุณาเปลี่ยนเป็นสถานะ หรือ เลือกหัวข้อ "กำลังซ่อม" เท่านั้น')

            else:
                finished = self.data_table.item(target, values=(
                    data[0],
                    status,
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    LTH_DB.time_record(),
                    data[10],
                    self.LTH_id[3],
                    calculate.cal_downtime(data[7], LTH_DB.time_record()),
                    calculate.cal_repairing_time(
                        data[8], LTH_DB.time_record()),
                    self.LTH_id[4],
                ))

                messagebox.showinfo(
                    'แจ้งเตือน', 'เปลี่ยนสถานะเป็น "ซ่อมเสร็จแล้ว"')

                self.update_data()

                Notify.maintenance_notify(
                    data[0],
                    status,
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    LTH_DB.time_record(),
                    calculate.cal_downtime(data[7], LTH_DB.time_record()),
                    calculate.cal_repairing_time(
                        data[8], LTH_DB.time_record()),
                    self.LTH_id[3],
                )

        except:
            pass

    def refresh_data(self):
        self.get_data = LTH_DB.get_record()[1:]

        for data in self.data_table.get_children():
            self.data_table.delete(data)

        for data_id, data in zip(range(len(self.get_data)), self.get_data):
            self.data_table.insert(
                parent='', index=data_id, iid=data_id, values=data)

    def change_status_to_finished(self, *args):
        target = self.data_table.focus()
        data = self.data_table.item(target, 'values')
        status = 'ซ่อมเสร็จแล้ว'
        get_cause = self.cause_entry.get("1.0", 'end-1c')
        get_action = self.action_entry.get("1.0", 'end-1c')
        try:
            if get_cause != "" and get_action != "":
                finished = self.data_table.item(target, values=(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    get_cause,
                    get_action,
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11],
                    data[12],
                    data[13],
                ))

                messagebox.showinfo(
                    'แจ้งเตือน', 'บันทึกข้อมูลแล้ว')

                self.update_data()

                Notify.maintenance_notify(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[12],
                    data[13],
                    self.LTH_id[3],
                )
            else:
                messagebox.showerror(
                    "แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน")
        except:
            pass


if __name__ == '__main__':
    pass
else:
    root = Tk()
    obj = Maintenance_screen(root)
    root.mainloop()
