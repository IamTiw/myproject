from tkinter import *
from tkinter import messagebox
from get_output import Get_weight


class interface:
    def __init__(self, root):
        self.root = root
        self.root.title('ระบบตรวจสอบจำนวนชิ้นงาน')

        self.screen_width = 300
        self.screen_height = 350
        self.screen_x = int(
            (self.root.winfo_screenwidth() - self.screen_width)/2)
        self.screen_y = int(
            (self.root.winfo_screenheight() - self.screen_height)/2)
        self.root.geometry(
            f'{self.screen_width}x{self.screen_height}+{self.screen_x}+{self.screen_y}')
        self.root.resizable(False, False)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=5)
        button_font = ('Angsana new', '10', 'bold')

        # Get Packaging Weight
        packaging_button = Button(
            self.button_frame, text='บันทึกค่าแพ็คกิ้ง', font=button_font, bg='#bbeedf', fg='black', command=self.get_packaging_weight)
        packaging_button.pack(padx=10, side=LEFT)

        # Get Quantity
        quantity_button = Button(
            self.button_frame, text='คำนวณจำนวนชิ้น', font=button_font, bg='lightblue', fg='black', command=self.calculate)
        quantity_button.pack(padx=10, side=LEFT)

        # Barcode
        self.label_barcode = Label(
            self.root, text='ITEM NUMBER', font=('Arial', '16', 'bold'))
        self.label_barcode.pack(pady=5)
        self.entry_barcode = Entry(
            self.root, width=20, justify=CENTER, font=('Arial', '14'))
        self.entry_barcode.pack()

        self.entry_barcode.bind('<Return>', self.check_part_data)
        self.entry_barcode.focus()

        # Offset Label
        off_x = self.screen_width/9
        off_y = self.screen_height/3

        # Unit
        self.label_unit = Label(self.root, text='กรัม',
                                font=('Arial', '10', 'bold'))
        self.label_unit.place(x=off_x*6.4, y=off_y)

        # Packaging Weight
        self.label_packaging = Label(
            self.root, text='น้ำหนักแพ็คกิ้ง:', font=('Arial', '10', 'bold'))
        self.label_packaging.place(x=off_x, y=off_y+30)

        self.value_packaging = StringVar()
        self.value_packaging.set('0.0')
        self.label_value_packaging = Label(
            self.root, textvariable=self.value_packaging, font=('Arial', '10', 'bold'), bg='white', width=8)
        self.label_value_packaging.place(x=off_x*5.8, y=off_y+30)

        # Part Weight
        self.label_part = Label(
            self.root, text='น้ำหนักชิ้นงานต่อชิ้น:', font=('Arial', '10', 'bold'))
        self.label_part.place(x=off_x, y=off_y + 60)

        self.value_part = StringVar()
        self.value_part.set('0.0')
        self.label_value_part = Label(
            self.root, textvariable=self.value_part, font=('Arial', '10', 'bold'), bg='white', width=8)
        self.label_value_part.place(x=off_x*5.8, y=off_y+60)

        # Gross Weight
        self.label_gross_weight = Label(
            self.root, text='น้ำหนักรวมแพ็คกิ้ง:', font=('Arial', '10', 'bold'))
        self.label_gross_weight.place(x=off_x, y=off_y + 90)

        self.value_gross_weight = StringVar()
        self.value_gross_weight.set('0.0')
        self.label_value_gross_weight = Label(
            self.root, textvariable=self.value_gross_weight, font=('Arial', '10', 'bold'), bg='white', width=8)
        self.label_value_gross_weight.place(x=off_x*5.8, y=off_y+90)

        # Net Weight
        self.label_net_weight = Label(
            self.root, text='น้ำหนักรวมเฉพาะชิ้นงาน:', font=('Arial', '10', 'bold'))
        self.label_net_weight.place(x=off_x, y=off_y + 120)

        self.value_net_weight = StringVar()
        self.value_net_weight.set('0.0')
        self.label_value_net_weight = Label(
            self.root, textvariable=self.value_net_weight, font=('Arial', '10', 'bold'), bg='white', width=8)
        self.label_value_net_weight.place(x=off_x*5.8, y=off_y+120)

        # Quantity
        self.value_quantity = StringVar()
        self.value_quantity.set('-------')
        self.label_quantity = Label(self.root, textvariable=self.value_quantity, font=(
            'Arial', '40', 'bold'), fg='blue')
        self.label_quantity.pack(side=BOTTOM, pady=10)

    def check_part_data(self, event=None):
        self.item_no = self.entry_barcode.get()

        if self.item_no == "":
            self.stop_calculate()
            messagebox.showerror('แจ้งเตือน', 'กรุณาใส่ Item Number ด้วยครับ')

        else:
            self.available = Get_weight.get_avg_part_weight(self.item_no)
            self.value_part.set(f'{self.available:.1f}')

            if self.available == 0:
                self.stop_calculate()
                get_answer = messagebox.askquestion(
                    'แจ้งเตือน', f'Item Number: {self.item_no} \nยังไม่มีในระบบคุณต้องการเพิ่มเข้าไปในระบบหรือไม่', icon='warning')

                if get_answer == 'yes':
                    self.add_new_item()
                    self.entry_barcode.delete(0, 'end')
                else:
                    self.entry_barcode.delete(0, 'end')

            else:
                pass

            return self.available

    def get_packaging_weight(self):
        self.packaging_weight = Get_weight.get_output_from_balacer()
        self.value_packaging.set(self.packaging_weight)

    def stop_calculate(self):
        try:
            self.root.after_cancel(self.calculate)
        except:
            pass

    def calculate(self):
        try:
            self.cal_gross_weight = Get_weight.get_output_from_balacer()
            self.cal_net_weight = self.cal_gross_weight - self.packaging_weight
            self.total_quantity = int(round(
                self.cal_net_weight/self.check_part_data()))

            self.value_gross_weight.set(self.cal_gross_weight)
            self.value_net_weight.set(self.cal_net_weight)
            self.value_quantity.set(f'{self.total_quantity} ชิ้น')

            # Get_weight.show_on_led_arduino(self.total_quantity)
            # Get_weight.record_to_csv(
            # self.item_no, self.total_quantity, self.cal_net_weight)
            self.root.after(100, self.calculate)

        except:
            self.value_quantity.set('-------')
            self.value_gross_weight.set(0.0)
            self.value_net_weight.set(0.0)
            self.stop_calculate()

    def check_weight_new_item(self):
        self.weight_new_item = Get_weight.get_output_from_balacer()
        self.new_item_weight_value.set(f'{self.weight_new_item} กรัม')

    def record_new_item(self):
        Get_weight.record_to_csv(
            self.item_no, int(10), self.weight_new_item)
        messagebox.showinfo('แจ้งเตือน', 'บันทึกข้อมูลเรียบร้อย')
        self.new_window.destroy()

    def add_new_item(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title('เพิ่มชิ้นงาน')

        nw_width = int(self.screen_width*0.75)
        nw_height = int(self.screen_height*0.60)
        nw_x = int(self.screen_x*1.075)
        nw_y = int(self.screen_y*1.25)

        self.new_window.geometry(
            f"{nw_width}x{nw_height}+{nw_x}+{nw_y}")
        self.new_window.resizable(False, False)

        # Item Number
        add_new_item = Label(
            self.new_window, text=self.item_no, font=('Arial', '14', 'bold'))
        add_new_item.pack(pady=5)

        # Comment
        comment = Label(
            self.new_window, text='* กรุณาวางชิ้นงานบนเครื่องชั่งน้ำหนัก 10 ชิ้น *', fg='red')
        comment.pack()

        # Check Weight Button
        get_new_item_weight = Button(self.new_window, text='ตรวจสอบน้ำหนัก', command=self.check_weight_new_item, font=(
            'Arial', '8', 'bold'), bg='lightblue')
        get_new_item_weight.pack(pady=5)

        # Check Weight Value
        self.new_item_weight_value = StringVar()
        self.new_item_weight_value.set('-------- กรัม')
        new_item_weight = Label(
            self.new_window, textvariable=self.new_item_weight_value, font=('Arial', '14', 'bold'))
        new_item_weight.pack(pady=15)

        # Confirm Button
        new_item_record = Button(self.new_window, text='บันทึก', font=(
            'Arial', '10', 'bold'), bg='blue', fg='white', command=self.record_new_item)
        new_item_record.pack(pady=10)


if __name__ == '__main__':
    root = Tk()
    tk_root = interface(root)
    root.mainloop()
else:
    pass
