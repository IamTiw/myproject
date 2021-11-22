from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
from LTH_database import LTH_DB
from LTH_notify import Notify


class Production_screen:
    def __init__(self, root):
        # Get LTH_id
        self.LTH_id = LTH_DB.get_log_transaction()

        # Screen
        self.root = root
        self.root.title('(ฝ่ายผลิต) ระบบแจ้งซ่อมเครื่องจักรออนไลน์')
        self.root['bg'] = '#F8FFFE'

        self.root.screen_width = int(self.root.winfo_screenwidth()/2)
        self.root.screen_height = int(self.root.winfo_screenheight()/2)
        self.root.screen_position_x = int(self.root.screen_width/2)
        self.root.screen_position_y = int(self.root.screen_height/2)
        self.root.geometry(
            f"{self.root.screen_width}x{self.root.screen_height}+{self.root.screen_position_x}+{self.root.screen_position_y}")
        self.root.resizable(False, False)

        # Title
        production_title = Label(self.root, text='ประวัติการแจ้งซ่อม', font=(
            'Arial', '18', 'bold'), fg='black', bg='#F8FFFE')
        production_title.place(x=5, y=10)

        # New Downtime Button
        button_new_downtime = Button(self.root, command=self.create_new_downtime_window, text='แจ้งซ่อม', font=(
            'Arial', '10', 'bold'), fg='White', bg='#b60022')
        button_new_downtime.place(
            x=self.root.screen_position_x*2-110, y=10, width=100, height=30)

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

    def create_new_downtime_window(self):
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

        # Line
        line_label = Label(self.new_window, text='ไลน์การผลิต:',
                           font=('Arial', '10', 'bold'))
        line_label.place(x=10, y=10)

        lines = ['DL6-PLUS 1', 'BEAM', 'ROUND COLUMN']
        self.line_variable = StringVar(self.new_window)
        self.line_variable.set('โปรดเลือกไลน์การผลิต')

        line_dropdown = OptionMenu(
            self.new_window, self.line_variable, *lines, command=self.machine_list)
        line_dropdown.place(x=self.nw_position_x/4, y=7)

        # Machine
        machine_label = Label(
            self.new_window, text='เครื่องจักร:', font=('Arial', '10', 'bold'))
        machine_label.place(x=10, y=55)

        self.machine_list()

        # Symptom
        symptom_label = Label(
            self.new_window, text='อาการที่พบ:', font=('Arial', '10', 'bold'))
        symptom_label.place(x=10, y=100)
        self.symptom_entry = Entry(self.new_window)
        self.symptom_entry.place(x=self.nw_position_x/4, y=102, width=170)

        # Button create
        create_new = Button(self.new_window, text='แจ้งซ่อม',
                            command=self.create_new_downtime, width=10, fg='White', bg='#b60022', font=('Arial', '8', 'bold'))
        create_new.place(x=self.nw_position_x/4, y=140)

    def machine_list(self, *args):
        try:
            self.machine_dropdown.destroy()

        except:
            pass

        if self.line_variable.get() == 'DL6-PLUS 1':
            machines = ['Milling Machine', 'Greasing',
                        'Assembly Profile SP1', 'Assembly Profile SP2', 'Bearing Assembly', 'Deflection Test','DL Final Test']

        elif self.line_variable.get() == 'BEAM':
            machines = ['Testing', 'Packing']

        elif self.line_variable.get() == 'ROUND COLUMN':
            machines = ['Assembly', 'EOL']

        else:
            machines = ['โปรดเลือกเครื่องจักรที่พบ']

        self.machine_variable = StringVar(self.new_window)
        self.machine_variable.set('โปรดเลือกเครื่องจักรที่พบ')

        self.machine_dropdown = OptionMenu(
            self.new_window, self.machine_variable, *machines)
        self.machine_dropdown.place(x=self.nw_position_x/4, y=50)

    def refresh_data(self):
        self.get_data = LTH_DB.get_record()[1:]
        
        for data in self.data_table.get_children():
            self.data_table.delete(data)

        for data_id, data in zip(range(len(self.get_data)), self.get_data):
            self.data_table.insert(
                parent='', index=data_id, iid=data_id, values=data)

    def create_new_downtime(self):
        if self.line_variable.get() != 'โปรดเลือกไลน์การผลิต' and self.machine_variable.get() != 'โปรดเลือกเครื่องจักรที่พบ' and self.symptom_entry.get() != "":

            self.check_no = LTH_DB.get_record()

            for no in range(len(self.check_no)):
                pass

            no += 1
            no = '{0:04}'.format(no)
            tracking_no = f'LTH-Downtime-{no}'
            status = 'เครื่องจักรเสีย'

            LTH_DB.record_to_share_drive([tracking_no, status, self.line_variable.get(
            ), self.machine_variable.get(), self.symptom_entry.get(), '', '', LTH_DB.time_record(), '', '', self.LTH_id[3]])

            messagebox.showinfo('แจ้งเตือน', 'บันทึกการแจ้งซ่อมสำเร็จ')
            self.refresh_data()

            Notify.production_notify(tracking_no, status, self.line_variable.get(
            ), self.machine_variable.get(), self.symptom_entry.get(), LTH_DB.time_record(), self.LTH_id[3])

        else:
            messagebox.showerror(
                'แจ้งเตือน', 'กรุณาเลือก ไลน์ผลิต / เครื่องจักร / อาการที่พบ ให้ครบด้วยครับ')
            self.create_new_downtime_window()

if __name__ == '__main__':
    pass
else:
    root = Tk()
    obj = Production_screen(root)
    root.mainloop()
