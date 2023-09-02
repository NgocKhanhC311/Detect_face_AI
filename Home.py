from tkinter import *
from tkinter import filedialog
from gui_app import *
import os

class MyMenu(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='#FFCC99')

        self.title = BlinkingTitle(self, "||\_(-_-)_/||",('Small Fonts',55)) # Tạo tiêu đề nhấp nháy
        self.title.place(relx = 0, rely= 0.1, relheight=0.4, relwidth=1) #Đặt vị trí
        self.title.config(bg ="#FFCC99") #Chỉnh màu background

        self.file_path=""

        #Tạo Button
        self.Button1 = Button(self)
        self.Button1.place(relx=0.18, rely=0.3, relheight=0.12, relwidth=0.64)
        self.Button1.config(bg ="#FFCC99")
        self.Button1.config(text='''Camera''')
        self.Button1.config(font=('Small Fonts',25))
        self.Button1.config(fg="#FFFFFF") # cài đặt màu chữ
        self.Button1.config(activebackground="#FFCC99") #màu bg khi được click
        self.Button1.config(activeforeground="#99FFFF") #màu fg khi được click
        self.Button1.config(relief='flat',borderwidth=0,highlightthickness= 0) # chỉnh viền.
        self.Button1.config(command=self.call_start) # câu lệnh thực thi khi bấm vào
        # chỉnh màu sắc button khi di chuột vào
        self.Button1.bind('<Enter>',self.on_enter)
        self.Button1.bind('<Leave>',self.on_leave)

        self.Button4 = Button(self)
        self.Button4.place(relx=0.18, rely=0.45, relheight=0.12, relwidth=0.64)
        self.Button4.config(bg ="#FFCC99")
        self.Button4.config(text='''File''')
        self.Button4.config(font=('Small Fonts',25))
        self.Button4.config(fg="#FFFFFF")
        self.Button4.config(activebackground="#FFCC99")
        self.Button4.config(activeforeground="#99FFFF")
        self.Button4.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.Button4.config(command=self.open_file)
        self.Button4.bind('<Enter>',self.on_enter)
        self.Button4.bind('<Leave>',self.on_leave)

        self.Button2 = Button(self)
        self.Button2.place(relx=0.18, rely=0.6, relheight=0.12, relwidth=0.64)
        self.Button2.config(bg ="#FFCC99")
        self.Button2.config(text='''Docs''')
        self.Button2.config(font=('Small Fonts',25))
        self.Button2.config(fg="#FFFFFF")
        self.Button2.config(activebackground="#FFCC99")
        self.Button2.config(activeforeground="#99FFFF")
        self.Button2.config(command=lambda:self.Docs())
        self.Button2.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.Button2.bind('<Enter>',self.on_enter)
        self.Button2.bind('<Leave>',self.on_leave)


        self.Button3 = Button(self) 
        self.Button3.place(relx=0.18, rely=0.75, relheight=0.12, relwidth=0.64)
        self.Button3.config(bg ="#FFCC99")
        self.Button3.config(text='''Quit''')
        self.Button3.config(font=('Small Fonts',25))
        self.Button3.config(fg="#FFFFFF")
        self.Button3.config(activebackground="#FFCC99")
        self.Button3.config(activeforeground="#99FFFF")
        self.Button3.config(command=quit)
        self.Button3.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.Button3.bind('<Enter>',self.on_enter)
        self.Button3.bind('<Leave>',self.on_leave)

        
    def on_enter(self,event):
        event.widget.config(fg='black')
        
    def on_leave(self,event):
        event.widget.config(fg='white')

    # Gọi tới AppGui
    def call_start(self):
        self.file_path =" "
        appGui = APP_GUI(self.master,self.file_path)
        appGui.place(relx=0, rely= 0, relheight= 1, relwidth=1)


    #Mở cửa sổ chọn file
    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        appGui = APP_GUI(self.master,self.file_path)
        appGui.place(relx=0, rely= 0, relheight= 1, relwidth=1)


    # Mở tài liệu của nhóm
    def Docs(self):
        os.startfile("Báo cáo Lập trình Python - Nhóm lớp 1 - Nhóm 1.pdf")    
        

class Root(Tk):
    def __init__(self):
        super().__init__()

        self.title('Title')
        self.geometry('1800x900')
        # đặt hình dáng con trỏ chuột
        self.config(cursor="mouse")


        img = PhotoImage(file="img/icon_ai.png")
        self.iconphoto(False,img)

        w = self.winfo_width()//2
        h = self.winfo_height()
        self.frame_photo = Photo(self,"img/mem2.png",h,w)
        self.frame_photo.place(relx=0, rely= 0, relheight= 1, relwidth=0.5)

        self.myMenu = MyMenu(self)
        self.myMenu.place(relx=0.5, rely= 0, relheight= 1, relwidth=0.5)


if __name__ == '__main__':
    app = Root()
    app.mainloop()
    