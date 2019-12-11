import cv2
import os
import pyscreenshot as ImageGrab
import time
import glob
import numpy as np
from tkinter import *
import tkinter
import tkinter.ttk


if __name__ == "__main__":
	running = False
	endProgram = False
	totalTime = 0
	imageCount = 0
	lastRunTime = time.time()
	try:
		file=open(os.getcwd() + "\\Video Images\\info.txt", "r")
		imageCount = int(file.readline())
		savedTime = float(file.readline()) #time from file
		totalTime = savedTime
	except:
		print("fail")
		imageCount = 0
		startTime = time.time()
	lastTime = time.time();

	def newImage():
		print(abs(time.time() - lastTime))
		print(running)
		if(running and abs(time.time() - lastTime) >= 5):
			print("newImage")
			path = os.getcwd()

			count = 0	

			s = path + "\\Video Images\\" + str(count) + ".png"

			im =ImageGrab.grab()
			last = time.time()


	def startRecord():
		global running
		running = True
		global lastTime
		lastTime = time.time()
		global lastRunTime
		lastRunTime = time.time()

	def stopRecord():
		global running
		running = False

	def export():
		if(imageCount == 0):
			return

		stopRecord()
		file = open(os.getcwd() + "\\Video Images\\info.txt", "w")
		file.write(str(imageCount) + "\n" + str(totalTime))#number of pictures first line, time second
		file.close()
		img_array = []
		size = 0
		#for filename in glob.glob(os.getcwd() + "\\Video Images\\" + '*.png'):
		img = cv2.imread(os.getcwd() + "\\Video Images\\" + str(1) + ".png")
		height, width, layers = img.shape
		size = (width,height)

		out = cv2.VideoWriter(filename = 'project.avi',fourcc=cv2.VideoWriter_fourcc(*'DIVX'), fps=15, frameSize=size)

		for i in range(imageCount):
			filename = os.getcwd() + "\\Video Images\\" + str(i) + ".png"
			img = cv2.imread(filename)
			out.write(img)
		out.release()

	def onClose():
		file = open(os.getcwd() + "\\Video Images\\info.txt", "w")
		file.write(str(imageCount) + "\n" + str(totalTime))#number of pictures first line, time second
		file.close()
		global endProgram
		endProgram = True


	def clear():
		for filename in glob.glob(os.getcwd() + "\\Video Images\\" + '*.png'):
			os.remove(filename)
		file = open(os.getcwd() + "\\Video Images\\info.txt", "w")
		file.write("0\n0")#number of pictures first line, time second
		file.close()
		global imageCount 
		imageCount = 0
		global totalTime 
		totalTime = 0
		label.config(text = str(round(float(totalTime), 2)))

	top = tkinter.Tk()
	top.attributes("-topmost", True)
	top.resizable(False, False)
	top.geometry("150x70")


	#widgets
	menu = Menu(top)
	top.config(menu=menu)
	file = Menu(menu)
	file.add_command(label="New Record", command = clear)
	menu.add_cascade(label="File", menu=file)

	label = Label(top, text = str(round(float(totalTime), 2)), width = 150, height = 20)

	mainFrame = tkinter.Frame(top, width = 150, height = 50)

	startFrame = tkinter.Frame(mainFrame, width = 50, height = 50)
	start = tkinter.Button(startFrame, command = startRecord, text = "Start", width = 5, bg = "green")
	start.pack(expand=True, fill = "both")

	endFrame = tkinter.Frame(mainFrame, width = 50, height = 50)
	end = tkinter.Button(endFrame, command = stopRecord, text = "Stop", width = 5, bg = "red")
	end.pack(expand=True, fill = "both")

	exportFrame = tkinter.Frame(mainFrame, width = 50, height = 50)
	export = tkinter.Button(exportFrame, command = export, text = "Export", width = 5, bg = "blue")
	export.pack(expand=True, fill = "both")

	#add frames to window
	startFrame.pack(side = tkinter.LEFT, expand=True, fill = "both")
	exportFrame.pack(side = tkinter.RIGHT, expand=True, fill = "both")
	endFrame.pack(side = tkinter.RIGHT, expand=True, fill = "both")
	mainFrame.pack(side = tkinter.TOP, expand=True, fill = "both")
	label.pack(side = tkinter.BOTTOM, expand=False, fill = "both")



	top.protocol("WM_DELETE_WINDOW", onClose)

	while not endProgram:
		if(running):
			totalTime += time.time() - lastRunTime
			lastRunTime = time.time()
			label.config(text = str(round(float(totalTime), 2)))


		if(running and abs(time.time() - lastTime) >= 5):
			lastTime = time.time()
			path = os.getcwd()	

			s = path + "\\Video Images\\" + str(imageCount) + ".png"
			imageCount += 1
			im =ImageGrab.grab()
			im.save(s,optimize=True,quality=75)

		top.update_idletasks()
		top.update()
