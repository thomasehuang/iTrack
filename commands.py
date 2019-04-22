import os
# import os.path
import socket
import glob
import pyautogui
import threading
import time
from tkinter import *
from PIL import ImageTk, Image
from AppKit import NSSound
from gtts import gTTS
import argparse

"""
Commands:
    mc  - mouse click
    if  - increase font
    df  - decrease font
    pu  - page up
    pd  - page down
    ss  - screenshot

You can chain together commands by separating them with the '|' character.
Commands will be executed in the order they are written.
For example, 'mc | df' will click the mouse then decrease the font size.
"""
CMD2NAME = {
    'mc': 'Mouse Click',
    'if': 'Increase Font',
    'df': 'Decrease Font',
    'pu': 'Page Up',
    'pd': 'Page Down',
    'ss': 'Screenshot',
}

parser = argparse.ArgumentParser()
parser.add_argument('-v', dest='v',  default=False, action='store_true')
options = parser.parse_args()
# Commmand functions
socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socks.bind(("localhost", 8123))
socks.listen(5)

def mouse_click():
    pyautogui.click()

def increase_font():
    pyautogui.hotkey('command', '+')

def decrease_font():
    pyautogui.hotkey('command', '-')

def page_up():
    pyautogui.scroll(20)

def page_down():
    pyautogui.scroll(-20)

def screenshot():
    if os.path.isfile('screenshot.png'):
        count = 0
        while True:
            fname = 'screenshot_%i.png' % (count)
            if not os.path.isfile('screenshot_%i.png' % (count)):
                pyautogui.screenshot(fname)
                break
            count += 1
    else:
        pyautogui.screenshot('screenshot.png')


# Helper functions
def parse_commands(commands):
    commands = commands.split('|')
    commands = [command.strip() for command in commands]
    return commands

def goto_url(url):
    os.system("open -a \"Google Chrome\" " + url)


b = True


def help_window(window, mode):
    img = Image.open('res/helpMenu.png')
    w, h = img.size
    ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()

    if float(h) / hs > 1.0 and float(h) / hs > float(w) / ws:
        new_h = hs
        new_w = int(w - (h - hs) * (w / h))
    elif float(w) / ws > 1.0 and float(w) / ws > float(h) / hs:
        new_h = int(h - (w - ws) * (h / w))
        new_w = ws
    else:
        new_w, new_h = w, h

    percent = .6
    if percent < 1:
        new_h = int(new_h * percent)
        new_w = int(new_w * percent)

    img = img.resize((new_w, new_h))
    img = ImageTk.PhotoImage(img)
    # canvas = Canvas(window, width=new_w, height=new_h)
    # canvas.pack()
    # canvas.create_image(0, 0, image=img, anchor=NW)
    l=Label(window,image=img)
    l.image=img       #just keeping a reference
    l.grid()
    label_name = Label(window, text=mode.name,width=10,anchor="w", font=("bold", 20))
    label_name.place(x=new_w*.535,y=new_h*.225)
    if "right" in mode.commands.keys():
        label_right = Label(window, text=mode.commands["right"][1],width=15,anchor="w", font=("bold", 14))
        label_right.place(x=new_w*.485,y=new_h*.41)

    if "wright" in mode.commands.keys():
        label_right = Label(window, text=mode.commands["wright"][1],width=15, anchor="w", font=("bold", 14))
        label_right.place(x=new_w*.2,y=new_h*.41)

    if "left" in mode.commands.keys():
        label_right = Label(window, text=mode.commands["left"][1],width=15,anchor="w", font=("bold", 14))
        label_right.place(x=new_w*.485,y=new_h*.59)
        
    if "wleft" in mode.commands.keys():
        label_right = Label(window, text=mode.commands["wleft"][1],width=10, anchor="w", font=("bold", 14))
        label_right.place(x=new_w*.2,y=new_h*.59)

    x = ws/2 - new_w/2
    y = hs/2 - new_h/2

    window.geometry("+%d+%d" % (x, y))

    return img

class Mode:
    def __init__(self, name):
        self.name = name
        self.commands = {}

    def set_command(self, movement, name, func, *args):
        self.commands[movement] = [func, name, args]

    def execute(self,movement):
        self.commands[movement][0](*self.commands[movement][2])

# reader_mod = Mode("reader")
# reader_mod.set_command("left", "Decrease Font", pyautogui.hotkey,'command', '-')
# reader_mod.set_command("right", "Increase Font", pyautogui.hotkey,'command', '+')
# reader_mod.set_command("wright", "Page Down", page_down)
# reader_mod.set_command("wleft", "Page Up", page_up)

