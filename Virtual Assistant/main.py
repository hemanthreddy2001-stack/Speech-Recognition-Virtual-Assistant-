# tasks to do:
# 1. open an app: Chrome, zoom, notepad, cmd, calculator
# 2. get info about a topic on wikipedia
# 3. automate a whatsapp message
# 4. incr/decrement volume/brightness

#importing libraries
import pyttsx3
import speech_recognition as sr
import pywhatkit as pw
import pyautogui as pg
import wikipedia
import csv
import time
import re
import sys
import screen_brightness_control as sbc

# initialize resources and global variables
r=sr.Recognizer()
mic=sr.Microphone()
engine=pyttsx3.init()
engine.setProperty('rate', 150)
typingModeEnabled = False


def speech_to_txt(r, mic,response):
    if not isinstance(r, sr.Recognizer):
        raise TypeError("'r' must be 'sr.Recognizer' instance")
    if not isinstance(mic, sr.Microphone):
        raise TypeError("'mic' must be 'sr.Microphone' instance")
    with mic as src:
        r.adjust_for_ambient_noise(src)
        speak(engine, 'speak now')
        print('listening....')
        audio=r.listen(src)
    response={
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        print('transcribing...')
        response['transcription']=r.recognize_google(audio).lower()
        print('you said: '+response['transcription'])
    except sr.RequestError:
        response['success']=False
        response['error']='API unreachable'
    except sr.UnknownValueError:
        response['error']='Unable to recognize speech'
    return response
    
# recognize command and take action
def recognizeCommand(response):
    if response['success']==False:
        print(response['error'])
        sys.exit()
    else:
        while response['error'] is not None:
            speak(engine,response['error']+". Try again")
            response=speech_to_txt(r,mic,response)
    return response
def takeAction(response):
    global typingModeEnabled
    response=recognizeCommand(response)
    speechInput=response['transcription']
    chromePatternWithWebsite=re.search("open [a-z]+ on browser$", speechInput)
    if chromePatternWithWebsite:
        openBrowser(site=speechInput.replace('open ', '').replace(' on browser', ''))
    else:
        # search for other pattern
        # opening application
        appPattern=re.search("open [a-z]+", speechInput)
        if appPattern:
            app=speechInput.replace('open ', '')
            if app == 'browser':
                openBrowser()
            elif app == 'notepad':
                openNotepad()
            elif app == 'windows explorer':
                openWinExplorer()
            elif app == 'command prompt':
                openCmd()
            else:
                res=None
                while res is None or (res['transcription']!='yes' and res['transcription']!='no'):
                    speak(engine, "can't find app on taskbar. do you want to search it on windows start menu? say yes or no")
                    res=None
                    res=speech_to_txt(r, mic, res)
                    if res['transcription']=='no':
                        break
                    elif res['transcription']=='yes':
                        speak(engine, 'searching on windows start menu...')
                        time.sleep(2)
                        pg.press('win')
                        time.sleep(2)
                        pg.write(app)
                        time.sleep(2)
                        pg.press('enter')
        else: 
            # whatsapp message
            whtspPtn = re.search("send (a )?whatsapp message(s)?",speechInput)
            
            if whtspPtn:
                print('whatsapp message to whom?')
                speak(engine, "to whom do you want to send message?")
                contactresponse=None
                contactresponse = speech_to_txt(r,mic,contactresponse)
                contactresponse = recognizeCommand(contactresponse)
                contactname=contactresponse['transcription']
                print('what is the message?')
                speak(engine, "what message you want to send to "+contactname)
                msgresponse=None
                msgresponse = speech_to_txt(r,mic,msgresponse)
                msgresponse = recognizeCommand(msgresponse)
                msg=msgresponse['transcription']
                print('sending '+msg+' to '+contactname)
                
                # scheduled whatsapp message
                if 'schedule' in speechInput:
                    speak(engine, 'what time do you want to send the message?')
                    hr, mins=list(input('enter in HH:MM format(24hrs)').split(':'))
                    pw.sendwhatmsg(find_phNo(contactname), msg, hr, mins,tab_close=True)
                
                # instant whatsapp message
                else:
                    pw.sendwhatmsg_instantly(find_phNo(contactname), msg,tab_close=True)
                    time.sleep(7)
                    pg.press('enter')
                speak(engine, "I have sent "+msg+" to "+contactname)
            else:
                
                # wikipedia search
                wikiPattern=re.search("(who|what) is [a-z]+",speechInput)
                if wikiPattern:
                    term = speechInput.replace(speechInput.split(" ")[0]+" is ","")
                    try:
                        speak(engine, wikipedia.summary(term,sentences=3))
                    except:
                        speak(engine, 'here is what I found on the web')
                        try:
                            pw.search(term)
                        except:
                            print('no info on '+term)
                else:
                    
                    # youtube video
                    ytPattern = re.search("play ([a-z]|[0-9]| )+ (([a-z]|[0-9]| )+)* on youtube", speechInput)
                    if ytPattern:
                        term = speechInput.replace(speechInput.split(" ")[0]+" is ", "")
                        pw.playonyt(term)
                        sys.exit()
                    else:
                        
                        # brightness
                        sysctrl = re.search("set brightness( to | )[0-9][0-9]?%", speechInput)
                        if sysctrl:
                            if "brightness" in speechInput:
                                speak(engine, "setting brightness to "+speechInput.split(" ")[-1])
                                sbc.set_brightness((speechInput.split(" ")[-1]).replace('%', ''))
                        else:
                            # volume
                            volctrl = re.search("(increase|decrease|mute|unmute) volume$",speechInput)
                            if volctrl:
                                if 'increase' in speechInput:
                                    pg.press('volumeup')
                                elif 'decrease' in speechInput:
                                    pg.press('volumedown')
                                elif 'mute' in speechInput or 'unmute' in speechInput:
                                    pg.press('volumemute')
                            else:
                                typePattern = re.search("(type|((enable)|(disable)) typing mode)", speechInput)
                                if typePattern:
                                    if 'enable' in speechInput:
                                        # enable typing mode
                                        typingModeEnabled=True
                                        print('typing mode enabled')
                                        speak(engine,'begin speaking and I will write it in text')
                                        res = None
                                        res = speech_to_txt(r, mic, res)
                                        type(res['transcription'])
                                        typingModeEnabled=False
                                        print('typing mode disabled')

                                    elif 'disable' in speechInput:
                                        #disable typing mode
                                        if typingModeEnabled == True:
                                            typingModeEnabled = False
                                            print('typing mode disabled')
                                else:
                                    winPattern = re.search('current window',speechInput)
                                    if winPattern:
                                        if 'close' in speechInput:
                                            windowOp(3)
                                        elif 'minimize' in speechInput or 'minimise' in speechInput:
                                            windowOp(0)
                                        elif 'maximize' in speechInput or 'maximise' in speechInput:
                                            windowOp(2)
                                        elif 'restore' in speechInput:
                                            windowOp(1)
                                    else:
                                        # stop the program
                                        stopPattern = re.search("^(stop|quit|end program|exit|bye)$", speechInput)
                                        if stopPattern:
                                            quit()
                                        else:
                                            # compliment
                                            comp = re.search("(good job|well done|thank(s| you)|great (job)?)",
                                                             speechInput)
                                            if comp:
                                                speak(engine,
                                                      "aww, I am just doing my job. Thank you for this compliment")
                                            else:
                                                speak(engine,
                                                      "Unable to take action on what you have said. Please try again.")


def openWinExplorer():
    speak(engine,'opening windows explorer')
    time.sleep(4)
    with pg.hold('win'):
        pg.press('1')
def openCmd():
    speak(engine,'opening cmd')
    time.sleep(4)
    with pg.hold('win'):
        pg.press('r')
    time.sleep(2)
    pg.write('cmd')
    time.sleep(2)
    pg.press('enter')
def openNotepad():
    speak(engine,'opening notepad')
    time.sleep(4)
    with pg.hold('win'):
        pg.press('r')
    time.sleep(2)
    pg.write('notepad')
    time.sleep(2)
    pg.press('enter')
def openBrowser(site=''):
    speak(engine, 'opening browser')
    time.sleep(3)
    
    # assuming browser is 2nd app on taskbar
    with pg.hold('win'):
        pg.press('2')
    if site != '':
        if site == 'telegram':
            url='https://web.telegram.org/k/'
        elif site== 'whatsapp':
            url='https://web.whatsapp.com/'
        elif site== 'gmail' or site== 'mail':
            url='https://mail.google.com/'
        elif site=='youtube':
            url='https://youtube.com/'
        elif site == 'google meet':
            url = 'https://meet.google.com/'
        elif site == 'facebook':
            url= 'https://www.facebook.com/'
        elif site == 'twitter':
            url= 'https://twitter.com/'
        elif site == 'instagram':
            url= 'https://www.instagram.com/'
        elif site == 'pinterest':
            url = 'https://in.pinterest.com/'
        elif site == 'github':
            url = 'https://github.com/'
        elif site == 'logic works':
            url = 'https://logikworks.instacks.co/'
        time.sleep(4)
        with pg.hold('altleft'):
            pg.press('d')
        time.sleep(3)
        pg.write(url)
        time.sleep(2)
        pg.press('enter')
        
def speak(engine,text):
    engine.say(text)
    engine.runAndWait()
    
def find_phNo(name):
    with open(r"C:\Users\sindu\Desktop\python\contacts.csv", 'r') as file:
            csvfile=csv.DictReader(file)
            for r in csvfile:
                    if name.lower()==dict(r)['Names']:
                            return dict(r)['Phone_numbers']
    return None

# for typing special chars
def type(text):
    chars = {
        '(dot)|(full stop)': '.',
        'comma': ',',
        "question mark": '?',
        "percentage (symbol)?": '%',
        "((ampers)?and)|(and symbol)": '&',
        "dollar(sign)?": '$',
        "exclamation (sign|mark)?": '!',
        "colon": ':',
        "semicolon": ';',
        "hash(tag|code| symbol)?": '#',
        "single quote(s)?": "'",
        "double quote(s)?": '"',
        "at (sign| the rate sign)": '@',
        "(forward )?slash": '/',
        "back(ward )?slash": "\\",
        "asterisk": '*',
        "opening parenthesis": '(',
        "closing parenthesis": ')',
        "opening square (parenthesis)|(brackets)": '[',
        "closing square (parenthesis)|(brackets)": ']',
        "opening brace(s)?": '{',
        "closing brace(s)": '}',
        "back( )?tick": '`',
        "tilde": '~',
        "(opening angular (parenthesis)|(brackets))|(less than symbol)": '<',
        "(closing angular (parenthesis)|(brackets))|(greater than symbol)": '>',
        "plus": '+',
        "(minus)|(dash)|(hyphen)": '-',
        "underscore": '_',
        "equal(s)?( to)?": '=',
        "new( )?line": '\n',
        "(horizontal )?tab": '\t'
    }
    isCharSpoken = False
    for x in list(chars.keys()):
        if re.search('^'+str(x),text):  # does `charname == re.search` fetch the regex match or do we have to check if `re.search` is true?
            isCharSpoken = True
            pg.write(chars[x])
            # speak(engine,  charname+' written')
            break
    time.sleep(2)
    if not isCharSpoken:
        pg.write(text)
    speak(engine, 'done typing.')


#current window (close, minimize, maximize, resize)
def windowOp(op):
    # minimize
    if op==0:
        with pg.hold('win'):
            pg.press('down')
        print('window minimized')

    # maximize
    elif op==1:
        with pg.hold('win'):
            pg.press('up')
        print('window maximized')

    # restore down
    elif op==2:
        windowOp(1)
        time.sleep(2)
        windowOp(0)
        print('window restored')

    # close
    elif op==3:
        windowOp(1)
        time.sleep(2)
        pg.click(x=1327,y=10) # coordinates of close button when maximized
        print('window closed')

# driver code
if __name__=='__main__':
    speak(engine,'hello! how may I help you?') # prompt message
    response = None
    while True: # indefinitely wait for user response until input is to quit program
        response=speech_to_txt(r,mic,response)
        takeAction(response)

# you can add further functionalities like adding calendar events, timer, etc.