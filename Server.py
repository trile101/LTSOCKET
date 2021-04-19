from tkinter import *
from socket import *
from threading import Thread
import threading
import time
import pyautogui
import os
import wmi

def take_picture(Client_socket):
	while True:
		Code = Client_socket.recv(1).decode("utf8")
		# Take picture
		if (Code == "1"):
			print("oke - da chup anh")
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
		if (Code == "0"):
			break

def Shutdown_Computer():
	os.system("C:\Windows\System32\shutdown /s /t 30")

def Process(Client_socket):
	c = wmi.WMI()
	
def Run():

	Server.bind(Address)
	try:
		Server.listen()
		# ket client
		Client_socket, Client_add = Server.accept()
		while True:
			Code = Client_socket.recv(1).decode("utf8")
			#QUIT
			if (Code == "0"):
				break
			#Process
			if (Code == "1"):
				Process(Client_socket)
			#App Running
			if (Code == "2"):
				break
			#ShutDown
			if (Code == "3"):
				Shutdown_Computer()
			#TAKEPIC
			if (Code == "4"):
				take_picture(Client_socket)
				break
			#KeyStock
			if (Code == "5"):
				break
			#Edit_Register
			if (Code == "6"):
				break
			#Exit
			if (Code == "7"):
				break

	except:
		print("Close")

def Run_Program():
	threading.Thread(target=Run).start()


def on_closing():
	Server.close()
	window.destroy()

HOST = ''
PORT = 12225
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
	