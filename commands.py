import os.path
import socket
import pyautogui
import threading
import time
from tkinter import *
# from PIL import ImageTk, Image


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


def help_window():
    window = Tk()
    window.title('iTrack')

    img = Image.open("menu.png")
    width, height = img.size
    img = ImageTk.PhotoImage(img)
    canvas = Canvas(window, width=width, height=height)
    canvas.pack()
    canvas.create_image(0, 0, image=img, anchor=NW)

    ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()
    x = ws/2 - width/2
    y = hs/2 - height/2

    window.geometry("+%d+%d" % (x, y))

    window.mainloop()

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
reader_mod.set_command("left", "Decrease Volume", pyautogui.hotkey,'shift', 'options', 'f11')
reader_mod.set_command("right", "Increase Volume", pyautogui.hotkey,'shift', 'options', 'f12')
reader_mod.set_command("wright", "Pause", pyautogui.hotkey,'space')
reader_mod.set_command("wleft", "Fullscreen", pyautogui.hotkey,'f')

modes = [web_mode,reader_mod, watch_mod]


mode_pos = 0


in_menu = False
if __name__ == '__main__':
    viz = True
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.bind(("localhost", 8123))
    socks.listen(5)
    while 1:
        client = socks.accept()[0]
        message = client.recv(1024)
        client.send(str("recieved").encode("utf-8"))
        commands = [message.decode('ascii')]
        c = ""
        # commands = parse_commands(args.command)
        for command in commands:
            if in_menu:
                if commands[0] == 'left':
                    mode_pos -= 1
                    mode_pos = mode_pos % len(modes)
                elif commands[0] == 'right':
                    mode_pos += 1
                    mode_pos = mode_pos % len(modes)
                    c = "Switch Too " + modes[mode_pos].name + " Mode"
                elif commands[0] == 'up':
                    in_menu = False
                    c = "Close Menu"

            elif commands[0] in modes[mode_pos].commands:
                c = modes[mode_pos].commands[commands[0]][1]
                modes[mode_pos].execute(command)
            elif commands[0] == "up":
                in_menu = True
                c = "Open Menu"
                help_window()

        if viz:
            if c != "":
                window = Tk()
                window.title('iTrack')
                w, h = 225, 50
                ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()
                window.geometry('%ix%i+%i+%i' % (w,h,ws-w-50,hs-h-50))

                lbl = Label(window, text=c, font=("Arial", 30))
                lbl.grid(column=0, row=0)
                window.columnconfigure(0, weight=1)
                window.rowconfigure(0, weight=1)
                window.after(1000, lambda: window.destroy())
                # window.destroy()
                window.mainloop()
                print("heere")

                # pyautogui.hotkey('command', 'tab')

        client.close()
