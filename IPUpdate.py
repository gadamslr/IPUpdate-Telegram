import requests
import os
import time
import socket
import platform
# When launched on boot, time is needed for a network  connection to be established
time.sleep(15)

###Config###
SettingsFile = "TelegramSettings.cfg"  # Location of settings file to be used
def GetSetting(Option, File=SettingsFile):
    with open(File) as Settings:
        for line in Settings:
            if Option in line:
                SettingResult = line.split("=", 1)[1]
                SettingResult = SettingResult.rstrip()
                return SettingResult

CHATID = GetSetting("CHATID")  # Chat ID for telegram user/group
TOKEN = GetSetting("TOKEN")  # Bot token for telegram bot
URL = "http://api.telegram.org/bot{0}/sendMessage".format(TOKEN)
prefix = "[{0}] ~".format(socket.gethostname())

def sendmsg(ip):
    print("Sending IP change message")
    MSG = "{0} Current IP address has changed! New IP is now: {1}".format(prefix, ip)
    r = requests.post("{0}?chat_id={1}&text={2}".format(URL, CHATID, MSG))

def sendmsg404(ip):
    print("Sending 404 telegram message")
    MSG = "{0} Lastip address was not found! Current IP is: {1}".format(prefix, ip)
    r = requests.post("{0}?chat_id={1}&text={2}".format(URL, CHATID, MSG))

###IP Functions###
def getip():
    website = requests.get('http://api.ipify.org')
    ip = website.text
    print("Current Public IP is: {0}".format(ip))
    return ip

def getLip():
    #Read Last IP from file#
    txt = open("lastip.txt", "r")
    lastip = txt.read()
    txt.close()
    print("Last IP is: {0}".format(lastip))
    return lastip

def setLip(ip):
    #Write IP To lastip file#
    txt = open("lastip.txt", "w")
    txt.write(ip)
    txt.close()
    lastip = ip

def CheckConnection(connected):
    OS = platform.platform()
    while connected == False:
        if "Windows" in OS: # Windows and Unix have diffrent parameters for ping counts becuase standards
            pingtest = os.system("ping -n 1 8.8.8.8")
        else:
            pingtest = os.system("ping -c 1 8.8.8.8")

        if pingtest == 0:
            print("Network good!")
            connected = True
        else:
            print("Network Bad will loop!")

# Main loop for checking public IP address
def checkip(ipchange):
    #test
    while ipchange == False:
        print("\nLooping\n")
        CheckConnection(False) # Make sure still connected before trying to get an IP!
        if getip() == getLip():
            print("IP matched! Sleeping for a few minutes!")
            time.sleep(120)
            ipchange = False
        else:
            print("IP changed!!!")
            sendmsg(getip())
            setLip(getip())


###MAIN###
CheckConnection(False)

# Check if IP address has changed from last run
if os.path.exists("lastip.txt"):
    print("Last IP address found!")
else:
    print("Last IP address not found")
    sendmsg404(getip())
    setLip(getip())

if getip() == getLip():
    print("MATCH! - Not sending telegram message")
    ipchange = False
else:
    print("NO MACTCH - Sending telegram message")
    sendmsg(getip())
    setLip(getip())
    ipchange = False

# Run main loop #
checkip(ipchange)
