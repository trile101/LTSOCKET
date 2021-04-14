from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import socket
import win32api

SCREEN_CAPTURE = '4'

class Pic():
    def __init__(self,root,client):
        self.client = client

        self.root = Toplevel()
        self.direction = "img.jpg"

        self.fr1 = Frame(self.root,padx = 5,pady=15)
        self.fr1.pack(side = LEFT)

        self.fr2 = Frame(self.root,padx = 5,pady = 15)
        self.fr2.pack(side = RIGHT)

        self.img = Image.open(self.direction)
        self.img = self.img.resize((450,500),Image.ANTIALIAS)
        
        self.my_img = ImageTk.PhotoImage(self.img)
        
        self.src_img =  Label(self.fr1,image = self.my_img)
        self.src_img.image = self.my_img
        self.src_img.pack()    

        self.take_pic_btn = Button(self.fr2,font = 2,bd=3,text = "Screenshot")
        self.take_pic_btn.pack(fill = Y,expand = 1,side = TOP)

        self.save_btn = Button(self.fr2,font = 2,bd=3,text = "Save")
        self.save_btn.pack()

    def run(self):
        self.root.mainloop()
        pass



class App:
    def __init__(self):
        self.connected = False
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.root = Tk()
        self.root.title("Client")

        self.fr1 = Frame(self.root,padx=10,pady = 10)
        self.fr1.pack()

        self.fr2 = Frame(self.root,padx=10,pady=5)
        self.fr2.pack()

        self.input_ip = Entry(self.fr1,bd=5, fg='grey',font=14)
        self.input_ip.insert(0,"Nhập IP")
        self.input_ip.bind("<FocusIn>", self.foc_in)
        self.input_ip.grid(column = 0, row = 0)

        self.connect_btn = Button(self.fr1,bd=3,font = 2, text = "Kết nối",command = self.connect)
        self.connect_btn.grid(column = 1, row = 0)

        #==============================================================================#

        self.process_btn = Button(self.fr2,text = "Process Running" ,bd = 5,font = 10,padx = 10,pady = 10)
        self.process_btn.grid(column = 0, row = 0, columnspan = 2, rowspan = 3,sticky=N+S+E+W)

        self.app_btn = Button(self.fr2,text = "App Running",bd = 5,font = 10,padx = 10,pady = 10)
        self.app_btn.grid(column = 2 , row = 0, columnspan = 3,sticky=N+S+E+W)

        self.shut_down_btn = Button(self.fr2,text = "Shut down",bd = 5,font = 10,padx = 10,pady = 10)
        self.shut_down_btn.grid(column = 2, row = 1,sticky=N+S+E+W)

        self.scr_capture_btn = Button(self.fr2,text = "Screen capture",bd = 5,font = 10,padx = 10,pady = 10, command=self.Scr_capture)
        self.scr_capture_btn.grid(column = 3, row = 1, columnspan = 2,sticky=N+S+E+W)

        self.key_btn = Button(self.fr2,text = "Keystroke",bd = 5,font = 10,padx = 10,pady = 10)
        self.key_btn.grid(column = 5, row = 0, columnspan = 2, rowspan = 2,sticky=N+S+E+W)

        self.registry_btn = Button(self.fr2,text = "Edit registry",bd = 5,font = 10,padx = 10,pady = 10)
        self.registry_btn.grid(column = 2, row = 2, columnspan = 4,sticky=N+S+E+W)

        self.exit_btn = Button(self.fr2,text = "Exit",bd = 5,font = 10,padx = 10,pady = 10)
        self.exit_btn.grid(column = 6, row=2,sticky=N+S+E+W)

    def foc_in(self,event):
        if event.widget == self.input_ip:
            if self.input_ip['fg'] == 'grey':
                self.input_ip['fg'] ='black'
                self.input_ip.delete('0', 'end')
        pass

    def connect(self,event = None):
        ip = self.input_ip.get()
        if ip != "":
            server_address = (ip,5656)
            try:
                self.client.connect(server_address)
                self.connected = True
            except Exception as e:
                print(e)
                messagebox.showerror(title="Error connection", message="Opps\nSomething went wrong!")
        pass

    def Scr_capture(self):
        #if self.connected:
        pic = Pic(self.root,self.client)
        pic.run()
        pass

    def run(self):
        self.root.mainloop()
        pass

if __name__ == "__main__":
    app = App()
    app.run()