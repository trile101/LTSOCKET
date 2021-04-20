from tkinter import *
from socket import *
from threading import Thread
import threading
import time
import pyautogui
import os
import wmi
import pythoncom

#=============================== Define control code ===============================#

QUIT             =  '0'
PROCESS_RUNNING  =  '1'
APP_RUNNING      =  '2'
SHUT_DOWN        =  '3'
SCREEN_CAPTURE   =  '4'
KEYSTROKE        =  '5'
EDIT_REGISTRY    =  '6'
EXIT             =  '7'

KILL             =  'K'
START            =  'S'
VIEW             =  'V'

#=============================== +++++++++++++++++++++++++ ===============================#

HOST = ''
PORT = 12225
Address = (HOST, PORT)
Server = socket(AF_INET, SOCK_STREAM)
global var_status

#=============================== +++++++++++++++++++++++++ ===============================#

def Process(Client_socket):
	while True:
		Code = Client_socket.recv(1).decode("utf8")
		print(Code)
		if (Code == VIEW):
			pythoncom.CoInitialize() # Running Windows functions in threads can be tricky since it often involves COM objects.
			print("hu o day")
			f = wmi.WMI()
			print("vao")
			for process in f.Win32_Process():
				Client_socket.sendall(bytes(str(process.ProcessId),"utf8"))
				Client_socket.recv(1)

				Client_socket.sendall(bytes(str(process.Name),"utf8"))
				Client_socket.recv(1)

				Client_socket.sendall(bytes(str(process.ThreadCount),"utf8"))
				Client_socket.recv(1)

			Client_socket.sendall(bytes('__END__',"utf8"))
		elif Code == KILL:
			a = 1
		elif Code == START:
			a = 1
		elif Code == QUIT:
			break

def take_picture(Client_socket):
	while True:
		Code = Client_socket.recv(1).decode("utf8")
		# Take picture
		if (Code == "1"):
			#screen capture
			myScreenshot = pyautogui.screenshot()
			f = myScreenshot.tobytes()
			sizef = f.__sizeof__()

			#size of picture
			Client_socket.sendall(bytes(str(sizef),'utf8'))
			Client_socket.recv(1).decode('utf8')

			#width of picture
			Client_socket.sendall(bytes(str(myScreenshot.width),'utf8'))
			Client_socket.recv(1).decode('utf8')

			#height of picture
			Client_socket.sendall(bytes(str(myScreenshot.height),'utf8'))
			Client_socket.recv(1).decode('utf8')

			#picture
			Client_socket.sendall(f)
		# Quit
		elif (Code == QUIT):
			print('quit screenshot')
			break

def Shutdown_Computer():
	os.system("C:\Windows\System32\shutdown /s /t 30")

def accept_incoming_connection():
	while True:
		try:
			Client_socket, Client_add = Server.accept()
			Z = threading.Thread(target=Run,args=(Client_socket,))
			Z.daemon = True # thread exit automatically when the main thread dies
			Z.start()
		except:
			pass

	
def Run(Client_socket):
	try:
		# ket client
		# Client_socket, Client_add = Server.accept()
		while True:
			Code = Client_socket.recv(1).decode("utf8")
			#QUIT
			if (Code == QUIT):
				Client_socket.close()
				break
			#Process
			if (Code == PROCESS_RUNNING):
				Process(Client_socket)
			#App Running
			if (Code == APP_RUNNING):
				break
			#ShutDown
			if (Code == SHUT_DOWN):
				Shutdown_Computer()
			#TAKEPIC
			if (Code == SCREEN_CAPTURE):
				take_picture(Client_socket)
			#KeyStock
			if (Code == KEYSTROKE):
				break
			#Edit_Register
			if (Code == EDIT_REGISTRY):
				break
			#Exit
			if (Code == EXIT):
				break

	except Exception as e:
		print(e)
		print("Close")
		

def Run_Program(label1):
	if label1.cget("text") == 'OFF':
		var_status.set('ON')
		label1.configure(fg='green')
		Server.bind(Address)
		Server.listen(5)
		Z = threading.Thread(target=accept_incoming_connection)
		Z.daemon = True # thread exit automatically when the main thread dies
		Z.start()


def on_closing():
	Server.close()
	window.destroy()


if __name__ == "__main__":
	window = Tk()
	window.title("Server")
	window.geometry("300x200+100+60")
	button = Button(window, text="Run Server",padx=15,pady=15, width=10, height=4, command=lambda:Run_Program(label1))
	button.pack()
	var_status = StringVar()
	var_status.set('OFF')

	label1 = Label(window,textvariable = var_status,fg='red')
	label1.pack()

	window.protocol("WM_DELETE_WINDOW", on_closing)
	window.mainloop()