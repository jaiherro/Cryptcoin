#Cryptcoin 5.6
#GUI 2.4

### IMPORT ### - Import all the dependencies and catches any error if the user doesn't have them.

try: #Splash screen, a try method is used in case the art cannot be displayed.
    print("""
     ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██████╗ ██╗███╗   ██╗
    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔════╝██╔═══██╗██║████╗  ██║
    ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║     ██║   ██║██║██╔██╗ ██║
    ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║     ██║   ██║██║██║╚██╗██║
    ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╗╚██████╔╝██║██║ ╚████║
     ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝
""")
except:
    print("Welcome to Cryptcoin.\n")

try: #Import all dependencies and if one does not exist, inform user in the proper format.
    import time
    import os
    import threading
    import configparser
    import json
    import requests
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt
    import tkinter as tk
    from tkinter import ttk
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
except Exception as e:
    print("{0}: Critical Error - Dependency missing or corrupted, cannot continue, refer to user guide.".format(time.strftime("%I:%M:%S")))
    print()
    print("{0}: Error Message - {1}.".format(time.strftime("%I:%M:%S"), e))
    input()
    exit()

### GUI ### - The main window for my application.
class Program():
    def __init__(self):
        print("{0}: Info - Creating GUI components.".format(time.strftime("%I:%M:%S")))

        def swap(self): #Used to store the radioValue, email address and input value and swap it with output variables when the user presses 'Enter'.
            self.radioValue = self.var.get()
            self.emailOutput = self.emailInput.get()
            try:
                self.numberOutput = int(self.numberInput.get())
            except:
                print("{0}: Entry denied.".format(time.strftime("%I:%M:%S")))
                popupmsg("Your entry cannot be accepted, please try again.", "Error!", False, None)

        def leave(self):
            os._exit(0)

        self.root = tk.Tk() #The next few lines are basic tkinter window setup.
        self.root.resizable(False, False)
        self.root.title("Cryptcoin")

        if os.path.isfile("./icon.ico") == True:
            try:
                self.root.iconbitmap("./icon.ico")
            except:
                print("{0}: Critical Error - icon.ico corrupted or invalid.".format(time.strftime("%I:%M:%S")))

        self.toolbar = ttk.Frame(self.root) #Toolbar is defined, it's used to hold the cryptocurrency values.
        self.buttonDict = {} #Dictionary holds the buttons
        self.currentName = None #Next few lines just declares some variables for later use.
        self.currentCode = None
        self.numberOutput = None
        self.email = None
        self.radioValue = None
        self.var = tk.IntVar()

        try: #Tries to read from Coins.ini but if it fails, for example if the user edited it and put in random characters, it doesn't crash but notifies the user and exits.
            config = configparser.ConfigParser()
            config.read('./Coins.ini')
            for key in config['COINS']:
                string = config['COINS'][key]
                string = string.strip().split(", ")
                self.buttonDict[key] = ButtonClass(string[0], self.toolbar)
                self.buttonDict[key].button.pack(side=tk.LEFT, padx=2, pady=2)
        except:
            print("{0}: Critical Error - Config file misconfigured or corrupt.".format(time.strftime("%I:%M:%S")))
            popupmsg("The Coins.ini file appears to be corrupted or misconfigured, please correct or delete the file.", "Error!", False, None)
            quit()

        self.toolbar.pack(side=tk.TOP, fill=tk.X) #Packs the buttons in.

        #This section is the other interactive elements of the GUI such as the seperator between the buttons and the rest of the window, the labels, the quit button, the input field, the radio buttons and the help button.
        self.seperator = ttk.Separator(self.root)
        self.seperator.pack(side=tk.TOP, fill=tk.X)
        self.quitButton = ttk.Button(self.toolbar, text="Quit", command = lambda : leave(self)).pack(side=tk.RIGHT, padx=2, pady=2)
        self.root.bind("<Escape>", leave)
        self.numberLabel = ttk.Label(self.root,text="Enter Alert Value:")
        self.numberLabel.pack(side=tk.TOP, padx=2, pady=7)
        self.numberInput = ttk.Entry(self.root)
        self.numberInput.pack(side=tk.TOP, padx=2, pady=2)
        self.numberInput.focus_set()
        self.emailLabel = ttk.Label(self.root,text="Enter Email:")
        self.emailLabel.pack(side=tk.TOP, padx=2, pady=7)
        self.emailInput = ttk.Entry(self.root)
        self.emailInput.pack(side=tk.TOP, padx=2, pady=2)
        self.submitButton = ttk.Button(self.root, text="Save", command = lambda : swap(self)).pack(side=tk.TOP, padx=2, pady=10)
        self.radioDown = ttk.Radiobutton(self.root, text="Falls", value=2, variable = self.var)
        self.radioDown.pack(side=tk.RIGHT, padx=20, pady=2)
        self.radioUp = ttk.Radiobutton(self.root, text="Exceeds", value=1, variable = self.var)
        self.radioUp.pack(side=tk.RIGHT, padx=2, pady=2)

        #This is the help button information, it shows the basic functionality of the program and who made it.
        self.help = ttk.Button(self.root, text = "Help", command = lambda : popupmsg("""Cryptcoin is used to track the live value of your preferred cryptocurrency and display it in an updating graph.
The row of buttons separated at the top represent currencies, they will update depending on what currencies are listed in the Coins.ini file.
The input value box in the middle accepts integer inputs and is used as a way to continually monitor the value of bitcoin and notify you, should it exceed or fall past your specified amount.
The email box is optionally used if the user would like to be emailed, it is not required should popup notifications are desired.
The radio buttons below it can be used to specify whether you would like to be notified when it rises or falls past your amount.
The save button must be used to submit and check your notification input amount the first time, and any other time you should need to update it.

Special thanks to --- for --- help throughout the project.

Created by ---, May 2018.""", "Help and Info", False, None)).pack(side=tk.LEFT, padx=5, pady=2)

        self.windowWidth = 150 #Sets the window width to a default of 150.
        self.windowHeight = 225 #and the height to a default of 175.
        for key in config['COINS']: #Goes through the Coins.ini config and increments the Width of the window depending on how many coins (to fit everything in).
            self.windowWidth += 75

        if self.windowWidth < 350: #Checks to make sure the window width is at least 350 pixels wide as anything lower looks strange and may not fit the other elememts of the gui such as radio buttons, if it is smaller than 350, it changes it to 350.
            self.windowWidth = 350

        self.root.update_idletasks()

        self.screenX = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2 #Gets the size of the screen divides it but two to get the middle.
        self.screenY = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2 #Gets the size of the screen divides it but two to get the middle.

        self.root.geometry("{0}x{1}+{2}+{3}".format(int(self.windowWidth), int(self.windowHeight), int(self.screenX), int(self.screenY))) #Combines all the calculated values using the .format method.
        print("{0}: Info - GUI ready for display.".format(time.strftime("%I:%M:%S")))

