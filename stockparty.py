# -*- coding: utf-8 -*- 
from Tkinter import *
import tkMessageBox as message
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime
import dateutil
from time import localtime, strftime
import unicodedata
# plt.rcParams['text.usetex'] = True

### Script to calculate prices during beursfuif.
### To run this script, create a text file, named beer_list.txt, in the same directory as the script itself and create two columns:
### Beers   Prices
### Stella  1.3
### ...	 ...
###
### Important note: the text file needs the header 'beers' and 'prices' (though the names are not important)
### otherwise one of your beers will not be used in the program. If you have/want a file without a header, follow the directions in the
### defineGlobals function.
###
### The script also saves the price history every time it gets updated. So when someone exits the program or a computer crash
### happens, you don't lose everything. If that happens, follow the guidelines in the defineGlobals function.
###
### The script creates a single plot to show the entire history of beer prices. If you want the script to show different
### plots for each beer, comment the existing showGraphs function and uncomment the other one.
### Every time the button to calculate new prices is pressed, a new plot is created, so if you're showing the graph to the audience,
### make sure you replace the old one every update.
###
### To use the script, make sure you can run python on your computer. If you're on a windows, I suggest following the
### steps in one of the following webpages:
### https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
### https://www.howtogeek.com/197947/how-to-install-python-on-windows/
###
### Make sure you run your command window as administrator when installing pip.
###
### To run the script, simply open a command window and move to the directory that has the script in it. To change
### directories, use the cd command. To move up a directory, type cd ../
### For example, let's say you're in the folder C:\Users\YourName\Downloads and the script is in the folder
### C:\Users\YourName\Documents\Stock-Party, type the following line in the console:
###
### cd ..\Documents\Stock-Party\
###
### This should get you to the proper directory. From there, type the following line in the command window:
### 
### python stockparty.py
###
### This should get the program to work.
### For more specific comments to adjust the program to your liking, see the rest of the script.

