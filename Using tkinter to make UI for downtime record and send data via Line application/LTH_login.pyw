from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from LTH_database import LTH_DB


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบแจ้งซ่อมเครื่องจักรออนไลน์")

        # Screen
        self.root.screen_width = int(self.root.winfo_screenwidth()/2)
        self.root.screen_height = int(self.root.winfo_screenheight()/2)
        self.root.screen_position_x = int(self.root.screen_width/2)
        self.root.screen_position_y = int(self.root.screen_height/2)
        self.root.geometry(
            f"{self.root.screen_width}x{self.root.screen_height}+{self.root.screen_position_x}+{self.root.screen_position_y}")
        self.root.resizable(False, False)

        # Background
        self.img = Image.open("login_pic.jpg")
        self.img = self.img.resize(
            (self.root.screen_width, self.root.screen_height), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.img)
        self.bg_image = Label(
            self.root, image=self.bg).pack()

        # Login Frame
        Frame_login = Frame(self.root, bg='white')
        Frame_login.place(x=self.root.screen_position_x/2, y=self.root.screen_position_y/2,
                          width=self.root.screen_width/2, height=self.root.screen_height/2)

        title = Label(Frame_login, text='ยินดีต้อนรับสู่', font=(
            'Arial', 16, 'bold'), fg='#0080FF', bg='White').pack()
        description = Label(Frame_login, text='ระบบการแจ้งซ่อมเครื่องจักรแบบออนไลน์', font=(
            'Arial', 10, 'bold'), fg='#0080FF', bg='White').pack()

        title_user = Label(Frame_login, text='รหัสพนักงาน', font=(
            'Arial', '8', 'bold'), bg='lightgrey').pack(pady=5)
        self.entry_user = Entry(Frame_login, justify='center',
                                bg='lightblue')
        self.entry_user.pack()
        self.entry_user.focus()

        title_password = Label(Frame_login, text='รหัสผ่าน', font=(
            'Arial', '8', 'bold'), bg='lightgrey').pack(pady=5)
        self.entry_password = Entry(Frame_login, justify='center',
                                    show='*', bg='lightblue')
        self.entry_password.pack()
        self.entry_password.bind('<Return>',self.login_function)

        login_button = Button(self.root, command=self.login_function, cursor='hand2', text='เข้าสู่ระบบ', font=(
            'Arial', '12', 'bold'), bg='#0000CD', fg='white').place(x=self.root.screen_position_x/1.25, y=self.root.screen_position_y*1.4,
                                                                    width=self.root.screen_width/5, height=self.root.screen_height/10)

    def login_function(self,event=None):
        self.User = LTH_DB.get_user_info(self.entry_user.get())
        try:
            if self.User['Password'] == self.entry_password.get():
                LTH_DB.log_transaction(self.User['Username'])
                self.entry_user.delete(0, END)
                self.entry_password.delete(0, END)
                messagebox.showinfo("แจ้งเตือน", 'เข้าสู่ระบบสำเร็จ')
                self.go_to_main()
            else:
                self.entry_password.delete(0, END)
                self.entry_password.focus()
                messagebox.showerror(
                    "แจ้งเตือน", 'กรุณาใส่ "รหัสผ่าน" ใหม่อีกครั้ง')
        except:
            self.entry_user.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_user.focus()
            messagebox.showerror(
                "แจ้งเตือน", 'กรุณาใส่ "รหัสพนักงาน/รหัสผ่าน" ใหม่อีกครั้ง')

    def go_to_main(self):
        if self.User['Department_EN'] == 'Production':
            self.root.destroy()
            from LTH_production_main import Production_screen
        else:
            pass
            self.root.destroy()
            from LTH_maintenance_main import Maintenance_screen


root = Tk()
obj = Login(root)
root.mainloop()