def popupmsg(msg, title, terminate, timeout): #This is the universal popupmsg function, it can be passed four values, a msg, a title, a terminate flag and a timeout amount, the first two are self explanitory, the terminate flag, if true, destroys the window after a given period of time, specified in the timeout variable.
    popup = tk.Tk() #Basic window setup
    popup.title(title)

    if os.path.isfile("./icon.ico") == True: #Checks if the icon exists, if so, tries to use it, if it fails, warns the user.
        try:
            popup.iconbitmap("./icon.ico")
        except:
            print("{0}: Critical Error - icon.ico corrupted or invalid.".format(time.strftime("%I:%M:%S")))

    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", padx=10, pady=10)
    if terminate == True: #Checks if terminate flag is true, if so, checks to make sure a valid timeout is entered then destroys the window after set time period.
        if (timeout != None) and (timeout != "") and (timeout != "0"):
            try:
                popup.after((timeout*1000), popup.destroy)
            except:
                print("Error")
    else:
        button = ttk.Button(popup, text="Ok", command = popup.destroy)
        button.pack(padx=10, pady=10)

    popup.update_idletasks()

    screenX = (popup.winfo_screenwidth() - popup.winfo_reqwidth()) / 2 #Finding center of screen and placing it, same as the main window GUI.
    screenY = (popup.winfo_screenheight() - popup.winfo_reqheight()) / 2

    popup.geometry("+{0}+{1}".format(int(screenX), int(screenY))) #Using the .format method to combine the values.

    popup.mainloop()

