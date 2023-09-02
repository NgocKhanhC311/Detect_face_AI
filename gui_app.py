from tkinter import *
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os

class APP_GUI(Frame):

    def __init__(self,parent,file_path):
        super().__init__(parent)

        self.k = 0 
        self.t = 0
        self.w = parent.winfo_width()
        self.h = parent.winfo_height()
        self.cap = cv2.VideoCapture(0)

        #Tạo 1 Frame
        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.Frame1.config(relief=GROOVE)
        self.Frame1.config(borderwidth="2")
        self.Frame1.config(background="#FFCC99")

        #Tạo 1 Label dùng để hiển thị ảnh hoặc video gốc
        self.label = Label(self.Frame1)
        self.label.place(relx=0.03, rely=0.03, relheight=0.9 , relwidth= 0.5)
        # self.label.config(bg="#3399CC")

        #Tạo một thuộc tính rỗng.
        self.emj_result = None

        # Tạo 1 label hiển thị kết quả text: giới tính, cảm xúc
        self.lbResult = Label(self.Frame1)
        self.lbResult.place(relx=0.58, rely= 0.6, relheight= 0.14, relwidth= 0.34)
        self.lbResult.config(bg="#FFCC99")

        # Tạo text hiển thị kết quả: tỉ lệ nhận diện cảm xúc.
        self.txtResult = Text(self.Frame1)
        self.txtResult.place(relx= 0.58, rely=0.76,relheight=0.2,relwidth=0.34)
        self.txtResult.config(bg="#FFCC99")
        self.txtResult.config(relief='flat',borderwidth=0,highlightthickness= 0)

        #Button quay vể trang chủ
        self.btnBack = Button(self.Frame1)
        self.btnBack.place(relx=0, rely=0.95, relheight=0.05, relwidth=0.1)
        self.btnBack.config(text='''Back''')
        self.btnBack.config(font=('Small Fonts',25))
        self.btnBack.config(activeforeground="#99FFFF")
        self.btnBack.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.btnBack.config(command=lambda: self.call_back())

        #Button ok, trong chức năng dùng camera, click ok sẽ cho ra kết quả hiển thị emoji
        self.btnOk = Button(self.Frame1)
        self.btnOk.config(text='''OK''')
        self.btnOk.config(font=('Small Fonts',25))
        self.btnOk.config(activeforeground="#99FFFF")
        self.btnOk.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.btnOk.config(command=lambda: self.setK())


        if(file_path ==" "): #Nếu không truyền đường dẫn tệp
            self.face_recog_from_camera() # nhận diện bằng cammera
        else:
            if file_path.endswith(".png") or file_path.endswith(".jpg") or file_path.endswith(".jfif"):
                self.face_recog_from_img(file_path) # Nhận diện cảm xúc của tệp hình ảnh
            else:
                if file_path.endswith(".mp4") :
                    self.cap = cv2.VideoCapture(file_path)
                    self.face_recog_from_camera()
                else:
                    messagebox.showwarning("Error", "Định dạng tệp không phù hợp, hãy chắc chắn tệp của bạn là hình ảnh hoặc video")
                    self.call_back()



    def face_recog(self,frame):
        self.FaceFrame = self.detect_faces(frame)
        image = cv2.cvtColor(self.FaceFrame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo
        try:
            result = DeepFace.analyze(self.FaceFrame,actions=['emotion'],enforce_detection=True)
            result2 = DeepFace.analyze(self.FaceFrame, actions=['gender'],enforce_detection=True)

            print(result2[0]['dominant_gender'])
            print(result2[0]['gender'])            
            print(result[0]['emotion'])

            try:
                sorted_result = sorted(result[0]['emotion'].items(),key=lambda x: x[1], reverse=True)
                text = "\n".join([f"{key}: {value}" for key, value in sorted_result])
                self.txtResult.config(font=('Small Fonts',14))
                self.txtResult.config(fg="white")
                self.txtResult.delete('1.0', END)
                self.txtResult.insert("1.0", text)
                self.txtResult.place(relx= 0.58, rely=0.76,relheight=0.2,relwidth=0.34)

            except:
                text = "\n".join([f"{key}: {value}" for key, value in result[0]['emotion'].items()])
                self.txtResult.config(font=('Small Fonts',12))
                self.txtResult.config(fg="white")
                self.txtResult.delete('1.0', END)
                self.txtResult.insert("1.0", text)
                self.txtResult.place(relx= 0.58, rely=0.76,relheight=0.2,relwidth=0.34)

            if(self.k == 1):
                self.k = 0
                self.t = 1
                # tạo một text
                Rtext =result[0]['dominant_emotion'].capitalize()+" "+result2[0]['dominant_gender']
                self.lbResult = Label(self,text = Rtext)
                self.lbResult.place(relx=0.58, rely= 0.6, relheight= 0.15, relwidth= 0.34)
                self.lbResult.config(font=('Small Fonts',25))

                path = os.getcwd().replace("\\","/") +"/emojis/"
                self.emj_url = (path+result2[0]['dominant_gender']+"/"+result[0]['dominant_emotion']+".png")
                self.emj_result = Photo(self,self.emj_url)
                self.emj_result.place(relx=0.58, rely= 0, relheight= 0.6, relwidth=0.34)
        except:
            self.txtResult.delete('1.0', END)
            self.txtResult.insert("1.0", "Không thể nhận diện")
            self.txtResult.config(font=('Small Fonts',25))
            self.txtResult.config(fg="red")
            self.txtResult.place(relx= 0.58, rely=0.76,relheight=0.2,relwidth=0.34)

            if self.t == 0 :
                try:
                    print(self.t)
                    print(self.h,self.w)
                    self.emj_result = Photo(self,"img/not4.png",self.h//10*7,self.w//10*4)
                    self.emj_result.place(relx=0.58, rely= 0.05, relheight= 0.7, relwidth=0.34)
                except:
                    print("không mở được ảnh")

    
    def call_back(self):
        self.cap.release()
        self.destroy()

    def setK(self):
         self.k = 1


    def face_recog_from_camera(self):
        
        self.btnOk.place(relx=0.3, rely=0.95, relheight=0.05, relwidth=0.1)
        ret, frame = self.cap.read()
        if ret:
           self.face_recog(frame)
    
        # lặp lại quá trình cập nhật khung hình
        self.label.after(20, self.face_recog_from_camera)
            

    def face_recog_from_img(self,img_path):
        self.k = 1 

        img = Image.open(img_path)
        img=img.resize((self.w//2,self.h*9//10), Image.ANTIALIAS)
        img.save("temp.png", format="png")

        frame = cv2.imread("temp.png") #Đọc hình ảnh
        self.face_recog(frame)
            

    def detect_faces(self,frame):
        # chuyển đổi khung hình thành ảnh xám để tăng tốc độ xử lý
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # sử dụng CascadeClassifier để nhận diện khuôn mặt
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(100, 100))
        # vẽ hình chữ nhật xung quanh khuôn mặt và trả về hình ảnh mới
        for (x, y, w, h) in self.faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        return frame

        
class Photo(Frame):
    def __init__(self,parent,path_to_img,h=None,w=None):
        super().__init__(parent)
        self.config(bg="#00CCFF")
        self.canvas = Canvas(self)
        self.canvas.config(bg ="#FFCC99")

        img = Image.open(path_to_img)
        if h != None and w != None :
            img=img.resize((w,h), Image.ANTIALIAS)

        img.save("temp.png", format="png")
        self.img = PhotoImage(file="temp.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)  
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)


class BlinkingTitle(Frame):

    def __init__(self, parent, title, f):
        Frame.__init__(self, parent)
        self.config(bg= parent['bg'])
        self.label = Label(self, text=title,font= f)
        self.label.config(bg = parent['bg'])
        self.label.pack(pady=20)
        self.blink()

    def blink(self):
        self.label.configure(fg='red')
        self.after(500, self.unblink)

    def unblink(self):
        self.label.configure(fg='blue')
        self.after(500, self.blink)