# web_mode = Mode("nav")
# web_mode.set_command("left", "Back", pyautogui.hotkey,'command', 'left')
# web_mode.set_command("right", "Enter", pyautogui.hotkey,'enter')
# web_mode.set_command("wright", "Next", pyautogui.hotkey,'tab')
# web_mode.set_command("wleft", "Previous", pyautogui.hotkey,'shift', 'tab')

# watch_mod = Mode("watcher")
# watch_mod.set_command("left", "Decrease Volume", pyautogui.hotkey,'up')
# watch_mod.set_command("right", "Increase Volume", pyautogui.hotkey,'down')
# watch_mod.set_command("wright", "Pause", pyautogui.hotkey,'space')
# watch_mod.set_command("wleft", "Fullscreen", pyautogui.hotkey,'f')

# url_mode = Mode("url")
# url_mode.set_command("left", "Open Gmail", goto_url,'https://www.gmail.com/')
# url_mode.set_command("right", "Open Reddit", goto_url,'https://www.reddit.com/')
# url_mode.set_command("wright", "Open NY Times", goto_url,'https://www.nytimes.com/')
# url_mode.set_command("wleft", "Open Youtube", goto_url,'https://www.youtube.com/')

modes = []
files = glob.glob("modes/*")

def add_mode_from_file(filename):
    file = open(filename, "r")
    mode_name = filename.split('/')[-1]
    temp = Mode(mode_name)
    for line in file:
        line = line.strip('\n')
        line = line.split(',')
        if line[2] == 'url':
            temp.set_command(line[0],line[1],goto_url,line[3])
        elif line[2] == 'page_up':
            temp.set_command(line[0],line[1],page_up)
        elif line[2] == 'page_down':
            temp.set_command(line[0],line[1],page_down)
        elif line[2] == 'key':
            temp.set_command(line[0],line[1],pyautogui.hotkey,*line[3:])
    if mode_name == "url":
        modes.insert(0,temp)
    else:
        modes.append(temp)

def save_mode_to_file(mode):
    file = open("modes/" + mode.name, "w")
    for key in mode.commands:
        val = mode.commands[key]
        if val[0] == pyautogui.hotkey:
            file.write(key + "," + val[1] + ",key," + str(val[2])[1:-1].replace(" ", "").replace("'", "") + "\n")
        elif val[0] == page_up:
            file.write(key + "," + val[1] + ",page_up," + "\n")
        elif val[0] == page_down:
            file.write(key + "," + val[1] + ",page_down," + "\n")
        elif val[0] == goto_url:
            file.write(key + "," + val[1] + ",url," + str(val[2])[1:-1].replace(" ", "").replace("'", "") + "\n")
    file.close

def delete_mode(position):
    mode = modes[position]
    os.remove("modes/" + mode.name)
    del modes[position]



for filename in files:
    add_mode_from_file(filename)

mode_pos = 0