### SUPPORT CLASS FOR GUI ### - This is used to dynamically create the buttons.
class ButtonClass():
    def __init__(self, coin, root):
        self.name = coin
        self.button = ttk.Button(root, text = coin, command = self.RunGui) #Makes the button with the passed values.

    def RunGui(self): #Start program with given cryptocurrency name

        def animate(i): #The animate function is run ever second and is responsible for the graph and updating its values.

            pullData = open("./Currencies/" + Program.currentName + ".txt","r").read() #Pulls data from the database for cryptocurrency in question.
            dataList = pullData.split('\n') #Splits the data every line.
            bidList = [] #Declares and empties arrays.
            askList = []
            lastList = []
            timeList = []
            for eachLine in dataList: #Basically means, for each line, in the database that's over 1 character long append each value splitted at ", ":
                if len(eachLine) > 1:
                    first, second, third, fourth = eachLine.strip().split(', ')
                    bidList.append(float(first))
                    askList.append(float(second))
                    lastList.append(float(third))
                    timeList.append(int(fourth))

            subplotA.clear() #Clear the plots.
            subplotB.clear()
            subplotC.clear()

            subplotA.plot(askList) #Label and plot the new points/graphs.
            subplotA.set_title('Sell Price')
            subplotA.set_xlabel('Entries')
            subplotA.set_ylabel('AUD')
            subplotB.plot(bidList)
            subplotB.set_title('Buy Price')
            subplotB.set_xlabel('Entries')
            subplotB.set_ylabel('AUD')
            subplotC.plot(lastList)
            subplotC.set_title('Last Sold Price')
            subplotC.set_xlabel('Entries')
            subplotC.set_ylabel('AUD')

            fig.canvas.set_window_title(Program.currentName) #Set the window title
            fig.suptitle(Program.currentName, fontsize=20) #Set the subtitle name

            if (app.numberOutput != "") and (app.numberOutput != None) and (app.numberOutput != "0"): #If the user input amount, is not nothing then continue.
                if app.radioValue == 1: #If the radio value is 1 then continue.
                    for eachThing in lastList: #Iterate through lastlist and compare the user specified amount with each thing, if its smaller then envoke popup message.
                        if int(app.numberOutput) <= eachThing:
                            print("{0}: Info - {1} has reached user defined amount.".format(time.strftime("%I:%M:%S"), Program.currentName))
                            email(("{0} reached your defined amount!".format(Program.currentName)), ("Just a heads up, {1} reached your defined amount of {2} when it exceeded {3} at {0}!\n\n- Cryptcoin".format(time.strftime("%I:%M:%S"), Program.currentName, app.numberOutput, str(lastList[-1]))))
                            app.numberOutput = None #Reset the user specified amount after it's reached.
                            app.radioValue = None
                            popupmsg(("{0} has exceeded your specified amount!".format(Program.currentName)), "Alert!", False, None)

                elif app.radioValue == 2: #If the radio value is 2 then continue.
                    for eachThing in lastList: #Iterate through lastlist and compare the user specified amount with each thing, if its bigger then envoke popup message.
                        if int(app.numberOutput) >= eachThing:
                            print("{0}: Info - {1} has fallen past user defined amount.".format(time.strftime("%I:%M:%S"), Program.currentName))
                            email(("{0} fell past your defined amount!".format(Program.currentName)), ("Just a heads up, {1} fell past your defined amount of {2} when it reached {3} at {0}!\n\n- Cryptcoin".format(time.strftime("%I:%M:%S"), Program.currentName, app.numberOutput, str(lastList[-1]))))
                            app.numberOutput = None #Reset the user specified amount after it's reached.
                            app.radioValue = None
                            popupmsg(("{0} has fallen past your specified amount!".format(Program.currentName)), "Alert!", False, None)

        if plt.fignum_exists(1) == True: #Checks if the figure exists, if it does then it only updates the coin.
            Program.currentName = self.name

        else: #If a figure doesn't exist then create one and update the coin.
            fig = plt.figure(figsize=(16, 9), dpi=75)
            if os.path.isfile("./icon.ico") == True:
                try:
                    plt.get_current_fig_manager().window.wm_iconbitmap("./icon.ico")
                except:
                    print("{0}: Critical Error - icon.ico corrupted or invalid.".format(time.strftime("%I:%M:%S")))

            subplotA = fig.add_subplot(2,2,2)
            subplotB = fig.add_subplot(2,2,1)
            subplotC = fig.add_subplot(2,1,2)
            Program.currentName = self.name
            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()

