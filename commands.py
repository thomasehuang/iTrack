import os
# import os.path
import socket
import pyautogui
import threading
import time
from tkinter import *
from PIL import ImageTk, Image
from AppKit import NSSound

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

# Commmand functions
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

def help_window(window, name):
    img = Image.open('res/NavMode.png')
    if name == "reader":
        img = Image.open('res/ReadMode.png')
    elif name == "watcher":
        img = Image.open('res/WatchMode.png')
    elif name == "url":
        img = Image.open('res/UrlMode.png')
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

    percent = 1
    if percent < 1:
        new_h = int(new_h * percent)
        new_w = int(new_w * percent)

    img = img.resize((new_w, new_h))
    img = ImageTk.PhotoImage(img)
    canvas = Canvas(window, width=new_w, height=new_h)
    canvas.pack()
    canvas.create_image(0, 0, image=img, anchor=NW)

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

reader_mod = Mode("reader")
reader_mod.set_command("left", "Decrease Font", pyautogui.hotkey,'command', '-')
reader_mod.set_command("right", "Increase Font", pyautogui.hotkey,'command', '+')
reader_mod.set_command("wright", "Page Down", page_down)
reader_mod.set_command("wleft", "Page Up", page_up)

web_mode = Mode("navigation")
web_mode.set_command("left", "Back", pyautogui.hotkey,'command', 'left')
web_mode.set_command("right", "Enter", pyautogui.hotkey,'enter')
web_mode.set_command("wright", "Next", pyautogui.hotkey,'tab')
web_mode.set_command("wleft", "Previous", pyautogui.hotkey,'shift', 'tab')

watch_mod = Mode("watcher")
watch_mod.set_command("left", "Decrease Volume", pyautogui.hotkey,'up')
watch_mod.set_command("right", "Increase Volume", pyautogui.hotkey,'down')
watch_mod.set_command("wright", "Pause", pyautogui.hotkey,'space')
watch_mod.set_command("wleft", "Fullscreen", pyautogui.hotkey,'f')

url_mode = Mode("url")
url_mode.set_command("left", "Open Gmail", goto_url,'https://www.gmail.com/')
url_mode.set_command("right", "Open Reddit", goto_url,'https://www.reddit.com/')
url_mode.set_command("wright", "Open NY Times", goto_url,'https://www.nytimes.com/')
url_mode.set_command("wleft", "Open Youtube", goto_url,'https://www.youtube.com/')

modes = [url_mode, web_mode,reader_mod, watch_mod]
mode_pos = 0

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

    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.bind(("localhost", 8123))
    socks.listen(5)
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
                    img = help_window(menu, modes[mode_pos].name)
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
                    img = help_window(menu, modes[mode_pos].name)
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
            img = help_window(menu, modes[mode_pos].name)
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
