##Socket library
import socket
import threading
import time
import sys
import re
def connectToTwitch(UserName,OAuth,Channel):
    ##IRC connection data
    HOST="199.9.253.199" ##This is the Twitch IRC ip, don't change it.
    PORT=6667 ##Same with this port, leave it be.
    NICK= UserName ##This has to be your bots username.
    PASS= OAuth ##Instead of a password, use this http://twitchapps.com/tmi/, since Twitch is soon updating to it.
    IDENT= UserName ##Bot username again
    REALNAME= "ZZZZZZZZZ" ##This doesn't really matter.
    CHANNEL= Channel ##This is the channel your bot will be working on.
 
    s = socket.socket( ) ##Creating the socket variable
    s.connect((HOST, PORT)) ##Connecting to Twitch
    s.send("PASS %s\r\n" % PASS) ##Notice how I'm sending the password BEFORE the username!
    ##Just sending the rest of the data now.
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    ##Connecting to the channel.
    s.send("JOIN %s\r\n" % CHANNEL)
    return s
def defaultfunction():
    return "cmd not found"

def parseVersion(version):
    p = re.findall(r'\d+', version)
    n = p[0:len(p)-1]
    vs = ""
    for q in n:
        vs+= str(q) + "."
    return "Using Python version " + vs[0:len(vs)-1]

globcount = 0

def count():
    global globcount
    globcount +=1
    return str(globcount)


#all functions called must return strings
def getResponse(cmd):
    if( cmd == "version"):
        return parseVersion(str(sys.version_info))
    elif(cmd == "count"):
        return count()
    else:
        return ""

def botLoop(s,CHANNEL):
    ## This infinite loop doesn't work as intended: String parsing is wrong
    readbuffer = ""
    while (1):
            ##Receiving data from IRC and spitting it into manageable lines.
            readbuffer=readbuffer+ s.recv(1024) # nfSocket.recv(1024)
            temp= readbuffer.split("\n") #  string.split(readbuffer, "\n")
            readbuffer=temp.pop( )
            for line in temp:
                    print(line)
                    ##IRC checks connectiond with ping. Every ping has to be replied to with a Pong.
                    if(line[0:4]=="PING"):
                        pong = "PONG %s\r\n" % line[5:len(line)-1]
                        s.send(pong)

                    firstSplit = line.split("PRIVMSG",2)
                    secondSplit = "1"
                    if(len(firstSplit)>=2):
                        secondSplit = firstSplit[1].split(":",2)
                    chatmsg = "none"
                    if(len(secondSplit)>=2):
                        chatmsg = secondSplit[1]
                    ##Checks if the first character is a !, for commands.
                    if(chatmsg[0] == '!'):
                            cmd = chatmsg[1:].split()[0]
                            ##Checks what command was queried.
                            toSend = getResponse(cmd)
                            if(toSend != ""):
                                ##Sending a reply to the channel. Notice the : before the actual message, that's mandatory, as well as the \r\n to let it post the new line.
                                reply ="PRIVMSG "+CHANNEL+" :"+toSend+"\r\n"
                                ##Sending the reply through the socket
                                s.send(reply)

 

                           
# Never terminates. Sends specified 'message' to the specified 'channel' every 'delay' seconds over socket 'skt'
def sendMessage (skt,Channel,Message,delay=30.5): 
    i = 1
    while True:
        print("Ran " + str(i) + " times so far")
        i+=1
        reply ="PRIVMSG "+ Channel +" :" + Message + "\r\n"
        ##Sending the reply through the socket
        z = skt.send(reply)
        time.sleep(delay)
        
def chatBot(UserName,OAuth,Channel,Message,Delay=30.5):
    s = connectToTwitch(UserName,OAuth,Channel)
    sendMessage(s,Channel,Message,Delay)