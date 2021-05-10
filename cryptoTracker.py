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

#Returns the price of the crypto grabbed from the API
#	Args: cryptoCode - code used on website to identify the currency
#	  	  key - the API key
def getCryptoPrice(cryptoCode, key):

	#Generates url
	url = "https://api.lunarcrush.com/v2?data=assets&key="+key+"&symbol=BTC"

	#Fetches and parses JSON into dictionary data
	page = requests.get(url)
	data = page.json()

	#returns the price from json file
	return data["data"][0]["price"]


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

        x=screenWidth-320
        y=screenHeight-200

        windowWidth = 300
        windowHeight = 100 

        #Configures window
        self.window = Tk()
        self.window.geometry(str(windowWidth) + 'x' + str(windowHeight) + '+' + str(x) + '+' + str(y))
        #self.window.overrideredirect(True)

        '''
        #Loads Team Images
        self.imageFile1 = Image.open(self.imagePath1).resize((75, 75), Image.ANTIALIAS)
        self.image1 = ImageTk.PhotoImage(self.imageFile1)
        self.imageLabel1 = Label(image=self.image1)
        self.imageLabel1.image = self.image1
        self.imageLabel1.place(x=10, y=25)
		self.imageLabel1.bind("<1>", self.openLink)


        #Configures title text
		
        self.titleLabel = Label(self.window, text=self.title, font= ("Verdana", 13))
        self.titleLabel.pack()
		'''

        self.priceLabel = Label(self.window, text="", font= ("Verdana", 13))
        self.priceLabel.pack()

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

    def updateWindow(self):
        price = getCryptoPrice(self.triCode, key)
        self.priceLabel.config(text = str(price))
        self.window.after(1000, self.updateWindow)



key = getAPIKey()
print(getCryptoPrice(key, key))

widget = CurrencyWidget(key, title="Title", price=getCryptoPrice(key, key), image1="", triCode="doge")
widget.createWindow()