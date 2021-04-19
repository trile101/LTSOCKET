from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import pyautogui
import os
import socket
import win32api

#=============================== Define control code ===============================#
QUIT             =  '0'
PROCESS_RUNNING  =  '1'
APP_RUNNING      =  '2'
SHUT_DOWN        =  '3'
SCREEN_CAPTURE   =  '4'
KEYSTROKE        =  '5'
EDIT_REGISTRY    =  '6'
EXIT             =  '7'
KILL             =  '8'
START            =  '9'
#=============================== +++++++++++++++++++++++++ ===============================#
PORT             = 12225


#=============================== Declare class of function ===============================#
class Process(Toplevel):
    def __init__(self,cl,master = None):
        super().__init__(master)

        self.master = master
        self.title('Process')

        self.grab_set()

        self.client = cl
        
        self.fr1 = Frame(self,padx = 10,pady = 10)
        self.fr1.pack(side = TOP)

        self.fr2 = Frame(self,padx = 10, pady = 10)
        self.fr2.pack(side = BOTTOM)

        self.kill_btn = Button(self.fr1,text = "Kill",bd=3,width = 10,command=self.kill)
        self.kill_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.view_btn = Button(self.fr1,text = "View",bd=3,width = 10,command=self.view)
        self.view_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.del_btn = Button(self.fr1,text = "Delete",bd=3,width = 10,command=self.delete)
        self.del_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.start_btn = Button(self.fr1,text = "Start",bd=3,width = 10,command=self.start)
        self.start_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.tree = ttk.Treeview(self.fr2,selectmode = 'browse')
        self.tree.pack(side= LEFT)

        self.scoll = ttk.Scrollbar(self.fr2,orient='vertical',command = self.tree.yview)
        self.scoll.pack(side = 'right',fill='y')

        self.tree.configure(yscrollcommand = self.scoll.set)

        self.tree['columns'] = ("1","2","3")
        self.tree['show'] = 'headings'
        self.tree.column("1",width = 100,anchor = 'c')
        self.tree.column("2",width = 100,anchor = 'c')
        self.tree.column("3",width = 100,anchor = 'c')
        self.tree.heading("1",text = "Name Process")
        self.tree.heading("2",text = "ID Process")
        self.tree.heading("3",text = "Count Thread")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def kill(self):
        t = Toplevel()
        t.grab_set()
        id_input = Entry(t,bd=3,width = 25)
        id_input.insert(0,"Input ID")
        id_input.pack(side=LEFT, padx=10,pady=10)
        k = Button(t,text='Kill')
        k.pack(side=LEFT, padx=10,pady=10)
        t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        pass

    def view(self):
        pass

    def delete(self):
        pass
    
    def start(self):
        t = Toplevel()
        t.grab_set()
        id_input = Entry(t,bd=3,width = 25)
        id_input.insert(0,"Input name")
        id_input.pack(side=LEFT, padx=10,pady=10)
        k = Button(t,text='Start')
        k.pack(side=LEFT, padx=10,pady=10)
        t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        pass

    def on_closing(self,func=None):
        if func == None:
            self.grab_release()
            if self.master != None:
                self.master.grab_set()
            self.destroy()
        else:
            func.grab_release()
            self.grab_set()
            func.destroy()
        pass
        

