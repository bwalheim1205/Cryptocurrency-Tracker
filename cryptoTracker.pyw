'''
Cryptocurrency Tracker

Version: 1.0
Author: Brian Walheim

Description: Creates a little interface widget for displaying 
cryptocurrency information


API Reference:

https://lunarcrush.com/developers/docs# 
- holds tons of data such as price of period 
  as well as social media hype for the currency

'''

#Imports for reading api
import requests
import json

#Handles window creation
from tkinter import *
from win32api import GetSystemMetrics
from PIL import ImageTk, Image

import webbrowser 

#Reads api key from first line of config file
#	Return: API Key
def getAPIKey():
	file = open("config.txt")

	return file.readline()

#Returns the info of the crypto grabbed from the API in a tuple
#	Args: cryptoCode - code used on website to identify the currency
#	  	  key - the API key
#
#   Returns: Tuple formatted (price, 7d change, 24 hour change, tweet surplus)    
def getCryptoInfo(cryptoCode, key):

	try:
		#Generates url
		url = "https://api.lunarcrush.com/v2?data=assets&key="+key+"&symbol="+cryptoCode

		#Fetches and parses JSON into dictionary data
		page = requests.get(url)
		data = page.json()

		#Debug statement for printing json
		#print(json.dumps(data, indent=2))

		#returns the price from json file
		return (data["data"][0]["price"], 
		data["data"][0]["percent_change_24h"],
		data["data"][0]["percent_change_7d"],
		data["data"][0]["timeSeries"][0]["tweets"],)
	except:
		return(0,0,0,0)


class CurrencyWidget:

    #Constructs a new notification
    def __init__(self, key, title="Title", price=0, image1="", triCode="doge"):
        self.title = title
        self.imagePath1 = image1
        self.price = price
        self.link = "https://lunarcrush.com/coins/" + triCode.lower()
        self.key = key
        self.triCode = triCode

    def createWindow(self):

        #cConfigures screen orientation
        screenWidth = GetSystemMetrics(0)
        screenHeight = GetSystemMetrics(1)

        x=screenWidth-370
        y=screenHeight-200

        windowWidth = 350
        windowHeight = 100 

        #Configures window
        self.window = Tk()
        self.window.title("Doge Coin Tracker")
        self.window.iconbitmap("dogeIcon.ico")
        self.window.geometry(str(windowWidth) + 'x' + str(windowHeight) + '+' + str(x) + '+' + str(y))
        #self.window.overrideredirect(True)
   
        #Loads Team Images
        self.imageFile1 = Image.open(self.imagePath1).resize((75, 75), Image.ANTIALIAS)
        self.image1 = ImageTk.PhotoImage(self.imageFile1)
        self.imageLabel1 = Label(image=self.image1)
        self.imageLabel1.image = self.image1
        self.imageLabel1.pack(side=LEFT)
        self.imageLabel1.bind("<1>", self.openLink)

        #Maps the data grid
        self.dataGrid = Frame(self.window)

        #Configures title text
        self.titleLabel = Label(self.window, text=self.title, font= ("Verdana", 13))
        self.titleLabel.pack()

        #Holds information key
        self.keyLabel1 = Label(self.dataGrid, text="Price/Tweets", font= ("Verdana", 10))
        self.keyLabel1.grid(row=0, column=0, padx=(0))

        self.keyLabel2 = Label(self.dataGrid, text="24H/7D", font= ("Verdana", 10))
        self.keyLabel2.grid(row=1, column=0, padx=(0))

        #Holds the price label
        self.priceLabel = Label(self.dataGrid, text="", font= ("Verdana", 13))
        self.priceLabel.grid(row=0, column=1, padx=(10))

        #Tweets Label
        self.tweetLabel = Label(self.dataGrid, text="", font= ("Verdana", 13))
        self.tweetLabel.grid(row=0, column=2, padx=(10))

        #24 Hour Change label
        self.dayLabel = Label(self.dataGrid, text="", font= ("Verdana", 13))
        self.dayLabel.grid(row=1, column=1, padx=(10))

        #7 day Change label
        self.weekLabel = Label(self.dataGrid, text="", font= ("Verdana", 13))
        self.weekLabel.grid(row=1, column=2, padx=(10))

        self.dataGrid.pack(side=RIGHT)

        #Updates window with proper information
        self.updateWindow()

        #Creates window
        self.window.mainloop()

    #Opens webpage on click of notification
    def openLink(self, event):
        webbrowser.open_new(self.link)
        self.window.destroy()

    #Destroys the window
    def destroyWindow(self):
        self.window.destroy()

    #Updates the window with new data
    def updateWindow(self):

        #Gets dataTuple
        dataTuple = getCryptoInfo(self.triCode, key)

        #Changes label text
        self.priceLabel.config(text = "${:.3f}".format(dataTuple[0]))
        self.dayLabel.config(text = "{:.1f}%".format(dataTuple[1]))
        self.weekLabel.config(text = "{:.1f}%".format(dataTuple[2]))
        self.tweetLabel.config(text = "{:d}".format(dataTuple[3]))

        #Handles color change for 24 hour and week change percentages
        if(dataTuple[1] >= 0):
            self.dayLabel.config(fg = "green")
        else:
            self.dayLabel.config(fg = "red")

        if(dataTuple[2] >= 0):
            self.weekLabel.config(fg = "green")
        else:
            self.weekLabel.config(fg = "red")

        #Sets function to be called again in 1000
        self.window.after(1000, self.updateWindow)

#----------------
# Main
#----------------

#Get API key from config file
key = getAPIKey()

#Creates Currency Window for Doge Coin
widget = CurrencyWidget(key, title="Doge Coin", price=getCryptoInfo("doge",key), image1="./doge.png", triCode="doge")
widget.createWindow()
