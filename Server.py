from tkinter import *
from socket import *
from threading import Thread
import threading
import time
import pyautogui
import os

def take_picture():
	while True:
		Code = Client_socket.recv(1).decode("utf8")
		# Take picture
		if (Code == 4):
			#screen capture
			myScreenshot = pyautogui.screenshot()
			myScreenshot.save(r'test.jpg')

			file = open('test.jpg', "rb")
			file_data = file.read(2048)

			while file_data:
				Client_socket.send(file_data)
				file_data = file.read(2048)

			file.close()
			os.remove("test.jpg")
		# Quit
		if (Code == 2):
			break

def Shutdown_Computer():
	os.system("C:\Windows\System32\shutdown /s /t 30")
def Run():
	Server.bind(Address)
	try:
		Server.listen()
		# ket client
		Client_socket, Client_add = Server.accept()
		while True:
			Code = Client_socket.recv(1).decode("utf8")
			#TAKEPIC
			if (Code == "4"):
				take_picture()
			#ShutDown
			if (Code == "1"):
			#Process
			if (Code == "2"):

	except:
		print("Close")

def Run_Program():
	threading.Thread(target=Run).start()


def on_closing():
	Server.close()
	window.destroy()

HOST = ''
PORT = 1225
Address = (HOST, PORT)
Server = socket(AF_INET, SOCK_STREAM)


if __name__ == "__main__":
	window = Tk()
	window.title("Server")

	window.geometry("200x100+100+60")
	button = Button(window, text="Run Server", width=10, height=4, command=Run_Program)
	button.pack()

	window.protocol("WM_DELETE_WINDOW", on_closing)
	window.mainloop()
	