#Graphical User Interface for poker bot

#Tkinter is a module part of the built library of python for siply GUIs
import tkinter

#simple setup of app's main window
mainWindow = tkinter.Tk()
mainWindow.title("Harvard Hold'em Poker Bot")
mainWindow.geometry("600x400")
mainWindow.wm_iconbitmap('hu.ico')
mainWindow.mainloop()