class mainWindow(Frame):
	### Create initial state.
	def __init__(root, master):
		Frame.__init__(root, master)
		root.grid()
		### Define global variables to be used in the varying functions.
		root.defineGlobals()
		### Create the different widgets based on all the beers.
		root.create_widgets()
		root.showGraphs()
	
	def create_widgets(root):
		root.entries = []
		### This loop creates all the entry widgets for the different beers in your lijst file.
		for i in range(len(beers)):
			label = Label(root, text = beers[i])
			label.grid(row = i + 1)
			
			entry = Entry(root)
			entry.grid(row = i + 1, column = 1)
			root.entries.append(entry)
			
		### If you want to change the text on the button, change it here.
		root.calc_button = Button(root, text = "Bereken nieuwe prijzen", command = root.calculatePrices)
		root.calc_button.grid(row = len(beers) + 2, column = 1)
		
		### Button to implement stock crash, if you don't want to use this button accidentally, change the line to
		### root.crash_button = Button(root, text = "Beurscrash!", state = DISABLED, command = root.crash)
		root.crash_button = Button(root, text = "Beurscrash!", command = root.crash)
		root.crash_button.grid(row = len(beers) + 2, column = 0)
	
	### This function retrieves the values of the widgets after you click the button and converts it to float.
	def get_values(root):
		try:
			return [float(entry.get()) for entry in root.entries]
		except ValueError:
			message.showerror("Error", "Geef enkel getalwaarden in aub.")
	
	### Function to calculate the new prices.
	def calculatePrices(root):
		newPrices = []
		points = []
		for i in range(len(priceHistory[-1])):
			points.append(priceHistory[-1][i]/1.3)
			
		sales = root.get_values()
		totalPoints = sum(np.multiply(sales, points))
		avgPoints = totalPoints/len(sales)
		### This loop calculates the new prices. If the price is outside of the allowed range of prices, it selects
		### either the minimum or maximum price. If you don't want to work with min/max prices, remove/comment the if
		### statements and simply add the line newPrices.append(newPrice) under the calculation.
		for i in range(len(sales)):
			newPrice = round(priceHistory[-1][i]*(1 + (sales[i]*points[i] - avgPoints)/totalPoints), 1)
			if priceLimits[0][i] <= newPrice <= priceLimits[1][i]:
				newPrices.append(newPrice)
			elif newPrice < priceLimits[0][i]:
				newPrices.append(priceLimits[0][i])
			elif newPrice > priceLimits[1][i]:
				newPrices.append(priceLimits[1][i])
		
		### The new prices get added to the priceHistory.
		priceHistory.append(newPrices)
		
		### This creates the lines that will be printed in the window to show the new prices.
		info = []
		for i in range(len(newPrices)):
			info.append(beers[i] + ": € " + str(newPrices[i]))
		
		### This checks the time when the button was pressed, which is used in plotting the price history.
		currentTime = strftime("%H:%M", localtime()) 
		time.append(dateutil.parser.parse(currentTime))
		
		### Windows has problems saving files with ":" in it, which Linux does not. So in order to be able to save
		### the files on windows, we need to use something else, such as an "u". I prefered the way it looks
		### on Linux, so if you're running this on one, feel free to comment out the next line.
		currentTime = currentTime.split(":")[0]+"u"+currentTime.split(":")[1]
		
		### Save a copy of the price history and time history, just in case the program/computer crashes or someone accidentally shuts
		### it down. Based on the timestamp, you can restart the program without having lost everything. See
		### defineGlobals() for more info.
		np.savetxt("PriceHistory_"+str(currentTime)+".txt", priceHistory, fmt = '%s')
		np.savetxt("TimeHistory_"+str(currentTime)+".txt", time, fmt = '%s')
		
		### Show the new prices.
		message.showinfo("Nieuwe prijzen", "\n".join(info))
		
		### Update the graphs.
		root.showGraphs()
	
	def crash(root):
		newPrices = []
		### When the stock crashes, we invert the difference between the original price and the current price. So a beer that costs 50% more
		### than it's original price will now cost 50% less than it's original price.
		for i in range(len(priceHistory[-1])):
			newPrices.append(round(priceHistory[0][i]/(priceHistory[-1][i]/priceHistory[0][i]), 1))
		
		### The new prices get added to the priceHistory.
		priceHistory.append(newPrices)
		
		### This creates the lines that will be printed in the window to show the new prices.
		info = []
		for i in range(len(newPrices)):
			info.append(beers[i] + ": € " + str(newPrices[i]))
		
		### This checks the time when the button was pressed, which is used in plotting the price history.
		currentTime = strftime("%H:%M", localtime())	 
		time.append(dateutil.parser.parse(currentTime))
		
		### Change to Windows format for saving (see calculatePrices for more info).
		currentTime = currentTime.split(":")[0]+"u"+currentTime.split(":")[1]
		
		### Save a copy of the price history and time history, just in case the program/computer crashes or someone accidentally shuts
		### it down. Based on the timestamp, you can restart the program without having lost everything. See
		### defineGlobals() for more info.
		np.savetxt("PriceHistory_"+str(currentTime), priceHistory, fmt = '%s')
		np.savetxt("TimeHistory_"+str(currentTime), time, fmt = '%s')
		
		### Show the new prices.
		message.showinfo("Nieuwe prijzen", "\n".join(info))
		
		### Update the graphs.
		root.showGraphs()
		
	def run(root):
		root.mainloop()
	
	### Function to show graphs.
	### The time axis is created the moment you click the button the first time.
	def showGraphs(root):
		plt.close()
		adjustprops = dict(left=0.05, bottom=0.05, right=0.98, top=0.98)
		for i in range(len(priceHistory[-1])):
			history = []
			for j in range(1, len(priceHistory)):
				history.append(priceHistory[j][i])
			plt.plot(time, history, 'o-', label = beers[i])
			
		for j in range(len(priceHistory[-1])):
			plt.annotate(beers[j]+": "+str(priceHistory[-1][j]), (time[-1], priceHistory[-1][j] + 0.02), fontsize = 18)
		
		plt.legend(loc = 'upper center', bbox_to_anchor=(0.5, 1.), ncol = len(priceHistory[-1]), shadow = True)
		### Set the format of the x-axis in hours:minutes.
		xfmt = md.DateFormatter("%H:%M")
		plt.gcf().autofmt_xdate()
		plt.gca().xaxis.set_major_formatter(xfmt)
		### This line sets the limit on the x axis. It starts 15 minutes before the first time you click the button and 
		### goes until 9 hours later. If you want to remove the x limit all together, comment out the line itself, 
		### the result will be a graph centered on the start time. If you want to change the time the graph starts/ends,
		plt.xlim(time[0] - datetime.timedelta(minutes = 15), time[0] + datetime.timedelta(hours = 9))
		### adjust the numbers in the timedelta function.
		plt.ylabel('Prijs', fontsize = 22)
		plt.yticks(fontsize = 18)
		mng = plt.get_current_fig_manager()
		### For linux: use the line labeled #1, for windows, use the line labeled #2. For Mac, try #1, if it doesn't 
		### work, use google to find a solution.
		mng.resize(*mng.window.maxsize()) #1
		#mng.window.state('zoomed') #2
		plt.gcf().subplots_adjust(**adjustprops)
		currentTime = strftime("%H:%M", localtime())
		### Change currentTime to Windows format (see calculatePrices for more info).
		currentTime = currentTime.split(":")[0]+"u"+currentTime.split(":")[1]
		plt.gcf().savefig("GraphHistory_"+str(currentTime)+".png")
		plt.show()
	
	### Function that defines the global parameters used in the function and sets their starting values.
	def defineGlobals(root):
		### Loads the text file containing the different beers and start prices. If your file is named differently,
		### either change the value in the loadtxt function or change the name of the file. If it is in another
		### directory than the one where your script is, give the full pathname of the file.
		### If you file has no header, just beer names and prices, set skiprows to 0.
		lijst = np.loadtxt("beer_list.txt", dtype = "string", skiprows = 1)

		global beers
		beers = lijst[:, 0]
		
		startPrices = lijst[:, 1]
		floatPrices = []
		for i in range(len(startPrices)):
			floatPrices.append(float(startPrices[i]))
		
		global priceHistory
		priceHistory = [floatPrices]
		priceHistory.append(floatPrices)
		
		global time
		time = [dateutil.parser.parse(strftime("%H:%M", localtime()))]
		### If someone accidentally closed the program, use these lines and comment the above. Change the HH:MM text in the file name by the hour and		
		### time of the last update. Check your directory and see what the last file is.
		# global priceHistory
		# priceHistory = np.loadtxt("PriceHistory_HH:MM.txt", dtype = float)
		
		# global time
		# time = np.loadtxt("TimeHistory_HH:MM.txt", dtype = "string")
		
		
		### This sets the price limits for your beers. If you want to limits on price, follow the steps in the 
		### calculatePrices function.
		### The minimum and maximum are currently set to half and double the start price, respectively.
		### If you want to change the price limits, change the values in the min/max price lines indicated below.
		global priceLimits
		priceLimits = [[] for i in range(2)]
		for i in range(len(floatPrices)):
			priceLimits[0].append(round(0.5*floatPrices[i], 1)) # Minimum price
			priceLimits[1].append(round(2.0*floatPrices[i], 1)) # Maximum price
	
	### The code below is for showing different plots for each beer.
	#def showGraphs(root):
		#b = len(priceHistory[-1]) 
		#adjustprops = dict(left=0.05, bottom=0.05, right=0.97, top=0.95)#, wspace=0.2)
		#fig, axs = plt.subplots(b, 1, figsize = (20., 15.), sharex = True)
		#fig.subplots_adjust(**adjustprops)
		
		#for i in range(b):
			#history = []
			#for j in range(1,len(priceHistory)):
				#history.append(priceHistory[j][i])
				
			#xfmt = md.DateFormatter("%H:%M")
			#axs[i].xaxis.set_major_formatter(xfmt)
			#axs[i].plot(time, history, 'o-')
			#axs[i].set_xlim(time[0], time[0] + datetime.timedelta(hours = 9))
			#axs[i].set_title(beers[i])
			#labels = axs[i].get_yticks()
			#axs[i].set_yticklabels(labels, fontsize = 16)
		
		#plt.gcf().autofmt_xdate()
		#plt.gca().xaxis.set_major_formatter(xfmt)
		#plt.xlim(time[0] - datetime.timedelta(minutes = 15), time[0] + datetime.timedelta(hours = 9))
		#mng = plt.get_current_fig_manager()
		#mng.resize(*mng.window.maxsize())
		#plt.gcf().subplots_adjust(**adjustprops)
		#plt.show()
		
		

root = Tk()
root.title("Beursfuif")

fuif = mainWindow(root)
fuif.run()