### COLLECTION ###
def Collect():
    def Currencies():
        Previous = {}
        CoinDatabase = []

        config = configparser.ConfigParser()
        config.read('./Coins.ini')
        for key in config['COINS']: #Goes through the Coins.ini and pulls out the names and codes for the coins listed in there and appends them to an array.
            string = config['COINS'][key]
            string = string.strip().split(", ")
            CoinDatabase.append(string)

        def Grab(currencyName, currencyCode): #Function to 'Grab' currency prices from API
            url = ("https://api.btcmarkets.net/market/{0}/AUD/tick".format(currencyCode)) #extension of URL thats replaced with the currency code.

            if os.path.exists("./Currencies/") == False: #Check if the folder Currencies exists, if not, create one.
                os.makedirs("./Currencies/")
            if os.path.isfile("./Currencies/" + currencyName + ".txt") == False: #Check if the database for the selected currency exists, if not, create one
                file = open("./Currencies/" + currencyName + ".txt","w")
                file.close()

            try: #Try to download the JSON string with currency prices and extract relevant information.
                dljson = requests.get(url, verify=True)
                ask = str(dljson.json()["bestAsk"])
                bid = str(dljson.json()["bestBid"])
                last = str(dljson.json()["lastPrice"])
                tstamp = dljson.json()["timestamp"]
            except Exception: #In the event something stops the request, inform user and stop the program.
                print("{0}: Error - Connection with API failed due to invalid coin or disconnection from internet. Terminating collection thread.".format(time.strftime("%I:%M:%S")))
                quit()

            saveArray = [bid, ask, last, tstamp] #Load relevant information into an array.

            if saveArray != Previous.get(currencyName): #Compare array to dictionary, this is done to ensure only NEW information is saved, if the downloaded information is the same as the previously saved information, skip saving.
                try: #Try to save new information, in the event the attempt is stopped, inform user and quit program.
                    file = open("./Currencies/" + currencyName + ".txt","a")
                    if len(saveArray) > 1: #Save information into database with specific structure.
                        for i in range(len(saveArray)-1):
                            file.write(str(saveArray[i]) + ", ")
                    file.write(str(saveArray[len(saveArray)-1]) + os.linesep)
                    Previous[currencyName] = saveArray
                    file.close()
                except Exception:
                    print("{0}: Critical Error - Access to file system denied.".format(time.strftime("%I:%M:%S")))
                    popupmsg(("Access has been denied to " + currencyName + ".txt, please refer to user guide."), "Warning!", False, None)
                    quit()

        while True: #Infinite statement that keeps calling the Grab function with different strings representing different currencies.
            for i in CoinDatabase:
                Grab(i[0],i[1])
                time.sleep(1)

    threading.Thread(target=Currencies).start()

def email(subject, body): #Email sender function
    def emailThread(): #Threads are used to ensure there is no slowdown or noticable lag for the user when the program needs to send an email.
        if (app.emailOutput != None) and (app.emailOutput != ""): #Checks to make sure there is a valid email entered.
            try:
                msg = MIMEMultipart() #Uses build in python email formatter.
                msg['From'] = 'Cryptcoin.Notifications@gmail.com' #Hard coded sender email, used to make sure the user cannot screw up who is sending the email.
                msg['To'] = app.emailOutput #Stores the users email if they choose.
                msg['Subject'] = subject #The subject line.

                msg.attach(MIMEText(body, 'plain')) #Stores the body of the email.

                content = msg.as_string()
                server = smtplib.SMTP('smtp.gmail.com:587') #Connects to the gmail SMPT server through port 587
                server.starttls() #Encrypts connection with TLS
                server.login('Cryptcoin.Notifications@gmail.com', 'cryptcoincryptcoin') #Logs in with sender credentials
                server.sendmail('Cryptcoin.Notifications@gmail.com', app.emailOutput, content) #Sends the compiled email to the user.
                server.quit() #Disconnects from the email server.
            except:
                print("{0}: Error - Email failed to send.".format(time.strftime("%I:%M:%S"))) #In case something goes wrong with the email.
    threading.Thread(target=emailThread).start() #Starts the thread.

