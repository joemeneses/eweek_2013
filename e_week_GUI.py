'''
This application requires Python 2.7 installed and makes use of the Tkinter GUI library

This application was written for Engineering Week 2013 (Feb 17-23) for a joint event between the
	East Los Angeles College Computer Science and Engineering Club (CSE)
		and the
	East Los Angeles COllege Robotics Club

The event will allow users to use this GUI to easily program a Sumo-Bot to navigate through a maze
without prior experience by committing commands to a queue, which will then be seperately compiled
and uploaded to the robot using Parallax BASIC Stamp Editor 2.5.3

This source code is Open Source for Educational Use.

This Python GUI was written by Joseph C Meneses, CSE Club member
The accompanying BASIC robot code was written by Pedro Lopez and various other members of the Robotics Club

'''

from Tkinter import *
import tkMessageBox
import re

'''
SOURCE FILE NAME FOR ROBOT SOURCE CODE.
	Will look for this source in the same directory as this script
'''
SOURCE_FILE_NAME = "eweek_bot_source.bs2"


class Command_GUI:
	def __init__(self, master):
	
		#create command array
		self.commandArray = []
		
		#set an index marker for text field command queue
		self.command_line_num = 1.0
		
		#create the master frame that will hold the whole GUI window
		master_frame = master
		
		master_frame.rowconfigure(0, weight=1)
		master_frame.columnconfigure(0, weight=1)
		#master_frame.pack()
		
		'''
		=======
		CREATE AND PLACE ON GRID the arrow buttons
		=======
		'''
		#LEFT ARROW
		self.left_image = PhotoImage(file="left_arrow.gif")
		self.left_arrow = Button(master_frame, image=self.left_image, text="<---", command=self.sendLeftCommand)
		self.left_arrow.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=E)
		
		#FORWARD ARROW
		self.forward_image = PhotoImage(file="forward_arrow.gif")
		self.forward_arrow = Button(master_frame, image=self.forward_image, text="^", command=self.sendForwardCommand)
		self.forward_arrow.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=W+E)
		
		#RIGHT ARROW
		self.right_image = PhotoImage(file="right_arrow.gif")
		self.right_arrow = Button(master_frame, image=self.right_image, text="--->", command=self.sendRightCommand)
		self.right_arrow.grid(row=0, column=2, rowspan=1, columnspan=1, sticky=W)
		
		'''
		=======
		HELPER BUTTONS
		=======
		'''
		
		'''
		#DEBUG
		self.show_commands_button = Button(master_frame, text="SHOW COMMAND LIST", command=self.showCommandQueue)
		self.show_commands_button.grid(row=1, column=1, rowspan=1, columnspan=1)
		#self.test_button.pack(side=BOTTOM)
		'''
		
		#DELETE BUTTON
		self.delete_button_image = PhotoImage(file="DELETE.gif")
		self.delete_last_button = Button(master_frame, image=self.delete_button_image, text="DELETE LAST COMMAND", command=self.deleteLastCommandInQueue)
		self.delete_last_button.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=E+N+S)
		
		#SEND BUTTON
		self.send_button_image = PhotoImage(file="SEND.gif")
		self.save_commands_button = Button(master_frame, image=self.send_button_image, text="SAVE/SEND COMMANDS TO BOT", command=self.sendCommandQueue)
		self.save_commands_button.grid(row=1, column=2, rowspan = 1, columnspan = 1, sticky=W+N+S)
		
		'''
		======
		COMMAND QUEUE WINDOW INTERFACE
		Includes:
			"Command Queue" Label
			Text Field
			Vertical Scroll Bar
		'''
		
		#"COMMAND QUEUE" Label
		self.queue_label = Label(master_frame, text="COMMAND QUEUE")
		self.queue_label.grid(row = 0, column=3, rowspan=1, columnspan=2)
		
		#Command Text Field
		self.command_queue_text = Text(master_frame, state=DISABLED, wrap="word",height=10, width=30, background="white", borderwidth=0, highlightthickness=0)
		self.command_queue_sb = Scrollbar(orient="vertical", borderwidth=1, command=self.command_queue_text.yview)
		self.command_queue_text.configure(yscrollcommand=self.command_queue_sb.set)
		
		#Pack and sticky scroll bar with text field
		self.command_queue_text.grid(row=1, column=3, rowspan=1, columnspan=1)
		self.command_queue_sb.grid(row=1, column=4, rowspan=1, columnspan=1, sticky=W+N+S)
		
	
	'''
	======
	Text Field specific modules
	======
	'''
	def sendCommandToTextField(self, command):
		self.command_queue_text.configure(state="normal")
		self.command_queue_text.insert(END, "{0} {1}".format(self.command_line_num, command))
		self.command_queue_text.configure(state="disabled")
		
		#iterate the command counter
		self.command_line_num += 1
		return
		
	def deleteLastCommandFromTextField(self):
	
		print ("This is the delete button working")
		self.command_queue_text.configure(state="normal")
		self.command_queue_text.delete(self.command_line_num-1, self.command_line_num)
		
		self.command_queue_text.configure(state="disabled")
		
		#decrease the command line counter
		self.command_line_num -= 1.0
		return
	
	def clear_command_queue_window(self):
		#clear the window itself
		self.command_queue_text.configure(state="normal")
		self.command_queue_text.delete(1.0, END)
		self.command_queue_text.configure(state="disabled")
		
		#reset command list and line Number
		self.commandArray = []
		self.command_line_num = 1.0
		
		
		return
		
	'''
	======
	Button Bind modules
	======
	'''
	def sendLeftCommand(self):
		self.commandArray.append("L")
		self.sendCommandToTextField("Turn Left\n")
		print "SENDING: LEFT Command to QUEUE"
		return
	
	def sendForwardCommand(self):
		self.commandArray.append("F")
		self.sendCommandToTextField("Go Forward\n")
		print "SENDING: FORWARD command to QUEUE"
		return
	
	def sendRightCommand(self):
		self.commandArray.append("R")
		self.sendCommandToTextField("Turn Right\n")
		print "SENDING: RIGHT command to QUEUE"
		return
	
	'''
	#DEBUG: Print self.commandArray (The list of commands) to console window	
	def showCommandQueue(self):
		print self.commandArray
		return
	'''
	
	def deleteLastCommandInQueue(self):
		if self.command_line_num > 1:
			self.deleteLastCommandFromTextField()
			self.commandArray.pop()
		else:
			tkMessageBox.showinfo("Error", "Number of instructions is already 0, cannot delete")
		return
	

	#Sends command queue to robot text file
	def sendCommandQueue(self):
		print "COMMAND QUEUE BEING SAVED TO FILE"
		tkMessageBox.showinfo("Instructions Sent!", "Your instructions have been successfully saved!\nAsk someone to load the instructions into the robot for you.")
		
		#Add a Quit command to the end of the command queue
		self.commandArray.append("Q")
		#need a list to string module
		commandString = self.makeCommandListString()
		#send this string to bot source inserter
		self.sendStringToBot(commandString)
		
		self.clear_command_queue_window()
		return

	'''
	Bot Source File manipulation: Will open bot source, parse for
	DATA "<string>"
	'''
	def makeCommandListString(self):
		tempString = ""
		print self.commandArray
		for command in self.commandArray:
			tempString += command
		
		print tempString
		
		return tempString
	
	def sendStringToBot(self, commandString):
		self.openBotSource()
		self.parseAndInsertCommands(commandString)
		
		self.botSource.close()
		
		return
		
	def openBotSource(self):
		self.botSource = open(SOURCE_FILE_NAME, 'r+')
		
		return
		
	def parseAndInsertCommands(self, commandString):
		nextLine = False
		lineNum = 0
		DELIMITER = "insert_next_line"
		dataList = []
		
		#copy every line in the source file so we can edit the specific line
		for line in self.botSource:
			dataList.append(line)
			
		for line in dataList:
		
			#here we find the delimiting line
			if nextLine == False:
				if DELIMITER in line:
					nextLine = True
			#next line contains the DATA line. create a tempData string and change it in the temp list
			else:
				print ("Line number is ", lineNum)
				#pos = self.botSource.tell()
				tempData = "DATA\t\"%s\"\n" % commandString
				
				print ("Sending the following string: %s" % tempData)
				dataList[lineNum] = tempData
				
				#write the entire dataList back to the source file
				#(We can't edit a single line directly, python only supports complete overwrite of the text file)
				with open(SOURCE_FILE_NAME, 'w') as file:
					file.writelines(dataList)
					
				return
			
			lineNum += 1
			
		
		return
			
	

#Run the application GUI
root = Tk()
gui = Command_GUI(root)
root.mainloop()