def custom_window(window):
    img = Image.open('res/customEditor.png')
    w, h = img.size
    ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()

    if float(h) / hs > 1.0 and float(h) / hs > float(w) / ws:
        new_h = hs
        new_w = int(w - (h - hs) * (w / h))
    elif float(w) / ws > 1.0 and float(w) / ws > float(h) / hs:
        new_h = int(h - (w - ws) * (h / w))
        new_w = ws
    else:
        new_w, new_h = w, h

    percent = .6
    if percent < 1:
        new_h = int(new_h * percent)
        new_w = int(new_w * percent)

    img = img.resize((new_w, new_h))
    img = ImageTk.PhotoImage(img)

    l=Label(window,image=img)
    l.image=img
    l.grid()

    name=StringVar()
    entry_name = Entry(window,textvariable=name)
    entry_name.place(x=new_w*.58,y=new_h*.2)

    list1 = ['key', 'url'];


    wright_type=StringVar()
    wright_droplist=OptionMenu(window,wright_type, *list1)
    wright_droplist.config(width=6)
    wright_type.set('Type') 
    wright_droplist.place(x=new_w*.15,y=new_h*.41)
    wright_args =StringVar()
    wright_args.set('Enter Command') 
    entry_wright = Entry(window,textvariable=wright_args,width =13)
    entry_wright.place(x=new_w*.25,y=new_h*.41)
    wright_name =StringVar()
    wright_name.set('Enter Command Name') 
    entry_wright_name = Entry(window,textvariable=wright_name)
    entry_wright_name.place(x=new_w*.17,y=new_h*.48)


    right_type=StringVar()
    right_droplist=OptionMenu(window,right_type, *list1)
    right_droplist.config(width=6)
    right_type.set('Type') 
    right_droplist.place(x=new_w*.465,y=new_h*.41)
    right_args =StringVar()
    right_args.set('Enter Command') 
    entry_right = Entry(window,textvariable=right_args,width =13)
    entry_right.place(x=new_w*.565,y=new_h*.41)
    right_name =StringVar()
    right_name.set('Enter Command Name') 
    entry_right_name = Entry(window,textvariable=right_name)
    entry_right_name.place(x=new_w*.485,y=new_h*.48)


    wleft_type=StringVar()
    wleft_droplist=OptionMenu(window,wleft_type, *list1)
    wleft_droplist.config(width=6)
    wleft_type.set('Type') 
    wleft_droplist.place(x=new_w*.15,y=new_h*.67)
    wleft_args =StringVar()
    wleft_args.set('Enter Command') 
    entry_wleft = Entry(window,textvariable=wleft_args,width =13)
    entry_wleft.place(x=new_w*.25,y=new_h*.67)
    wleft_name =StringVar()
    wleft_name.set('Enter Command Name') 
    entry_wleft_name = Entry(window,textvariable=wleft_name)
    entry_wleft_name.place(x=new_w*.17,y=new_h*.74)


    left_type=StringVar()
    left_droplist=OptionMenu(window,left_type, *list1)
    left_droplist.config(width=6)
    left_type.set('Type') 
    left_droplist.place(x=new_w*.465,y=new_h*.67)
    left_args =StringVar()
    left_args.set('Enter Command') 
    entry_left = Entry(window,textvariable=left_args,width =13)
    entry_left.place(x=new_w*.565,y=new_h*.67)
    left_name =StringVar()
    left_name.set('Enter Command Name') 
    entry_left_name = Entry(window,textvariable=left_name)
    entry_left_name.place(x=new_w*.485,y=new_h*.74)

    global b
    b = True
    
    def callback():
        global b
        b = False
        window.destroy()
        new_mode = Mode(name.get())
        if wright_type.get() == "url":
            new_mode.set_command("wright", wright_name.get(), goto_url,wright_args.get())
        elif wright_type.get() == "key":
            line = wright_args.get()
            line = line.split(',')
            new_mode.set_command("wright", wright_name.get(),pyautogui.hotkey,*line)

        if right_type.get() == "url":
            new_mode.set_command("right", right_name.get(), goto_url,right_args.get())
        elif right_type.get() == "key":
            line = right_args.get()
            line = line.split(',')
            new_mode.set_command("right", right_name.get(),pyautogui.hotkey,*line)

        if wleft_type.get() == "url":
            new_mode.set_command("wleft", wleft_name.get(), goto_url,wleft_args.get())
        elif wleft_type.get() == "key":
            line = wleft_args.get()
            line = line.split(',')
            new_mode.set_command("wleft", wleft_name.get(),pyautogui.hotkey,*line)

        if left_type.get() == "url":
            new_mode.set_command("left", left_name.get(), goto_url,left_args.get())
        elif left_type.get() == "key":
            line = left_args.get()
            line = line.split(',')
            new_mode.set_command("left", left_name.get(),pyautogui.hotkey,*line)
        modes.append(new_mode)
        save_mode_to_file(new_mode)
        global mode_pos
        mode_pos = len(modes) - 1


    def callbackexit():
        global b
        b = False
        window.destroy()


    Button(window, text='Exit',width=10,bg='brown',fg='white',command=callbackexit).place(x=new_w*.5,y=new_h*.825)
    Button(window, text='Save',width=10,bg='brown',fg='white',command=callback).place(x=new_w*.3,y=new_h*.825)


    x = ws/2 - new_w/2
    y = hs/2 - new_h/2

    window.geometry("+%d+%d" % (x, y))

    def testsss():
        while True:
            client = socks.accept()[0]
            message = client.recv(1024)
            client.send(str("recieved").encode("utf-8"))
            command = message.decode('ascii')
            global b
            if b == False:
                client.close()
                return
            if command == "up":
                b = False
                client.close()
                return
            client.close()

    download_thread = threading.Thread(target=testsss)
    download_thread.start()

    while b:
        window.update_idletasks()
        window.update()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host ="localhost"
    port =8123
    s.connect((host,port))
    s.send('e'.encode()) 