### SELF CHECK AND SETUP ###
def Check():
    success = 0
    failed = 0

    if os.path.isfile("./icon.ico") == False: #Interacts with dropbox to download icon file.
        try:
            print("{0}: Info - Starting icon download.".format(time.strftime("%I:%M:%S")))
            url = 'https://www.dropbox.com/s/c2vpl4ksjqryrvp/icon.ico?dl=1'
            r = requests.get(url, verify=True)
            with open('./icon.ico', 'wb') as f:
                f.write(r.content)
            print("{0}: Success - Icon download finished with no errors.".format(time.strftime("%I:%M:%S")))
            success += 1
        except:
            failed += 1
            print("{0}: Error - Icon file could not be downloaded.".format(time.strftime("%I:%M:%S")))
    else:
        success += 1
        print("{0}: Info - Icon file found.".format(time.strftime("%I:%M:%S")))

    if os.path.isfile("./Coins.ini") == False: #Check if Coins.ini exists, if it doesn't create it with the following entries:
        try:
            print("{0}: Info - No config file found, creating.".format(time.strftime("%I:%M:%S")))
            config = configparser.ConfigParser()
            config['COINS'] = {}
            config['COINS']['Bitcoin'] = 'Bitcoin, BTC'
            config['COINS']['Ethereum'] = 'Ethereum, ETH'
            config['COINS']['Ripple'] = 'Ripple, XRP'
            config['COINS']['Litecoin'] = 'Litecoin, LTC'
            config['COINS']['Bitcoincash'] = 'Bitcoin Cash, BCH'
            with open('./Coins.ini', 'w') as configfile:
                config.write(configfile)
            print("{0}: Success - Config file created successfully.".format(time.strftime("%I:%M:%S")))
            success += 1
        except Exception:
            failed += 1
            print("{0}: Critical Error - Failed to create config file, cannot continue.".format(time.strftime("%I:%M:%S")))
            popupmsg(("Cryptcoin has been denied access to file system, please refer to user guide."), "Warning!", False, None)
            exit()
    else:
        success += 1
        print("{0}: Info - Config file found.".format(time.strftime("%I:%M:%S")))

    if os.path.exists("./Currencies/") == False: #Check if the folder Currencies exists, if not, create one.
        os.makedirs("./Currencies/")

    try: #Verifies the Coins.ini file matches the needed format, if it doesnt the program will refuse to start until its corrected.
        config = configparser.ConfigParser()
        config.read('./Coins.ini')
        for key in config['COINS']:
            string = config['COINS'][key]
            string = string.strip().split(", ")
            if os.path.isfile("./Currencies/" + string[0] + ".txt") == False: #Check if the database for the currencies listed in the Coins.ini exist, if not, then create one for each.
                print("{0}: Info - {1} database created.".format(time.strftime("%I:%M:%S"), string[0]))
                file = open("./Currencies/" + string[0] + ".txt","w")
                file.close()
        print("{0}: Success - Config file verified.".format(time.strftime("%I:%M:%S")))
        success += 1
    except:
        failed += 1
        print("{0}: Critical Error - Config file failed verification.".format(time.strftime("%I:%M:%S")))
        popupmsg("The Coins.ini file appears to be corrupted or misconfigured, please correct or delete the file.", "Error!", False, None)
        quit()

    print("{0}: Info - Started API connection test.".format(time.strftime("%I:%M:%S")))

    try: #Tests the API connection to BTCMarkets, if it fails, the threaded collection function will not start but the program will still function.
        dljson = requests.get("https://api.btcmarkets.net/market/BTC/AUD/tick", verify=True)
        success += 1
        print("{0}: Success - API connection successful.".format(time.strftime("%I:%M:%S")))
        Collect() #Begin threaded collection function to interact with the API and collect the values for the cryptocurrencies listed in the Coins.ini
    except:
        failed += 1
        print("{0}: Error - API connection failed. Collection thread will not be started.".format(time.strftime("%I:%M:%S")))

    try: #Tests the email server connection.
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login('Cryptcoin.Notifications@gmail.com', 'cryptcoincryptcoin') # Don't even ask. Just want to finish this project, storing in plain text is the least of my concerns.
        server.quit()
        success += 1
        print("{0}: Success - Email connection successful.".format(time.strftime("%I:%M:%S")))
    except:
        failed += 1
        print("{0}: Error - Email connection failed. Email notifications will not be available.".format(time.strftime("%I:%M:%S")))

    print("{0}: Result - {1} module failures and {2} module successes from a total of {3}.".format(time.strftime("%I:%M:%S"), failed, success, failed + success)) #Prints the total number of failed and successful modules.

    print("{0}: Info - Self-check complete.".format(time.strftime("%I:%M:%S")))


### RUN ###
Check() #Self check and dependent file creation.

app = Program() #Create the GUI parts

print("{0}: Success - Cryptcoin ready.".format(time.strftime("%I:%M:%S")))
print()

app.root.mainloop() #Run the GUI