class ListApp(Toplevel):
    def __init__(self, client,master = None):
        super().__init__(master)

        self.master = master
        self.title('List App')

        self.grab_set()

        self.client = client
        
        self.fr1 = Frame(self,padx = 10,pady = 10)
        self.fr1.pack(side = TOP)

        self.fr2 = Frame(self,padx = 10, pady = 10)
        self.fr2.pack(side = BOTTOM)

        self.kill_btn = Button(self.fr1,text = "Kill",bd=3,width = 10,command=self.kill)
        self.kill_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.view_btn = Button(self.fr1,text = "View",bd=3,width = 10,command=self.view)
        self.view_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.del_btn = Button(self.fr1,text = "Delete",bd=3,width = 10,command=self.delete)
        self.del_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.start_btn = Button(self.fr1,text = "Start",bd=3,width = 10,command=self.start)
        self.start_btn.pack(side = LEFT,padx = 5,pady= 5)

        self.tree = ttk.Treeview(self.fr2,selectmode = 'browse')
        self.tree.pack(side= LEFT)

        self.scoll = ttk.Scrollbar(self.fr2,orient='vertical',command = self.tree.yview)
        self.scoll.pack(side = 'right',fill='y')

        self.tree.configure(yscrollcommand = self.scoll.set)

        self.tree['columns'] = ("1","2","3")
        self.tree['show'] = 'headings'
        self.tree.column("1",width = 100,anchor = 'c')
        self.tree.column("2",width = 100,anchor = 'c')
        self.tree.column("3",width = 100,anchor = 'c')
        self.tree.heading("1",text = "Name Application")
        self.tree.heading("2",text = "ID Application")
        self.tree.heading("3",text = "Count Thread")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def kill(self):
        t = Toplevel()
        t.grab_set()
        id_input = Entry(t,bd=3,width = 25)
        id_input.insert(0,"Input ID")
        id_input.pack(side=LEFT, padx=10,pady=10)
        k = Button(t,text='Kill')
        k.pack(side=LEFT, padx=10,pady=10)
        t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        pass

    def view(self):
        pass

    def delete(self):
        pass
    
    def start(self):
        t = Toplevel()
        t.grab_set()
        id_input = Entry(t,bd=3,width = 25)
        id_input.insert(0,"Input name")
        id_input.pack(side=LEFT, padx=10,pady=10)
        k = Button(t,text='Start')
        k.pack(side=LEFT, padx=10,pady=10)
        t.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(t))
        pass

    def on_closing(self,func=None):
        if func == None:
            self.grab_release()
            if self.master != None:
                self.master.grab_set()
            self.destroy()
        else:
            func.grab_release()
            self.grab_set()
            func.destroy()
        pass

class Pic(Toplevel):
    def __init__(self,client,master = None):
        super().__init__(master)
        self.client = client

        self.master = master
        self.title('Pic')
        
        self.grab_set()

        self.fr1 = Frame(self,width = 550,height =400)
        self.fr1.configure(highlightbackground="black",highlightthickness=1)
        self.fr1.pack(side = LEFT,padx = 20, pady = 20)

        self.take()

        self.fr2 = Frame(self)
        self.fr2.pack(side = RIGHT,padx=10,pady=10)

        self.take_btn = Button(self.fr2,text = 'Take',height = 5, width = 10,font = 10,bd=5,command=self.take)
        self.take_btn.pack(side = TOP)

        self.save_btn = Button(self.fr2,text = 'Save',height = 5, width = 10,font = 10,bd=5,command = self.save)
        self.save_btn.pack(side = BOTTOM)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def take(self):
        for widget in self.fr1.winfo_children():
            widget.destroy()
        self.client.sendall(bytes(str('1'),'utf8'))

        sizef = int(self.client.recv(2048).decode('utf8'))
        self.client.sendall(bytes(str('1'),'utf8'))

        w = int(self.client.recv(2048).decode('utf8'))
        self.client.sendall(bytes(str('1'),'utf8'))

        h = int(self.client.recv(2048).decode('utf8'))
        self.client.sendall(bytes(str('1'),'utf8'))

        data = self.client.recv(sizef)

        self.img = Image.frombytes(mode = 'RGB',size=(w,h), data=data)
        cre_img = self.img.resize((550,400),Image.ANTIALIAS)
        
        render_img = ImageTk.PhotoImage(cre_img)
        
        self.label = Label(self.fr1,image = render_img)
        self.label.image = render_img
        self.label.pack()
        pass

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension = ".png")
        if not filename:
            return
        self.img.save(filename)
        pass

    def on_closing(self,func=None):
        if func == None:
            self.grab_release()
            if self.master != None:
                self.master.grab_set()
            self.destroy()
        else:
            func.grab_release()
            self.grab_set()
            func.destroy()       
        pass

class Keylog(Toplevel):
    def __init__(self,client,master =None):
        super().__init__(master)
        self.client = client
        self.master = master
        self.title('Keystroke')

        self.grab_set()

        self.keys = StringVar()
        self.keys.set('')

        self.fr1 = Frame(self,padx=10,pady=10)
        self.fr1.pack(side = TOP)

        self.fr2 = Frame(self,padx = 10,pady = 10)
        self.fr2.configure(highlightbackground="black",highlightthickness=1)
        self.fr2.pack(side = BOTTOM)

        self.hook_btn = Button(self.fr1,text = 'Hook',font = 10, bd=5,padx=10,pady=10,command=self.hook)
        self.hook_btn.grid(column = 0,row=0)

        self.unhook_btn = Button(self.fr1,text = 'Unhook',font = 10, bd=5,padx=10,pady=10,command=self.unhook)
        self.unhook_btn.grid(column = 1,row=0)

        self.print_btn = Button(self.fr1,text = 'Print',font = 10, bd=5,padx=10,pady=10,command=self.print)
        self.print_btn.grid(column = 2,row=0)

        self.del_btn = Button(self.fr1,text = 'Delete',font = 10, bd=5,padx=10,pady=10,command=self.delete)
        self.del_btn.grid(column = 3,row=0)

        self.text = Text(self.fr2,height = 20,width=50)
        self.scroll = Scrollbar(self.fr2,command=self.text.yview)
        self.text.configure(yscrollcommand = self.scroll.set,state=DISABLED)
        
        self.text.pack(side = LEFT)
        self.scroll.pack(side = LEFT, fill=Y)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def hook(self):
        pass

    def unhook(self):
        pass

    def print(self):
        pass

    def delete(self):
        pass

    def on_closing(self,func=None):
        if func == None:
            self.grab_release()
            if self.master != None:
                self.master.grab_set()
            self.destroy()
        else:
            func.grab_release()
            self.grab_set()
            func.destroy()
        pass