in_menu = False
if __name__ == '__main__':
    # For visualization
    viz = True
    menu = None
    img = None
    pause = False
    setup = False
    setup_window = None

    root = Tk()
    root.withdraw()
    while True:
        client = socks.accept()[0]
        message = client.recv(1024)
        client.send(str("recieved").encode("utf-8"))
        command = message.decode('ascii')
        sound = NSSound.alloc()

        sound.initWithContentsOfFile_byReference_('/System/Library/Sounds/Ping.aiff', True)
        #rewind and play whenever you need it:
        sound.stop() #rewind
        sound.play()
        c = ""
        if in_menu:
            if setup:
                continue
            if command == 'left':
                if pause:
                    c = 'Locked'
                else:
                    mode_pos -= 1
                    mode_pos = mode_pos % len(modes)
                    menu.destroy()
                    c = "Switch To " + modes[mode_pos].name + " Mode"
                    menu = Toplevel(root)
                    menu.title('Help Menu')
                    menu.attributes("-topmost", True)
                    img = help_window(menu, modes[mode_pos])
            elif command == 'right':
                if pause:
                    c = 'Locked'
                else:
                    mode_pos += 1
                    mode_pos = mode_pos % len(modes)
                    menu.destroy()
                    c = "Switch To " + modes[mode_pos].name + " Mode"
                    menu = Toplevel(root)
                    menu.title('Help Menu')
                    menu.attributes("-topmost", True)
                    img = help_window(menu, modes[mode_pos])
            elif command == 'up':
                in_menu = False
                c = "Close Menu"
                menu.destroy()
                menu = None
            elif command == 'wleft':
                pause = not pause
                if pause:
                    c = "Lock"
                else:
                    c = "Unlock"
            elif command == 'wright':
                menu.destroy()
                menu = Toplevel(root)
                menu.title('Help Menu')
                menu.attributes("-topmost", True)
                img = custom_window(menu)
                menu.destroy()
                menu = Toplevel(root)
                menu.title('Help Menu')
                menu.attributes("-topmost", True)
                img = help_window(menu, modes[mode_pos])
        elif command in modes[mode_pos].commands:
            if setup:
                continue
            elif pause:
                c = 'Locked'
            else:
                c = modes[mode_pos].commands[command][1]
                modes[mode_pos].execute(command)
        elif command == "up":
            in_menu = True
            c = "Open Menu"
            menu = Toplevel(root)
            menu.title('Help Menu')
            menu.attributes("-topmost", True)
            img = help_window(menu, modes[mode_pos])
            if setup_window != None:
                setup_window.destroy()
                setup_window = None
                setup = False

        elif command[:5] == "print":
            if setup_window:
                setup_window.destroy()
            setup_window = Toplevel(root)
            setup_window.title('Setup Window')
            setup_window.attributes("-topmost", True)
            w, h = 800, 300
            ws, hs = setup_window.winfo_screenwidth(), setup_window.winfo_screenheight()
            setup_window.geometry('%ix%i+%i+%i' % (w,h,ws//2 - w//2,hs//2 - h//2))

            lbl = Label(setup_window, text=command[6:], font=("Arial", 30), wraplength=750)
            lbl.grid(column=0, row=0)
            setup_window.columnconfigure(0, weight=1)
            setup_window.rowconfigure(0, weight=1)
            root.update_idletasks()
            root.update()
            if command[5:] == "~":
                setup_window.destroy()
                setup_window = None
            setup = True



        if viz:
            if c != "":
                if options.v:
                    mp3 = gTTS(text=c,lang='en',slow=False)
                    mp3.save("temp.mp3")
                    os.system("afplay temp.mp3")
                    os.system("rm temp.mp3")

                window = Toplevel(root)
                window.title('Executed Command')
                window.attributes("-topmost", True)
                w, h = 400, 50
                ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()
                window.geometry('%ix%i+%i+%i' % (w,h,ws-w-50,hs-h-50))

                lbl = Label(window, text=c, font=("Arial", 30))
                lbl.grid(column=0, row=0)
                window.columnconfigure(0, weight=1)
                window.rowconfigure(0, weight=1)
                root.update_idletasks()
                root.update()
                time.sleep(1)
                window.destroy()

        root.update_idletasks()
        root.update()

        client.close()