class Registry(Toplevel):
    def __init__(self,client,master = None):
        super().__init__(self,master)

        self.client = client
        self.title('Registry')

        self.fr1 = Frame(self)
        self.fr1.pack()

        self.fr2 = Frame(self)
        self.fr2.pack()

        self.fr3 = Frame(self)
        self.fr3.pack()

        

class App(Tk):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.title("Client")

        self.fr1 = Frame(self,padx=10,pady = 10)
        self.fr1.pack()

        self.fr2 = Frame(self,padx=10,pady=5)
        self.fr2.pack()

        self.input_ip = Entry(self.fr1,bd=5, fg='grey',font=14,width = 45)
        self.input_ip.insert(0,"Input IP")
        self.input_ip.bind("<FocusIn>", self.foc_in)
        self.input_ip.grid(column = 0, row = 0)

        self.connect_btn = Button(self.fr1,bd=3,font = 1, text = "Connect",command = self.connect)
        self.connect_btn.grid(column = 1, row = 0)

        #==============================================================================#

        self.process_btn = Button(self.fr2,text = "Process Running" ,bd = 5,font = 10,padx = 10,pady = 10, command = self.Process_running)
        self.process_btn.grid(column = 0, row = 0, columnspan = 2, rowspan = 3,sticky=N+S+E+W)

        self.app_btn = Button(self.fr2,text = "App Running",bd = 5,font = 10,padx = 10,pady = 10, command = self.App_running)
        self.app_btn.grid(column = 2 , row = 0, columnspan = 3,sticky=N+S+E+W)

        self.shut_down_btn = Button(self.fr2,text = "Shut down",bd = 5,font = 10,padx = 10,pady = 10)
        self.shut_down_btn.grid(column = 2, row = 1,sticky=N+S+E+W)

        self.scr_capture_btn = Button(self.fr2,text = "Screen capture",bd = 5,font = 10,padx = 10,pady = 10, command=self.Scr_capture)
        self.scr_capture_btn.grid(column = 3, row = 1, columnspan = 2,sticky=N+S+E+W)

        self.key_btn = Button(self.fr2,text = "Keystroke",bd = 5,font = 10,padx = 10,pady = 10, command = self.Keystroke)
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
            server_address = (ip,PORT)
            try:
                self.client.connect(server_address)
                self.connected = True
                messagebox.showinfo(title="Notification",message="Connection successful !!!")
            except Exception as e:
                print(e)
                messagebox.showerror(title="Error", message="Opps\nConnection error!")
        pass

    def Process_running(self):
        if self.connected:
            Viewapp = Process(self.client,self)
            # self.grab_set()
        else:
            messagebox.showerror(title="Error", message="Opps\nConnection error!")            
        pass

    def App_running(self):
        if self.connected:
            Viewapp = ListApp(self.client,self)
            # self.grab_set()
        else:
            messagebox.showerror(title="Error", message="Opps\nConnection error!")
        pass

    def Shut_down(self):
        pass

    def Scr_capture(self):
        if self.connected:
            self.client.sendall(bytes(SCREEN_CAPTURE,'utf8'))
            Viewapp = Pic(self.client,self)
        else:
            messagebox.showerror(title="Error", message="Opps\nConnection error!")
        pass

    def Keystroke(self):
        if self.connected:
            Viewapp = Keylog(self.client,self)
        else:
            messagebox.showerror(title="Error", message="Opps\nConnection error!")
        pass

    def Edit_registry(self):
        pass

    def exit(self):
        pass

    def quit(self):
        pass

    def on_closing(self):
        pass    

    def run(self):
        self.root.mainloop()
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()